# Ejercicio 4.8 A — Store de UI con Zustand (persist + selectores atómicos)

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.8` Estado global (Zustand)
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 40 min

## 🎯 Objetivo

Implementar `useUiStore`, el estado global de cliente de una app de chat con IA, en **Zustand v5 + TypeScript**: con la forma currificada `create<UiState>()(...)`, **actions inmutables**, y el middleware `persist` con `partialize` que guarda **solo** lo que debe sobrevivir a una recarga. La decisión que este ejercicio te obliga a tomar bien: **qué persistir y qué no** (`modeloActivo` es de sesión, no se persiste; un token jamás iría aquí).

## 📋 Contexto

Este es el estado global de cliente del **Capstone F4** (frontend de una app de IA): tema, modelo activo y favoritos, leídos por componentes lejanos. Los mensajes y conversaciones NO van aquí (son server state, los maneja TanStack Query). Si dominas el store con selectores atómicos y `partialize` correcto, tienes el patrón de estado global que usarás en todo proyecto React.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** de Zustand: <https://zustand.docs.pmnd.rs/> y la guía de [persist](https://zustand.docs.pmnd.rs/integrations/persisting-store-data).
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el store.
4. Mañana, **reconstrúyelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `useUiStore.ts`. Implementa el store respetando la firma exportada (no cambies el nombre `useUiStore` ni el tipo `UiState`).
2. Instala dependencias y corre los tests:

   ```bash
   pnpm install
   pnpm test
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test propio** en `useUiStore.test.tsx` (un caso borde que se te ocurra: dos favoritos distintos, persistir tras varias acciones, etc.).

> Los tests validan el **comportamiento** (actions, inmutabilidad, lectura por selector, `partialize`), pero no pueden ver si destructuras el store entero o si un selector devuelve un objeto nuevo. El espíritu del ejercicio es el **método**: selectores atómicos y persistir solo lo duradero. La corrección con IA revisa eso.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El store usa la forma currificada `create<UiState>()(...)` y exporta `useUiStore` y `UiState`.
- [ ] `setModelo` cambia `modeloActivo`; `alternarTema` alterna `"claro"`/`"oscuro"`.
- [ ] `alternarFavorito` hace toggle creando **arreglos nuevos** (sin `push`, sin mutar).
- [ ] El store está envuelto en `persist` con `name: "ui-chat-storage"` y `createJSONStorage(() => localStorage)`.
- [ ] `partialize` persiste **solo** `tema` y `modelosFavoritos`; **no** `modeloActivo`.
- [ ] Un componente lee el modelo con un **selector atómico** (`useUiStore(s => s.modeloActivo)`).
- [ ] Todos los tests pasan y agregaste un test propio.
- [ ] Puedes **explicar sin notas** por qué `modeloActivo` no se persiste y por qué un token nunca va en `localStorage`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El esqueleto: `create<UiState>()(persist((set) => ({ ...estado, ...actions }), { name, storage, partialize }))`.
Las actions de toggle usan `set((state) => ({ ... }))` y deciden con `state.modelosFavoritos.includes(modelo)`
entre `state.modelosFavoritos.filter((m) => m !== modelo)` (quitar) y `[...state.modelosFavoritos, modelo]`
(agregar). El `partialize` recibe el estado y devuelve un objeto SOLO con lo que persiste:
`(state) => ({ tema: state.tema, modelosFavoritos: state.modelosFavoritos })`. Importa `persist` y
`createJSONStorage` desde `"zustand/middleware"`. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/store-ui-zustand/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/store-ui-zustand.md` — no la mires antes de intentarlo de verdad.
