import { describe, it, expect } from "vitest";

import { parsearCompra } from "./compra";

// Lo que un LLM "bien portado" devolvería. Ojo: `monto` viene como STRING.
const VALIDO = JSON.stringify({
  comercio: "Líder",
  monto: "12990",
  moneda: "CLP",
  categoria: "supermercado",
  fecha: "2026-06-21",
  items: ["leche", "pan"],
});

const base = JSON.parse(VALIDO) as Record<string, unknown>;

describe("CompraSchema (caso válido)", () => {
  it("coacciona monto string a number", () => {
    const c = parsearCompra(VALIDO);
    expect(c.monto).toBe(12990);
    expect(typeof c.monto).toBe("number");
  });

  it("conserva los demás campos", () => {
    const c = parsearCompra(VALIDO);
    expect(c.comercio).toBe("Líder");
    expect(c.moneda).toBe("CLP");
    expect(c.items).toEqual(["leche", "pan"]);
  });
});

describe("CompraSchema (rechazos)", () => {
  it("rechaza monto <= 0", () => {
    expect(() => parsearCompra(JSON.stringify({ ...base, monto: -5 }))).toThrow();
  });

  it("rechaza comercio de solo espacios", () => {
    expect(() => parsearCompra(JSON.stringify({ ...base, comercio: "   " }))).toThrow();
  });

  it("rechaza items vacío", () => {
    expect(() => parsearCompra(JSON.stringify({ ...base, items: [] }))).toThrow();
  });

  it("rechaza moneda desconocida", () => {
    expect(() => parsearCompra(JSON.stringify({ ...base, moneda: "EUR" }))).toThrow();
  });

  it("rechaza fecha no-ISO", () => {
    expect(() => parsearCompra(JSON.stringify({ ...base, fecha: "ayer" }))).toThrow();
  });

  it("rechaza campos alucinados (extra)", () => {
    expect(() => parsearCompra(JSON.stringify({ ...base, confianza: 0.99 }))).toThrow();
  });
});

// TODO(estudiante): añade un caso borde realista de un LLM.
// Ejemplo: monto "12.990" con separador de miles (Number("12.990") === 12.99,
// que NO es entero) debería ser rechazado por .int().
// it("rechaza monto con separador de miles", () => {
//   expect(() => parsearCompra(JSON.stringify({ ...base, monto: "12.990" }))).toThrow();
// });
