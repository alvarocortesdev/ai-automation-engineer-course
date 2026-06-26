/**
 * Ejercicio 1.8 B — Validar la salida de un LLM con zod (Primero-Sin-IA).
 *
 * Un LLM extrajo una compra desde un correo y devolvió este JSON. NO confíes en él.
 * Diseña el schema que lo valide EN LA FRONTERA.
 *
 * Reglas del schema (los seis campos):
 *   - comercio:  string, NO vacío ni de solo espacios.
 *   - monto:     entero positivo; debe COACCIONAR "12990" (string) a 12990 (number).
 *   - moneda:    solo "CLP" o "USD".
 *   - categoria: string, NO vacío ni de solo espacios.
 *   - fecha:     string con formato ISO de fecha (YYYY-MM-DD).
 *   - items:     array de strings (no vacíos) con al menos 1 elemento.
 *   - RECHAZA cualquier campo alucinado (extra) que el LLM pueda inventar.
 *
 * Pista de la lección (4.8): `z.object` IGNORA los campos extra. Para rechazarlos,
 * necesitas otra forma de objeto. Empieza con `z.object` y deja que el test de
 * "campos alucinados" te diga que tienes que cambiarla.
 */
import { z } from "zod";

export const CompraSchema = z.object({
  // TODO: define los seis campos con sus constraints.
});

// El tipo Compra se INFIERE del schema. No lo escribas a mano.
export type Compra = z.infer<typeof CompraSchema>;

/** Parsea el JSON crudo Y lo valida en una sola función. Lanza si es inválido. */
export function parsearCompra(rawJson: string): Compra {
  throw new Error("TODO: JSON.parse(rawJson) + validación con zod");
}
