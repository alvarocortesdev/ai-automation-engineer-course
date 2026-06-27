/**
 * Tests del ejercicio 4.6 A — Route Handler con validación (Vitest, entorno node).
 *
 * Verifican el CONTRATO del endpoint: filtrado, validación, status codes y la forma
 * de la respuesta. Como el handler usa Request/Response web estándar, no hace falta
 * Next.js: construimos una Request a mano y leemos la Response.
 *
 * Ejecuta:   pnpm install && pnpm test
 */

import { describe, it, expect } from "vitest";
import { GET } from "./route";
import { MODELOS } from "./datos";

// Helper: arma una Request GET contra una URL con query string y llama al handler.
function pedir(query = ""): Promise<Response> {
  return GET(new Request(`http://localhost/api/modelos${query}`));
}

describe("respuesta base", () => {
  it("sin params devuelve 200 y la forma { query, count, items }", async () => {
    const res = await pedir();
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body).toHaveProperty("query");
    expect(body).toHaveProperty("count");
    expect(body).toHaveProperty("items");
    expect(Array.isArray(body.items)).toBe(true);
  });

  it("sin params aplica el limit por defecto de 10", async () => {
    const body = await (await pedir()).json();
    expect(body.count).toBe(10); // hay 12 modelos; el default 10 los acota
    expect(body.items).toHaveLength(10);
    expect(body.query).toBe("");
  });
});

describe("filtrado", () => {
  it("filtra por nombre sin distinguir mayúsculas", async () => {
    const body = await (await pedir("?q=claude")).json();
    expect(body.count).toBe(3);
    expect(body.items.every((m: { nombre: string }) => m.nombre.toLowerCase().includes("claude"))).toBe(true);
  });

  it("filtra también por proveedor", async () => {
    const body = await (await pedir("?q=openai")).json();
    const ids = body.items.map((m: { id: string }) => m.id).sort();
    expect(ids).toEqual(["4", "5", "6"]); // los tres modelos de OpenAI
  });

  it("sin coincidencias devuelve count 0 e items vacío (pero status 200)", async () => {
    const res = await pedir("?q=zzzznada");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.count).toBe(0);
    expect(body.items).toEqual([]);
  });

  it("refleja la consulta usada en query", async () => {
    const body = await (await pedir("?q=gemini")).json();
    expect(body.query).toBe("gemini");
  });
});

describe("limit", () => {
  it("acota la cantidad de resultados", async () => {
    const body = await (await pedir("?limit=3")).json();
    expect(body.count).toBe(3);
  });

  it("un limit mayor a 50 se acota a 50 (no es error)", async () => {
    const res = await pedir("?limit=1000");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.count).toBe(MODELOS.length); // 12 < 50, devuelve todos
  });

  it("limit no numérico devuelve 400", async () => {
    const res = await pedir("?limit=abc");
    expect(res.status).toBe(400);
    expect(await res.json()).toHaveProperty("error");
  });

  it("limit 0 o negativo devuelve 400", async () => {
    expect((await pedir("?limit=0")).status).toBe(400);
    expect((await pedir("?limit=-5")).status).toBe(400);
  });
});

describe("seguridad: entrada acotada", () => {
  it("una consulta de más de 64 caracteres devuelve 400", async () => {
    const largo = "a".repeat(65);
    const res = await pedir(`?q=${largo}`);
    expect(res.status).toBe(400);
    expect(await res.json()).toHaveProperty("error");
  });
});

// 👉 Agrega aquí al menos un test tuyo (caso borde: q con espacios, limit=50
//    exacto, acentos, q en mayúsculas contra proveedor en minúsculas, ...).
