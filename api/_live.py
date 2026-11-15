"""Nucleo compartido: arma el paquete de datos reales que consume el juego.

Lo usan la funcion de Vercel (api/live-data.py) y el script local (tools/fetch_data.py).
Solo biblioteca estandar. Cada fuente falla por separado y queda anotada en "errors".
Verificado contra los servidores el 15/11/2026.
"""
import json, os, time, threading, urllib.error, urllib.request, urllib.parse, datetime as dt
from concurrent.futures import ThreadPoolExecutor

HOR = "https://ssd.jpl.nasa.gov/api/horizons.api"
MDESIGN = "https://ssd-api.jpl.nasa.gov/mdesign.api"
DONKI = "https://ccmc.gsfc.nasa.gov/DONKI-API/get/"  # migro desde api.nasa.gov (2026-09-30)
NEOWS = "https://api.nasa.gov/neo/rest/v1/feed"
BODIES = {"luna": "301", "venus": "299", "marte": "499", "bennu": "2101955",
          "europa": "502", "titan": "606", "nept": "899"}
MJD_EPOCH = dt.date(1858, 11, 17)
HOR_SLOTS = threading.Semaphore(2)  # Horizons responde 503 si recibe muchas consultas simultaneas


def get(url, params, timeout=40):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": "space-mission-design-game/0.2"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def mjd(d):
    return (d - MJD_EPOCH).days


def from_mjd(m):
    return (MJD_EPOCH + dt.timedelta(days=int(m))).isoformat()


# ---------- Horizons: distancia y luz-tiempo ----------
def horizons(cmd, start, stop):
    for intento in range(4):
        try:
            with HOR_SLOTS:
                return _horizons(cmd, start, stop)
        except urllib.error.HTTPError as e:
            if e.code != 503 or intento == 3:
                raise
            time.sleep(1.5 * (intento + 1))


def _horizons(cmd, start, stop):
    d = get(HOR, {"format": "json", "COMMAND": f"'{cmd}'", "OBJ_DATA": "'NO'", "MAKE_EPHEM": "'YES'",
                  "EPHEM_TYPE": "'VECTORS'", "CENTER": "'500@399'", "START_TIME": f"'{start}'",
                  "STOP_TIME": f"'{stop}'", "STEP_SIZE": "'10 d'", "VEC_TABLE": "'3'",
                  "CSV_FORMAT": "'YES'", "OUT_UNITS": "'KM-S'"})
    txt = d.get("result", "")
    if "$$SOE" not in txt:
        raise RuntimeError(txt[:300])
    rows = [l.split(",") for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return [(float(r[8]), float(r[9])) for r in rows]  # (luz-tiempo en s, distancia en km)


def fmt(lo, hi):
    if hi < 60: u, k = "s", 1
    elif hi < 5400: u, k = "min", 60
    else: u, k = "h", 3600
    a, b = lo / k, hi / k
    n = (lambda x: f"{x:.1f}".replace(".", ",")) if k != 60 else (lambda x: f"{x:.0f}")
    return f"{n(a)}–{n(b)} {u}" if n(a) != n(b) else f"{n(a)} {u}"


def body(cmd, today):
    r = horizons(cmd, today.isoformat(), (today + dt.timedelta(days=365)).isoformat())
    lt = [x[0] for x in r]; km = [x[1] for x in r]
    return {"horizons_id": cmd, "lt_now_s": lt[0], "dist_now_km": km[0],
            "dist_min_km": min(km), "dist_max_km": max(km),
            "lt_min_s": min(lt), "lt_max_s": max(lt), "delay_txt": fmt(min(lt), max(lt)),
            "delay_now_txt": fmt(lt[0], lt[0])}


# ---------- DONKI: clima espacial de los ultimos 30 dias ----------
FLR_RANK = {"A": 0, "B": 1, "C": 2, "M": 3, "X": 4}


def flare_key(c):
    c = str(c or "")
    try:
        return (FLR_RANK.get(c[:1], -1), float(c[1:] or 0))
    except ValueError:
        return (FLR_RANK.get(c[:1], -1), 0.0)


def space_weather(today):
    p = {"startDate": (today - dt.timedelta(days=30)).isoformat(), "endDate": today.isoformat()}
    flr, cme, gst = (get(DONKI + k, p) or [] for k in ("FLR", "CME", "GST"))
    mx = [e for e in flr if str(e.get("classType", ""))[:1] in "MX"]
    top = max(flr, key=lambda e: flare_key(e.get("classType")), default=None)
    kps = [(k.get("kpIndex") or 0, k.get("observedTime", "")) for g in gst for k in (g.get("allKpIndex") or [])]
    kp, kp_t = max(kps, default=(0, ""))
    has_x = any(str(e.get("classType", ""))[:1] == "X" for e in flr)
    level = "severe" if has_x or kp >= 6 else "moderate" if mx or kp >= 5 else "quiet"
    max_flare = {"class": top["classType"], "date": top.get("peakTime") or top.get("beginTime", "")} if top else None
    parts = []
    if max_flare: parts.append(f"fulguración {max_flare['class']} del {fecha(max_flare['date'])}")
    if kp >= 5: parts.append(f"tormenta geomagnética Kp {kp:g} del {fecha(kp_t)}")
    parts.append(f"{len(cme)} eyecciones de masa coronal en 30 días")
    return {"source": "NASA CCMC DONKI", "flares_30d": len(flr), "flares_M_or_X_30d": len(mx),
            "max_flare": max_flare, "cme_30d": len(cme), "gst_30d": len(gst),
            "max_kp": kp, "max_kp_time": kp_t, "level": level,
            "headline": "Actividad solar real: " + ", ".join(parts) + "."}


def fecha(iso):
    try:
        return dt.date.fromisoformat(iso[:10]).strftime("%d/%m")
    except ValueError:
        return iso[:10]


# ---------- Small-Body Mission Design ----------
def best_porkchop(sstr, today):
    d = get(MDESIGN, {"sstr": sstr, "mjd0": mjd(today), "span": 730,
                      "tof-min": 100, "tof-max": 900, "step": 10}, timeout=60)
    if "vinf_dep" not in d:
        raise RuntimeError(str(d.get("message", d))[:200])
    best = None
    for i, tof in enumerate(d["tof"]):
        for j, dep in enumerate(d["dep_date"]):
            a, b = d["vinf_dep"][i][j], d["vinf_arr"][i][j]
            if a and b and (best is None or a + b < best[0]):
                best = (a + b, a, b, tof, dep)
    if not best:
        raise RuntimeError("sin trayectorias en la grilla")
    return mission(d, best[1], best[2], best[3], best[4])


def best_selected(sstr):
    d = get(MDESIGN, {"sstr": sstr, "lim": 20}, timeout=60)
    rows = d.get("selectedMissions") or []
    if not rows:
        raise RuntimeError(str(d.get("message", "sin misiones precalculadas"))[:200])
    r = min(rows, key=lambda r: r[2] + r[3])
    return mission(d, r[2], r[3], r[9], r[0])


def mission(d, vdep, varr, tof, dep):
    o = d.get("object", {})
    return {"source": "NASA/JPL Small-Body Mission Design API", "object": o.get("fullname"),
            "launch_date": from_mjd(dep), "tof_days": round(tof), "vinf_dep": round(vdep, 3),
            "vinf_arr": round(varr, 3), "c3": round(vdep ** 2, 2), "warning": d.get("warning")}


# ---------- NeoWs: asteroide cercano de la semana ----------
def neo(today):
    key = os.environ.get("NASA_API_KEY") or "DEMO_KEY"
    d = get(NEOWS, {"start_date": today.isoformat(),
                    "end_date": (today + dt.timedelta(days=7)).isoformat(), "api_key": key})
    cands = [o for day in d.get("near_earth_objects", {}).values() for o in day]
    cands.sort(key=lambda o: -o["estimated_diameter"]["meters"]["estimated_diameter_max"])
    errs = []
    for o in cands[:5]:
        try:
            md = best_selected(o["neo_reference_id"])
        except Exception as e:
            errs.append(f"{o['name']}: {str(e)[:80]}"); continue
        ca = o["close_approach_data"][0]
        dm = o["estimated_diameter"]["meters"]
        return {"source": "NASA NeoWs + JPL Mission Design", "name": o["name"].strip("() "),
                "id": o["neo_reference_id"],
                "diam_m": round((dm["estimated_diameter_min"] + dm["estimated_diameter_max"]) / 2),
                "hazardous": o["is_potentially_hazardous_asteroid"],
                "miss_km": float(ca["miss_distance"]["kilometers"]),
                "vel_kms": float(ca["relative_velocity"]["kilometers_per_second"]),
                "approach_date": ca["close_approach_date"], "nasa_jpl_url": o.get("nasa_jpl_url"),
                "mission": md}
    raise RuntimeError("ningún NEO con trayectoria calculable; " + "; ".join(errs)[:200])


# ---------- Ensamblado ----------
def build(today=None):
    today = today or dt.date.today()
    out = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "source": "NASA/JPL Horizons API (centro: geocentro)", "bodies": {},
           "space_weather": None, "mission_design": {}, "neo": None, "errors": {}}
    jobs = {k: ("body", cmd) for k, cmd in BODIES.items()}
    jobs.update({"donki": ("sw",), "mdesign_bennu": ("md",), "neows": ("neo",)})

    def run(job):
        kind = job[0]
        if kind == "body": return body(job[1], today)
        if kind == "sw": return space_weather(today)
        if kind == "md": return best_porkchop("101955", today)
        return neo(today)

    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        futs = {k: ex.submit(run, j) for k, j in jobs.items()}
        for k, f in futs.items():
            try:
                v = f.result()
            except Exception as e:
                out["errors"][k] = str(e)[:200]; continue
            if k in BODIES: out["bodies"][k] = v
            elif k == "donki": out["space_weather"] = v
            elif k == "mdesign_bennu": out["mission_design"]["bennu"] = v
            else: out["neo"] = v
    return out
