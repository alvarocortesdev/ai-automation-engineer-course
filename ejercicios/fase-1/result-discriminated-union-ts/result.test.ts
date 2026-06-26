/**
 * Tests del ejercicio 1.9 — El patrón Result con discriminated unions (Vitest).
 *
 * Estos tests son el CONTRATO. Fijan que parseGasto NUNCA lanza (devuelve Result),
 * que el `tipo` de ParseError es el correcto, y que safeJsonParse doma el throw de
 * JSON.parse. Hazlos pasar todos y luego AÑADE un caso borde tuyo.
 *
 * Ejecuta:   pnpm dlx vitest run     (o:  npx vitest run)
 */

import { describe, it, expect } from "vitest";

import { ok, err, parseGasto, safeJsonParse } from "./result";

describe("ok / err", () => {
  it("ok envuelve el valor", () => {
    expect(ok(42)).toEqual({ ok: true, value: 42 });
  });

  it("err envuelve el error", () => {
    expect(err("roto")).toEqual({ ok: false, error: "roto" });
  });
});

describe("parseGasto", () => {
  it("devuelve ok con el Gasto para una línea válida (con trim)", () => {
    const r = parseGasto("  Lider ; 12990 ; supermercado ");
    expect(r.ok).toBe(true);
    if (r.ok) {
      expect(r.value).toEqual({ comercio: "Lider", monto: 12990, categoria: "supermercado" });
    }
  });

  it("campos != 3 => error de formato", () => {
    const r = parseGasto("Lider;12990");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error.tipo).toBe("formato");
  });

  it("comercio vacío => error de formato", () => {
    const r = parseGasto(";12990;supermercado");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error.tipo).toBe("formato");
  });

  it("monto no numérico => error de monto", () => {
    const r = parseGasto("Lider;abc;supermercado");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error.tipo).toBe("monto");
  });

  it("monto <= 0 => error de monto", () => {
    const r = parseGasto("Lider;-5;supermercado");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error.tipo).toBe("monto");
  });

  it("monto con decimales => error de monto", () => {
    const r = parseGasto("Lider;12.5;supermercado");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error.tipo).toBe("monto");
  });
});

describe("safeJsonParse", () => {
  it("JSON válido => ok con el valor parseado", () => {
    const r = safeJsonParse('{"a":1}');
    expect(r.ok).toBe(true);
    if (r.ok) expect(r.value).toEqual({ a: 1 });
  });

  it("JSON roto => err con un Error, sin lanzar", () => {
    const r = safeJsonParse("{roto");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error).toBeInstanceOf(Error);
  });
});

// TODO(estudiante): añade aquí al menos un caso borde tuyo.
// Ideas: una línea con espacios extra y categoría vacía; un JSON que parsea a `null`;
// verificar que parseGasto("Lider;0;super") da error de monto.
