/**
 * Tests del ejercicio — corre con el test runner integrado de Node (sin instalar nada):
 *
 *   node --test
 *
 * La gracia: `fetchFn` está INYECTADO. Aquí pasamos funciones falsas que devuelven
 * la respuesta que queremos (o que rechazan). NUNCA se toca la red.
 * Añade al menos un caso borde tuyo al final.
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import {
  obtenerNombreUsuario,
  EntradaInvalida,
  ServicioInalcanzable,
  UsuarioNoEncontrado,
  ServicioCaido,
  RespuestaInesperada,
} from "./solucion.js";

// fetchFn falso: RESUELVE con una respuesta del status y payload dados.
// Imita que fetch NO rechaza por un status de error: 404/500 también resuelven.
const responde = (status, payload = {}) => async (_userId) => ({
  status,
  json: async () => payload,
});

// fetchFn falso que RECHAZA, simulando un fallo de red (sin respuesta).
const redCaida = () => async (_userId) => {
  throw new Error("ECONNREFUSED: la red falló");
};

// fetchFn que NO debe ser llamado: si la validación de input es correcta,
// nunca se ejecuta. Si se ejecuta, el test falla con un mensaje claro.
const noDebeCorrer = () => async () => {
  throw new Error("fetchFn no debía llamarse: el input inválido se valida ANTES de la red");
};

test("status 200 devuelve el nombre (doble await)", async () => {
  const r = await obtenerNombreUsuario(7, responde(200, { name: "Grace Hopper" }));
  assert.equal(r, "Grace Hopper");
});

test("userId inválido lanza EntradaInvalida ANTES de llamar fetchFn", async () => {
  await assert.rejects(() => obtenerNombreUsuario(0, noDebeCorrer()), EntradaInvalida);
  await assert.rejects(() => obtenerNombreUsuario(-3, noDebeCorrer()), EntradaInvalida);
  await assert.rejects(() => obtenerNombreUsuario(1.5, noDebeCorrer()), EntradaInvalida);
});

test("error de red (fetchFn rechaza) se convierte en ServicioInalcanzable", async () => {
  await assert.rejects(() => obtenerNombreUsuario(7, redCaida()), ServicioInalcanzable);
});

test("status 404 lanza UsuarioNoEncontrado", async () => {
  await assert.rejects(() => obtenerNombreUsuario(7, responde(404)), UsuarioNoEncontrado);
});

test("status 500 lanza ServicioCaido", async () => {
  await assert.rejects(() => obtenerNombreUsuario(7, responde(500)), ServicioCaido);
});

test("status 503 (>= 500) lanza ServicioCaido", async () => {
  await assert.rejects(() => obtenerNombreUsuario(7, responde(503)), ServicioCaido);
});

test("status raro (418) lanza RespuestaInesperada", async () => {
  await assert.rejects(() => obtenerNombreUsuario(7, responde(418)), RespuestaInesperada);
});

// TODO(estudiante): añade aquí al menos un caso borde tuyo.
// Ideas: status 301 (redirección) → ¿RespuestaInesperada? · un 200 cuyo payload no trae `name`.
// test("mi caso borde", async () => { ... });
