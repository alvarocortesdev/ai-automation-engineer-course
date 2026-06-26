/**
 * Lógica de dominio de la despensa (sin HTTP).
 *
 * Completa los TODO. NO cambies las firmas públicas: los tests de `pantry.test.ts`
 * dependen de ellas.
 */

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { z } from "zod";

// TODO (1.8): define el esquema zod de un ítem NUEVO (sin id):
//   - name: string NO vacío        -> z.string().min(1)
//   - quantity: número > 0          -> z.number().positive()
//   - unit: string NO vacío         -> z.string().min(1)
export const NewItemSchema = z.object({
  // ...completa los campos
});

// `z.infer` deriva el tipo TypeScript del esquema: no repites la forma dos veces.
export type NewItem = z.infer<typeof NewItemSchema>;
export type Item = NewItem & { id: number };

export class PantryStore {
  constructor(private readonly path: string) {
    // TODO (1.5): si el archivo no existe, créalo con "[]".
    throw new Error("TODO: implementa el constructor");
  }

  list(): Item[] {
    // TODO: lee el archivo JSON y devuelve la lista de ítems.
    throw new Error("TODO: list");
  }

  add(data: unknown): Item {
    // TODO:
    //   1) valida `data` con NewItemSchema.parse(data) (lanza ZodError si no valida),
    //   2) calcula el próximo id = max(ids, 0) + 1,
    //   3) construye el Item, persístelo y devuélvelo.
    throw new Error("TODO: add");
  }

  get(id: number): Item | undefined {
    // TODO: devuelve el ítem con ese id, o undefined si no existe.
    throw new Error("TODO: get");
  }

  remove(id: number): boolean {
    // TODO: borra el ítem con ese id. Devuelve true si borró, false si no existía.
    throw new Error("TODO: remove");
  }
}
