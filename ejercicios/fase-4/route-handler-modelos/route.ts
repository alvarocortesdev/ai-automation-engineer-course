/**
 * Ejercicio 4.6 A — Route Handler con validación de entrada.
 *
 * En un proyecto Next.js real, este archivo vive en `app/api/modelos/route.ts`
 * y atiende GET /api/modelos. Lo tipamos con la `Request`/`Response` web estándar
 * (que Next.js soporta) para que corra y se pruebe SIN levantar Next.js.
 *
 * Implementa `GET` según el contrato (los tests lo verifican):
 *
 *   ?q=        (opcional) filtra por substring CASE-INSENSITIVE contra nombre O proveedor.
 *              Sin q (o vacío) no filtra. Si q tiene más de 64 caracteres → 400.
 *   ?limit=    (opcional, default 10) entero >= 1. Si no es entero >= 1 → 400.
 *              Si supera 50, se ACOTA a 50 (no es error).
 *
 *   Éxito (200): Response.json({ query, count, items })
 *                - query: el q usado (string, "" si no vino)
 *                - count: cantidad de items DEVUELTOS
 *                - items: el arreglo de modelos filtrado y acotado por limit
 *   Entrada inválida (400): Response.json({ error }, { status: 400 })
 */

import { MODELOS } from "./datos";

export async function GET(request: Request): Promise<Response> {
  // TODO 1: lee los query params desde new URL(request.url).searchParams
  // TODO 2: valida q (largo) y limit (entero >= 1) → 400 ante entrada inválida
  // TODO 3: filtra MODELOS por q (case-insensitive, nombre O proveedor)
  // TODO 4: acota por limit (clamp a 50) y responde { query, count, items }
  return Response.json({ query: "", count: 0, items: [] });
}
