---
ejercicio_id: fase-4/store-ui-zustand
fase: fase-4
sub_unidad: "4.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Store de UI con Zustand

## Respuesta canónica

```ts
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export type Tema = "claro" | "oscuro";

export interface UiState {
  modeloActivo: string;
  modelosFavoritos: string[];
  tema: Tema;
  setModelo: (modelo: string) => void;
  alternarFavorito: (modelo: string) => void;
  alternarTema: () => void;
}

export const useUiStore = create<UiState>()(
  persist(
    (set) => ({
      modeloActivo: "claude-haiku",
      modelosFavoritos: [],
      tema: "claro",

      setModelo: (modelo) => set({ modeloActivo: modelo }),

      alternarFavorito: (modelo) =>
        set((state) => ({
          modelosFavoritos: state.modelosFavoritos.includes(modelo)
            ? state.modelosFavoritos.filter((m) => m !== modelo)
            : [...state.modelosFavoritos, modelo],
        })),

      alternarTema: () =>
        set((state) => ({ tema: state.tema === "claro" ? "oscuro" : "claro" })),
    }),
    {
      name: "ui-chat-storage",
      storage: createJSONStorage(() => localStorage),
      // Persistimos SOLO preferencias duraderas. modeloActivo es de sesión.
      partialize: (state) => ({
        tema: state.tema,
        modelosFavoritos: state.modelosFavoritos,
      }),
    },
  ),
);
```

Y la lectura desde un componente (lo que prueba el test de re-render):

```tsx
function VistaModelo() {
  const modelo = useUiStore((s) => s.modeloActivo);   // selector atómico
  const setModelo = useUiStore((s) => s.setModelo);
  return (
    <div>
      <p>Modelo: {modelo}</p>
      <button onClick={() => setModelo("gpt-4o-mini")}>Cambiar</button>
    </div>
  );
}
```

## Razonamiento paso a paso
- **Forma currificada `create<UiState>()(...)`:** el segundo par de paréntesis es la peculiaridad de Zustand para que TypeScript infiera bien con middlewares. Sin ella, los tipos pelean con `persist`.
- **Actions inmutables:** `alternarFavorito` decide con `includes` entre `filter` (quitar) y spread `[...]` (agregar); **nunca** `push`. `set` con función recibe el estado más reciente; `set` con objeto hace merge superficial.
- **`persist` + `partialize` (el corazón):** `partialize` devuelve un objeto solo con `tema` y `modelosFavoritos`. Por eso el blob en `localStorage` **no** contiene `modeloActivo` (lo verifica el test). Decisión de producto **y** de seguridad: no guardamos basura transitoria ni —jamás— secretos.
- **Selector atómico:** `useUiStore(s => s.modeloActivo)` re-renderiza el componente solo si ese campo cambia; el test de re-render lo confirma con el click.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Persistir el estado entero:** si el alumno omite `partialize`, `persist` guarda todo (incluido `modeloActivo`) y el test `partialize` falla (`modeloActivo` no es `undefined`). Es exactamente el error que la lección combate.
2. **Mutación:** `state.modelosFavoritos.push(modelo)` y luego `set({ modelosFavoritos: state.modelosFavoritos })` muta la referencia; el test "NO muta: crea un arreglo nuevo" (`not.toBe(antes)`) lo atrapa. Aunque pasara, es C1 en-progreso.
3. **Destructurar el store entero** en el componente (`const { modeloActivo } = useUiStore()`): los tests no lo ven (el componente igual funciona), pero es C3-incompleto. Hay que abrir el archivo.
4. **Selector que devuelve objeto sin `useShallow`:** no aparece en este ejercicio porque solo se lee un campo por selector, pero si el alumno "optimiza" devolviendo `{ modelo, setModelo }` desde un solo selector, márcalo (re-render en bucle en v5).
5. **Firma:** si cambió el nombre del export o del tipo, los tests fallan al importar; pídele restaurar la firma antes de evaluar.

## Rango de soluciones aceptables
- `storage` omitido (por defecto `persist` usa `localStorage`): aceptable, pero el ejercicio pide declararlo con `createJSONStorage(() => localStorage)`; mencionarlo, no penalizar fuerte.
- Estado inicial con otros nombres de modelo (`"gpt-4o"`, etc.): válido mientras el toggle y el tipo sean correctos y los tests pasen (el test resetea a `"claude-haiku"` en `beforeEach`, así que el inicial del alumno no afecta los asserts).
- Tipar el initializer con `(set, get)` aunque no use `get`: válido.
- Usar `immer` middleware para escribir `state.modelosFavoritos.push(...)` de forma "mutante pero segura": **aceptable** (immer produce inmutabilidad por debajo); el corrector debe notar que es sofisticación opcional y que el alumno debe saber explicar por qué ahí sí se puede "mutar".
- Agrupar las actions bajo una clave `actions: {...}`: válido como patrón, pero entonces el test (que llama `getState().setModelo`) fallaría; con la firma plana del enunciado es lo esperado.
