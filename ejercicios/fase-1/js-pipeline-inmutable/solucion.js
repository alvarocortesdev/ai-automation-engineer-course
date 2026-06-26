/**
 * Starter del ejercicio — Primero-Sin-IA.
 *
 * Implementa las TRES funciones a mano, sin IA. NO cambies las firmas (nombres
 * ni parámetros): los tests de `solucion.test.js` dependen de ellas.
 *
 * Regla de oro: ninguna de estas funciones debe MUTAR el array `pedidos` ni los
 * objetos que contiene. Cada una devuelve datos NUEVOS (un array nuevo o un
 * número). Usa filter / map / reduce, destructuring y spread — no bucles `for`
 * con `.push()` a una variable externa.
 *
 * Lee la sección 4.3 y 4.4 de la lección (1.7 JavaScript moderno) si te trabas.
 *
 * Forma de un pedido:
 *   { id: number, cliente: string, total: number, pagado: boolean }
 */

/**
 * Devuelve un array NUEVO solo con los pedidos cuyo `pagado` es true.
 * @param {Array<{id:number, cliente:string, total:number, pagado:boolean}>} pedidos
 * @returns {Array<object>}
 */
export function pagados(pedidos) {
  throw new Error("Implementa pagados a mano, sin IA.");
}

/**
 * Devuelve un array NUEVO donde cada pedido tiene un campo extra
 * `totalConIva = total * (1 + tasa)`, SIN mutar los objetos originales (usa spread).
 * @param {Array<object>} pedidos
 * @param {number} tasa  ej. 0.19
 * @returns {Array<object>}
 */
export function conIva(pedidos, tasa) {
  throw new Error("Implementa conIva a mano, sin IA.");
}

/**
 * Suma con `reduce` el `total` de los pedidos PAGADOS. Devuelve un solo número.
 * @param {Array<object>} pedidos
 * @returns {number}
 */
export function totalRecaudado(pedidos) {
  throw new Error("Implementa totalRecaudado a mano, sin IA.");
}
