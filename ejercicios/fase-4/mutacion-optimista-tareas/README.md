# Ejercicio 4.7 A — useToggleTarea con optimistic update y rollback

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.7` Estado y datos (TanStack Query, RHF + zod)
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 45 min

## 🎯 Objetivo

Implementar un custom hook `useToggleTarea` con **TanStack Query v5** que marque/desmarque una tarea como hecha usando el patrón completo de **optimistic update**: actualizar la caché al instante, **revertir (rollback)** si el servidor falla, e **invalidar** al terminar para reconciliar con el servidor. El hook recibe la función de API por configuración (`toggleApi`) para poder testearlo con una API falsa.

## 📋 Contexto

Este es el patrón que hace que una app "se sienta rápida": en el **Capstone F4**, enviar un mensaje de chat aparece al instante en la lista y se revierte con un aviso si el backend falla. Es exactamente este hook, aplicado a mensajes en vez de tareas. Si lo dominas (incluido el rollback, que casi nadie implementa bien), tienes el músculo central del manejo de server state.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial**: <https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates>.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el hook.
4. Mañana, **reconstrúyelo de memoria**. Si te falta `cancelQueries` o el snapshot, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `useToggleTarea.ts`. Implementa el hook respetando la firma exportada (no cambies el nombre ni los exports `TAREAS_KEY` / `Tarea`).
2. Instala dependencias y corre los tests:

   ```bash
   pnpm install
   pnpm test
   ```

3. Itera hasta que **todos los tests pasen en verde**, incluido el de **rollback** (el que fuerza un fallo de la API).
4. Añade al menos **un test propio** en `useToggleTarea.test.tsx` (idea: una promesa controlada para verificar que la caché muestra el cambio **antes** de que la API responda).

> Los tests verifican el efecto sobre la **caché** (volteo en éxito, restauración en fallo). No pueden ver tu código por dentro: el corrector revisa con la rúbrica que uses el patrón completo (cancelar, snapshot, inmutable, invalidar) y que lo entiendas.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `useMutation` con `mutationFn: toggleApi`.
- [ ] `onMutate`: `cancelQueries` de `["tareas"]` → snapshot con `getQueryData` → `setQueryData` **inmutable** (voltea `hecha` de la tarea con ese `id`) → `return { previas }`.
- [ ] `onError`: restaura el snapshot (`setQueryData(TAREAS_KEY, contexto.previas)`).
- [ ] `onSettled`: `invalidateQueries({ queryKey: ["tareas"] })`.
- [ ] **No mutas la caché en sitio** (usas `map` + spread, no `push`/asignación).
- [ ] Todos los tests pasan (éxito **y** rollback) y agregaste un test propio.
- [ ] Puedes **explicar sin notas** por qué `cancelQueries` es necesario y qué pasaría sin el snapshot.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Dentro del hook: `const queryClient = useQueryClient()`. En `onMutate(id)` el orden es:
`await queryClient.cancelQueries({ queryKey: [...TAREAS_KEY] })` →
`const previas = queryClient.getQueryData<Tarea[]>([...TAREAS_KEY])` →
`queryClient.setQueryData<Tarea[]>([...TAREAS_KEY], (viejas) => (viejas ?? []).map(t => t.id === id ? { ...t, hecha: !t.hecha } : t))` →
`return { previas }`.
En `onError(_e, _id, contexto)`: `if (contexto?.previas) queryClient.setQueryData([...TAREAS_KEY], contexto.previas)`.
En `onSettled`: `queryClient.invalidateQueries({ queryKey: [...TAREAS_KEY] })`.
Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/mutacion-optimista-tareas/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/mutacion-optimista-tareas.md` — no la mires antes de intentarlo de verdad.
