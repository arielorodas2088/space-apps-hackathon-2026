"""Funcion serverless de Vercel: GET /api/live-data

Llama a las APIs de NASA/JPL (ver _live.py) y devuelve el JSON que lee el juego.
El CDN de Vercel cachea la respuesta 6 h, asi NASA recibe pocas llamadas por dia.
Variable de entorno opcional: NASA_API_KEY (si falta, NeoWs usa DEMO_KEY).
"""
import json, os, sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _live import build  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            data = build()
            ok = bool(data["bodies"] or data["space_weather"])
        except Exception as e:  # no deberia pasar: build() aisla cada fuente
            data, ok = {"errors": {"build": str(e)[:200]}}, False
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200 if ok else 502)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "public, s-maxage=21600, stale-while-revalidate=86400"
                         if ok else "public, max-age=60")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
