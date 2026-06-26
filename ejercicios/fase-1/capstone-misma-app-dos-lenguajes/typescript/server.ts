/**
 * Capa HTTP de la despensa (TypeScript, solo node:http).
 *
 * Las AYUDAS (send, readBody, parseId) ya están escritas: son plomería.
 * Tu trabajo es el RUTEO dentro de createServer, siguiendo CONTRATO-HTTP.md.
 *
 * Corre:  npm start            (tsx server.ts)
 * Prueba: curl -s localhost:8001/health
 */

import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { join } from "node:path";
import { ZodError } from "zod";
import { PantryStore } from "./pantry";

const store = new PantryStore(join(import.meta.dirname, "pantry-data.json"));

// ---- ayudas (ya escritas; no necesitas tocarlas) ---------------------------
function send(res: ServerResponse, status: number, payload?: unknown): void {
  if (payload === undefined) {
    res.writeHead(status);
    res.end();
    return;
  }
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload));
}

async function readBody(req: IncomingMessage): Promise<string> {
  let raw = "";
  for await (const chunk of req) raw += chunk;
  return raw;
}

/** Devuelve el id de /items/{id}, o null si no es un entero. */
function parseId(path: string): number | null {
  const tail = path.slice("/items/".length);
  if (!/^\d+$/.test(tail)) return null;
  return Number(tail);
}

// ---- ruteo (TU TRABAJO) ----------------------------------------------------
const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
  const path = req.url ?? "";
  const method = req.method ?? "GET";

  // TODO: GET  /health        -> 200 { status: "ok" }
  // TODO: GET  /items         -> 200 [lista]
  // TODO: GET  /items/{id}    -> 400 si no es entero, 404 si no existe, 200 si existe
  // TODO: POST /items         -> 400 si el JSON está roto, 422 si ZodError, 201 si ok
  // TODO: DELETE /items/{id}  -> 400 si no es entero, 204 si borró, 404 si no existía
  // TODO: cualquier otra cosa -> 404

  send(res, 501, { error: "ruteo no implementado" });
});

const PORT = 8001;
server.listen(PORT, "127.0.0.1", () => {
  console.log(`Despensa (TypeScript) escuchando en http://127.0.0.1:${PORT}`);
});
