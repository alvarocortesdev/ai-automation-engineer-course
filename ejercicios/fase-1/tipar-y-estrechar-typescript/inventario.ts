/**
 * Ejercicio 1.8 A — Tipar y estrechar (Primero-Sin-IA).
 *
 * Reglas:
 *  - Reemplaza TODOS los `any` por tipos correctos. No debe quedar ningún `any`.
 *  - `npm run typecheck` (tsc --strict) en verde Y `npm test` (vitest) en verde.
 *  - No cambies los nombres ni la cantidad de parámetros de las funciones exportadas:
 *    los tests dependen de ellos.
 */

// 1) Modela el producto de la despensa. (Pista: una `interface`.)
//    Campos: id (number), nombre (string), stock (number),
//    categoria (solo "fresco" | "seco" | "congelado").
export interface Producto {
  // TODO
}

// 2) Modela los eventos de stock como UNIÓN DISCRIMINADA (campo discriminante `kind`):
//    - { kind: "add";    cantidad: number }  → suma `cantidad` al stock
//    - { kind: "remove"; cantidad: number }  → resta `cantidad` (sin bajar de 0)
//    - { kind: "set";    valor: number }     → fija el stock a `valor`
export type EventoStock = any; // TODO: reemplaza por la unión discriminada

// 3) Aplica un evento al stock actual. Estrecha por `kind` con un `switch`.
//    En el `default`, incluye el chequeo de exhaustividad con `never`.
export function aplicarEvento(stockActual: number, evento: EventoStock): number {
  throw new Error("TODO: implementar con switch + narrowing + never");
}

// 4) Crea un producto a partir de los datos SIN id (usa un utility type, no copies los campos).
export function crearProducto(
  datos: any /* TODO: Omit<Producto, "id"> */,
  id: number,
): Producto {
  throw new Error("TODO: implementar con Omit<Producto, 'id'>");
}

// 5) Type guard: ¿este evento fija el stock ("set")?
//    Debe tener la firma de predicado de tipo: `evento is ...`
export function esEventoSet(evento: EventoStock): boolean /* TODO: predicado `evento is ...` */ {
  throw new Error("TODO: implementar como type guard");
}
