/**
 * Tests del ejercicio — corre con el test runner integrado de Node (sin instalar nada):
 *
 *   node --test
 *
 * Estos tests definen el contrato. Verifican DOS cosas: que el resultado es
 * correcto y que el array original NO se mutó (el corazón del ejercicio).
 * Añade al menos un caso borde tuyo al final.
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import { pagados, conIva, totalRecaudado } from "./solucion.js";

// Fábrica: devuelve un fixture FRESCO en cada test (evita que un test contamine a otro).
const fixture = () => [
  { id: 1, cliente: "ada", total: 1200, pagado: true },
  { id: 2, cliente: "linus", total: 800, pagado: false },
  { id: 3, cliente: "grace", total: 1500, pagado: true },
];

// Comparación tolerante a floats (1200 * 1.19 puede no ser exacto en binario).
const cerca = (a, b) => Math.abs(a - b) < 1e-9;

test("pagados devuelve solo los pedidos pagados", () => {
  const r = pagados(fixture());
  assert.deepEqual(r.map((p) => p.id), [1, 3]);
});

test("pagados NO muta el array original", () => {
  const original = fixture();
  const copia = structuredClone(original);
  pagados(original);
  assert.deepEqual(original, copia);
});

test("conIva agrega totalConIva = total * (1 + tasa)", () => {
  const r = conIva(fixture(), 0.19);
  assert.ok(cerca(r[0].totalConIva, 1200 * 1.19), `esperaba ~1428, vino ${r[0].totalConIva}`);
  assert.ok(cerca(r[1].totalConIva, 800 * 1.19), `esperaba ~952, vino ${r[1].totalConIva}`);
});

test("conIva NO muta los objetos originales", () => {
  const original = fixture();
  const copia = structuredClone(original);
  conIva(original, 0.19);
  assert.equal("totalConIva" in original[0], false); // el objeto original quedó intacto
  assert.deepEqual(original, copia);
});

test("totalRecaudado suma SOLO los pagados", () => {
  assert.equal(totalRecaudado(fixture()), 1200 + 1500); // 800 no está pagado
});

test("totalRecaudado de una lista vacía es 0", () => {
  assert.equal(totalRecaudado([]), 0);
});

// TODO(estudiante): añade aquí al menos un caso borde tuyo.
// Ideas: ¿qué pasa si NINGÚN pedido está pagado? ¿si tasa es 0?
// test("mi caso borde", () => { ... });
