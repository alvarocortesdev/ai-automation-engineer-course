// Tu suite va AQUÍ. El SUT (`solucion.ts`) ya funciona; no lo toques.
//
// Objetivo: (a) `it.each` con emails válidos e inválidos (incluye bordes), (b)
// verificar que `registrar` llama a `logger.warn` SOLO cuando el email es
// inválido, usando `vi.fn()`, y (c) afirmar el valor de retorno de `registrar`.
//
// Corre con pnpm (nunca npm):
//     pnpm install      # una sola vez
//     pnpm test

import { describe, it, expect, vi } from "vitest";
import { esEmailValido, normalizarEmail, registrar } from "./solucion";

describe("esEmailValido", () => {
  it.each([
    // TODO: completa la tabla. Incluye al menos 3 válidos y 3 inválidos, con
    //       bordes: espacios alrededor, MAYÚSCULAS, "a@b" sin punto, dominio
    //       que termina en punto, "@dominio.com" sin parte local.
    // { entrada: " A@B.com ", esperado: true },
  ])("$entrada -> $esperado", ({ entrada, esperado }) => {
    expect(esEmailValido(entrada)).toBe(esperado);
  });
});

describe("registrar", () => {
  it("devuelve el email normalizado y NO avisa cuando es válido", () => {
    const logger = { warn: vi.fn() };
    // TODO: llama a registrar con un email válido (p. ej. " A@B.com ").
    //       Afirma el retorno normalizado y que logger.warn NO se llamó.
  });

  it("devuelve null y avisa cuando es inválido", () => {
    const logger = { warn: vi.fn() };
    // TODO: llama a registrar con un email inválido (p. ej. "sin-arroba").
    //       Afirma que devuelve null y que logger.warn se llamó (toHaveBeenCalled).
  });
});
