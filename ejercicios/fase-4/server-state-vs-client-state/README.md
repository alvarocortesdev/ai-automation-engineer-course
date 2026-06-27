# Ejercicio 4.7 B — Diagnostica y diseña la capa de datos (server vs client)

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.7` Estado y datos (TanStack Query, RHF + zod)
**Ruta:** crítica · **Modalidad:** razonamiento / diseño (sin código) · **Timebox:** 35 min

## 🎯 Objetivo

Clasificar cada pieza de estado de un componente real como **server state** o **client state**, nombrar los **cinco déficits** del enfoque "fetch en `useEffect`" y emparejar cada uno con el mecanismo de TanStack Query que lo resuelve, y **diseñar por escrito** la capa de datos (queries, mutaciones, invalidación) que reemplazaría ese componente. Es la conversación de arquitectura que tendrías en una entrevista de frontend, antes de escribir una sola línea.

## 📋 Contexto

La lección insiste en que, una vez tienes clara la distinción server vs client, las herramientas son detalles. Este ejercicio entrena ese músculo conceptual sin que escribas código: si diseñas bien la capa de datos en papel, implementarla con TanStack Query es mecánico. Alimenta directo al **Capstone F4**, donde tendrás que decidir qué es query, qué es mutación y qué se queda en `useState`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Lee `componente-buggy.md` y `spec-api.md`, y razona en tu documento. **Sin IA.**
2. Solo entonces, consulta la **documentación oficial**: <https://tanstack.com/query/latest/docs/framework/react/overview>.
3. **Solo al final**, usa IA para *revisar y cuestionar* tu diseño —no para *generártelo*.
4. Mañana, explícale a alguien (o al espejo) la diferencia server vs client en menos de un minuto. Si no te sale, no lo aprendiste.

## 🛠️ Instrucciones

1. Lee `componente-buggy.md` (el componente `PanelTareas` a diagnosticar) y `spec-api.md` (los endpoints del backend de la Fase 3).
2. Escribe tu análisis en `diseno-datos.md` (ya tiene la estructura con los huecos a completar). **No escribes código de implementación**: es un documento de diseño.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **Tabla de clasificación**: cada pieza de estado del componente clasificada como server o client, con una línea de justificación.
- [ ] **Los cinco problemas**: nombras los cinco déficits del `fetch`-en-`useEffect` y, para cada uno, el mecanismo concreto de TanStack Query que lo resuelve.
- [ ] **Diseño de la capa**: defines las `queryKey`, qué es `useQuery` y qué es `useMutation`, y describes el **flujo de invalidación** tras crear una tarea.
- [ ] **Decisión de optimistic**: para "marcar tarea como hecha", argumentas optimistic vs solo `invalidateQueries` y nombras el trade-off.
- [ ] **Nota de seguridad**: una línea sobre por qué validar con zod en el cliente no exime al backend.
- [ ] Puedes **defender tu diseño sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para clasificar cada pieza pregúntate: *¿el dueño de este dato es el servidor o mi UI?* La lista de tareas y la info de cada tarea vienen de la DB → **server state**. El texto del input, qué fila está expandida, si un modal está abierto → **client state**. Para los cinco problemas, relee la sección 4.2 de la lección punto por punto y empareja con las herramientas de 4.3–4.6 (caché/queryKey, cancelQueries, retry/refetch, invalidateQueries, fin del boilerplate). Para el trade-off de optimistic: rápido vs simple-y-siempre-correcto. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/server-state-vs-client-state/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/server-state-vs-client-state.md` — no la mires antes de intentarlo de verdad.
