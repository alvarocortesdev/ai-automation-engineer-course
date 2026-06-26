/**
 * Ejercicio 1.9 — El patrón Result con discriminated unions (Primero-Sin-IA).
 *
 * Mismo parser de gastos que el ejercicio de Python, pero SIN lanzar: el fallo se
 * DEVUELVE como un valor tipado. Así el error queda en la firma —parte del contrato—
 * y el compilador obliga al llamador a discriminar antes de usar el `Gasto`.
 *
 * Formato de cada línea:  comercio;monto;categoria   (ej. "Lider;12990;supermercado")
 *
 * Tu trabajo: implementar `ok`, `err`, `parseGasto` y `safeJsonParse` (abajo).
 * Los TIPOS (Result, Gasto, ParseError) ya están dados: ese es el contrato.
 *
 * Correr los tests (sin instalar nada permanente):
 *     pnpm dlx vitest run          # o:  npx vitest run
 */

// ─────────────────────────────────────────────────────────────────────────────
//  Contrato (dado)
// ─────────────────────────────────────────────────────────────────────────────

/** O un éxito con `value`, o un fallo con `error`. Discriminados por el campo `ok`. */
export type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export type Gasto = { comercio: string; monto: number; categoria: string };

/** El error también es una discriminated union: distingue el TIPO de fallo. */
export type ParseError =
  | { tipo: "formato"; mensaje: string }
  | { tipo: "monto"; mensaje: string };

// ─────────────────────────────────────────────────────────────────────────────
//  Tu trabajo
// ─────────────────────────────────────────────────────────────────────────────

/** Construye un Result de éxito. El `never` lo hace asignable a cualquier Result<T, E>. */
export const ok = <T>(value: T): Result<T, never> => {
  // TODO(estudiante): devuelve el objeto de éxito.
  throw new Error("TODO: implementa ok()");
};

/** Construye un Result de fallo. */
export const err = <E>(error: E): Result<never, E> => {
  // TODO(estudiante): devuelve el objeto de fallo.
  throw new Error("TODO: implementa err()");
};

/**
 * Parsea UNA línea SIN lanzar: devuelve ok(Gasto) o err(ParseError).
 * Modos de fallo: campos != 3 o vacíos => tipo "formato"; monto no entero o <= 0 => tipo "monto".
 */
export function parseGasto(linea: string): Result<Gasto, ParseError> {
  // TODO(estudiante): valida con `return err({ tipo, mensaje })` temprano; ok({...}) al final.
  throw new Error("TODO: implementa parseGasto()");
}

/**
 * Envuelve `JSON.parse` (que SÍ lanza) en un Result. Nunca propaga el throw.
 * Recuerda: en strict, `catch (e)` tipa `e` como `unknown` -> estréchalo a Error.
 */
export function safeJsonParse(raw: string): Result<unknown, Error> {
  // TODO(estudiante): try { return ok(...) } catch (e) { return err(...) }
  throw new Error("TODO: implementa safeJsonParse()");
}
