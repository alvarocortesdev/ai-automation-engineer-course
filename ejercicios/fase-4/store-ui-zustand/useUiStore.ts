/**
 * Ejercicio 4.8 A — Store de UI con Zustand (persist + selectores atómicos).
 *
 * Implementa el store `useUiStore`. Respeta la firma exportada:
 * el corrector y los tests importan exactamente `useUiStore` y el tipo `UiState`.
 *
 * Reglas del ejercicio:
 *   - Forma currificada para TypeScript: create<UiState>()(...).
 *   - Actions INMUTABLES: nunca `push` ni mutación; crea arreglos/objetos nuevos.
 *       · setModelo(modelo): cambia modeloActivo.
 *       · alternarFavorito(modelo): toggle (lo agrega si no está, lo quita si está).
 *       · alternarTema(): alterna "claro" <-> "oscuro".
 *   - Envuelve el store en el middleware `persist`:
 *       · name: "ui-chat-storage"
 *       · storage: createJSONStorage(() => localStorage)
 *       · partialize: persiste SOLO `tema` y `modelosFavoritos`.
 *         `modeloActivo` es de sesión y NO debe persistirse.
 */

import { create } from "zustand";
// TODO: importa `persist` y `createJSONStorage` desde "zustand/middleware".

export type Tema = "claro" | "oscuro";

export interface UiState {
  modeloActivo: string;
  modelosFavoritos: string[];
  tema: Tema;
  // actions:
  setModelo: (modelo: string) => void;
  alternarFavorito: (modelo: string) => void;
  alternarTema: () => void;
}

// Estado inicial sugerido: modeloActivo "claude-haiku", modelosFavoritos [], tema "claro".
// TODO: envuelve este initializer en persist(initializer, { name, storage, partialize }).
export const useUiStore = create<UiState>()((set) => ({
  modeloActivo: "claude-haiku",
  modelosFavoritos: [],
  tema: "claro",

  // TODO (1): cambia modeloActivo.
  setModelo: (modelo) => set({}),

  // TODO (2): toggle inmutable de modelosFavoritos.
  alternarFavorito: (modelo) => set((state) => ({})),

  // TODO (3): alterna el tema.
  alternarTema: () => set((state) => ({})),
}));
