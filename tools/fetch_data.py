#!/usr/bin/env python3
"""Genera assets/live-data.js y assets/live-data.json (snapshot de respaldo del juego).

Uso:  python tools/fetch_data.py
En produccion el juego pide los datos a /api/live-data (Vercel). Este snapshot se usa
cuando esa funcion no responde o cuando se abre index.html como archivo local.
La logica vive en api/_live.py. NASA_API_KEY es opcional (NeoWs usa DEMO_KEY si falta)."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))
from _live import build  # noqa: E402


def main():
    out = build()
    if not out["bodies"]:
        print("Sin datos de Horizons; no se sobrescribe nada.", out["errors"]); sys.exit(1)
    (ROOT / "assets" / "live-data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "assets" / "live-data.js").write_text("window.LIVE_DATA=" + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
    print("OK:", len(out["bodies"]), "cuerpos;",
          "clima:", (out["space_weather"] or {}).get("level"), ";",
          "Bennu:", "ok" if out["mission_design"].get("bennu") else "-", ";",
          "NEO:", (out["neo"] or {}).get("name"), ";",
          "errores:", out["errors"] or "ninguno")


if __name__ == "__main__":
    main()
