import { describe, it, expect } from "vitest";

import { aplicarEvento, crearProducto, esEventoSet } from "./inventario";

describe("aplicarEvento", () => {
  it("suma con add", () => {
    expect(aplicarEvento(10, { kind: "add", cantidad: 5 })).toBe(15);
  });

  it("resta con remove", () => {
    expect(aplicarEvento(10, { kind: "remove", cantidad: 4 })).toBe(6);
  });

  it("no baja de 0 con remove", () => {
    expect(aplicarEvento(3, { kind: "remove", cantidad: 9 })).toBe(0);
  });

  it("fija el stock con set", () => {
    expect(aplicarEvento(10, { kind: "set", valor: 2 })).toBe(2);
  });
});

describe("crearProducto", () => {
  it("asigna el id y conserva los datos", () => {
    const p = crearProducto({ nombre: "Leche", stock: 12, categoria: "fresco" }, 7);
    expect(p).toEqual({ id: 7, nombre: "Leche", stock: 12, categoria: "fresco" });
  });
});

describe("esEventoSet (type guard)", () => {
  it("true para set", () => {
    expect(esEventoSet({ kind: "set", valor: 1 })).toBe(true);
  });

  it("false para add", () => {
    expect(esEventoSet({ kind: "add", cantidad: 1 })).toBe(false);
  });
});

// TODO(estudiante): añade aquí al menos un caso borde tuyo.
// Ejemplo: un `add` con cantidad 0 no debería cambiar el stock.
// it("add con cantidad 0 no cambia el stock", () => {
//   expect(aplicarEvento(5, { kind: "add", cantidad: 0 })).toBe(5);
// });
