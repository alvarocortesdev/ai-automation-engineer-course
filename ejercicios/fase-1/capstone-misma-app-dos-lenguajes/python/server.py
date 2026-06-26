"""Capa HTTP de la despensa (Python, solo stdlib).

Las AYUDAS (_send, _read_body, _parse_id) ya están escritas: son plomería.
Tu trabajo es el RUTEO en do_GET / do_POST / do_DELETE, siguiendo CONTRATO-HTTP.md.

Corre:  uv run python server.py     (o:  python server.py)
Prueba: curl -s localhost:8000/health
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from pydantic import ValidationError

from pantry import PantryStore

STORE = PantryStore(Path(__file__).parent / "pantry-data.json")


class Handler(BaseHTTPRequestHandler):
    # ---- ayudas (ya escritas; no necesitas tocarlas) -------------------------
    def _send(self, status: int, payload: object | None = None) -> None:
        body = b"" if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _read_body(self) -> str:
        length = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(length).decode("utf-8")

    def _parse_id(self) -> int | None:
        """Devuelve el id de /items/{id}, o None si no es un entero."""
        tail = self.path[len("/items/"):]
        try:
            return int(tail)
        except ValueError:
            return None

    # silencia el log por defecto del handler (opcional)
    def log_message(self, *args: object) -> None:  # noqa: D401
        pass

    # ---- ruteo (TU TRABAJO) --------------------------------------------------
    def do_GET(self) -> None:
        # TODO: /health -> 200 {"status":"ok"}
        # TODO: /items  -> 200 [lista]
        # TODO: /items/{id} -> 400 si el id no es entero, 404 si no existe, 200 si existe
        # TODO: cualquier otra ruta -> 404
        raise NotImplementedError

    def do_POST(self) -> None:
        # TODO: solo /items. Lee el body, parsea JSON (400 si está roto),
        #       llama a STORE.add_item (422 si ValidationError), 201 con el ítem si ok.
        raise NotImplementedError

    def do_DELETE(self) -> None:
        # TODO: /items/{id} -> 400 si no es entero, 204 si borró, 404 si no existía.
        raise NotImplementedError


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Despensa (Python) escuchando en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
