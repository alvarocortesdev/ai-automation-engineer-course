// Ejercicio 2.6 — Suite Vitest para un validador (SUT).
//
// Este módulo es el "system under test". NO lo modifiques: tu trabajo es escribir
// la suite en `solucion.test.ts`.
//
// - `normalizarEmail` y `esEmailValido` son LÓGICA PURA: NO se mockean.
// - `registrar` usa un `logger` inyectado (en producción escribiría a un archivo
//   o a un servicio de observabilidad): esa es la FRONTERA. En tus tests, el
//   logger se reemplaza por un doble (`vi.fn()`).

export interface Logger {
  warn(msg: string): void;
}

export function normalizarEmail(raw: string): string {
  return raw.trim().toLowerCase();
}

export function esEmailValido(raw: string): boolean {
  const email = normalizarEmail(raw);
  const at = email.indexOf("@");
  if (at <= 0) return false; // sin "@", o "@" al inicio (parte local vacía)
  const dominio = email.slice(at + 1);
  if (!dominio.includes(".")) return false; // el dominio necesita un punto
  if (dominio.startsWith(".") || dominio.endsWith(".")) return false;
  return true;
}

export function registrar(raw: string, logger: Logger): string | null {
  if (!esEmailValido(raw)) {
    logger.warn(`email inválido: ${raw}`);
    return null;
  }
  return normalizarEmail(raw);
}
