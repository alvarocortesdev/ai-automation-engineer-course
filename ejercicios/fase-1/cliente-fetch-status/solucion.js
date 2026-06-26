/**
 * Starter del ejercicio — Primero-Sin-IA.
 *
 * Implementa `obtenerNombreUsuario` a mano, sin IA. NO cambies las firmas ni los
 * nombres de las clases de error: los tests de `solucion.test.js` dependen de ellos.
 *
 * El corazón del ejercicio NO es "llamar fetch" (no se llama el fetch real): es
 *   1) validar el input ANTES de gastar una petición,
 *   2) separar el error de RED (la promesa rechaza) del status de error (la promesa
 *      RESUELVE con un status malo — fetch no rechaza por 404/500), y
 *   3) usar el DOBLE await (la respuesta, y luego .json()).
 *
 * `fetchFn` está INYECTADO: tus tests pasan una función falsa, sin tocar la red.
 *
 * Lee la sección 4.6 de la lección (1.7 JavaScript moderno) si te trabas.
 */

// Errores de dominio (ya definidos — úsalos donde el contrato lo pide).
export class EntradaInvalida extends Error {}
export class ServicioInalcanzable extends Error {}
export class UsuarioNoEncontrado extends Error {}
export class ServicioCaido extends Error {}
export class RespuestaInesperada extends Error {}

/**
 * Devuelve el nombre del usuario, manejando todos los modos de fallo.
 *
 * Contrato:
 *   - userId inválido (≤ 0 o no entero) → lanza EntradaInvalida ANTES de llamar fetchFn.
 *   - fetchFn RECHAZA (error de red simulado) → lanza ServicioInalcanzable.
 *   - status 200 → devuelve (await resp.json()).name
 *   - status 404 → lanza UsuarioNoEncontrado
 *   - status >= 500 → lanza ServicioCaido
 *   - cualquier otro status → lanza RespuestaInesperada
 *
 * @param {number} userId
 * @param {(userId:number) => Promise<{status:number, json:() => Promise<any>}>} fetchFn
 *        función inyectada que simula fetch. Devuelve una promesa de un objeto con
 *        `.status` (number) y `.json()` (async). Puede RECHAZAR (error de red).
 * @returns {Promise<string>}
 */
export async function obtenerNombreUsuario(userId, fetchFn) {
  throw new Error("Implementa esta función a mano, sin IA.");
}
