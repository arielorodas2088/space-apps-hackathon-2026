#!/usr/bin/env python3
"""Genera data/live-data.js y data/live-data.json con datos reales (solo biblioteca estandar).
Uso:  python tools/fetch_data.py
ESTADO: escrito el 14/11/2026 SIN poder probarse contra los servidores (el entorno donde se creo
no tenia acceso a ssd.jpl.nasa.gov). Corrolo localmente y revisa la salida antes de confiar en ella."""
import json, urllib.request, urllib.parse, datetime as dt, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
HOR = "https://ssd.jpl.nasa.gov/api/horizons.api"
# VERIFICAR: ruta exacta de DONKI en CCMC (migro desde api.nasa.gov el 2026-09-30, sin clave, rango maximo 30 dias)
DONKI = "https://ccmc.gsfc.nasa.gov/DONKI-API/get/FLR"
BODIES = {"luna": "301", "venus": "299", "marte": "499", "bennu": "2101955",
          "europa": "502", "titan": "606", "nept": "899"}

def get(url, params):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": "space-mission-design-game/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def horizons(cmd, start, stop):
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
    return f"{n(a)}\u2013{n(b)} {u}" if n(a) != n(b) else f"{n(a)} {u}"

def main():
    today = dt.date.today(); end = today + dt.timedelta(days=365)
    out = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "source": "NASA/JPL Horizons API (centro: geocentro)", "bodies": {}, "space_weather": None, "errors": {}}
    for k, cmd in BODIES.items():
        try:
            r = horizons(cmd, today.isoformat(), end.isoformat())
            lt = [x[0] for x in r]; km = [x[1] for x in r]
            out["bodies"][k] = {"horizons_id": cmd, "lt_now_s": lt[0], "dist_now_km": km[0],
                                "lt_min_s": min(lt), "lt_max_s": max(lt), "delay_txt": fmt(min(lt), max(lt))}
        except Exception as e:
            out["errors"][k] = str(e)[:200]
    try:
        ev = get(DONKI, {"startDate": (today - dt.timedelta(days=30)).isoformat(), "endDate": today.isoformat()})
        out["space_weather"] = {"source": "NASA CCMC DONKI", "flares_30d": len(ev),
                                "flares_M_or_X_30d": sum(1 for e in ev if str(e.get("classType", ""))[:1] in "MX")}
    except Exception as e:
        out["errors"]["donki"] = str(e)[:200]
    if not out["bodies"]:
        print("Sin datos de Horizons; no se sobrescribe nada.", out["errors"]); sys.exit(1)
    (ROOT / "data" / "live-data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "data" / "live-data.js").write_text("window.LIVE_DATA=" + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
    print("OK:", list(out["bodies"]), "errores:", out["errors"])

if __name__ == "__main__":
    main()
