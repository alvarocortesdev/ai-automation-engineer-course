# Ejercicio 4.11 A — chatReducer: la máquina de estados de un chat de IA

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.11` UI para apps de IA
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 45 min

## 🎯 Objetivo

Implementar un reducer **puro** `chatReducer(state, accion)` que modele el estado de un chat de IA con streaming: **optimistic UI** (el mensaje del usuario aparece al instante), un mensaje de asistente que **crece chunk por chunk**, y los caminos de **error** y **cancelación**. Es —en esencia— lo que `useChat` del Vercel AI SDK hace por dentro (sección 4.5 de la lección). Construirlo a mano es entender la UI de IA de raíz. TypeScript puro, sin React ni el SDK.

## 📋 Contexto

En el **Capstone F4** la conversación es exactamente esta máquina de estados: el mensaje del usuario aparece ya, la respuesta del asistente crece token a token, y un fallo de red no borra lo que el usuario estaba leyendo. Si dominas el reducer (incluidos `ERROR` y `CANCELAR`, que casi nadie maneja bien), tienes el músculo central de la UI de IA.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial**: <https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat>.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el reducer.
4. Mañana, **reconstrúyelo de memoria**. Si mutas el último mensaje en sitio o pierdes el guard, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `chatReducer.ts`. Implementa la función respetando las firmas y tipos exportados (no cambies los nombres ni los exports `chatReducer` / `estadoInicial` / `ChatState` / `Accion` / `Mensaje`).
2. Instala dependencias y corre los tests:

   ```bash
   pnpm install
   pnpm test
   ```

3. Itera hasta que **todos los tests pasen en verde**, incluidos los de `ERROR` (conserva el parcial) y de **inmutabilidad** (no muta la entrada).
4. Añade al menos **un test propio** en `chatReducer.test.ts` (idea: dos preguntas seguidas y verificar que el historial acumula los cuatro mensajes en orden).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `ENVIAR`: añade **dos** mensajes (usuario con texto + asistente **vacío**), pasa a `"enviando"`, limpia `error`.
- [ ] `CHUNK`: concatena `delta` al **último** mensaje de forma **inmutable** (copia array + objeto), pasa a `"streaming"`; guard si no hay mensajes / el último no es del asistente.
- [ ] `COMPLETAR`: vuelve a `"idle"`.
- [ ] `ERROR`: pasa a `"error"`, guarda el mensaje, **no borra** el parcial.
- [ ] `CANCELAR`: vuelve a `"idle"` **conservando** el parcial.
- [ ] **No mutas** el estado de entrada (el test de inmutabilidad pasa).
- [ ] Todos los tests pasan y agregaste un test propio.
- [ ] Puedes **explicar sin notas** por qué el mensaje de asistente nace vacío y por qué el parcial no se borra en `ERROR`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Un `switch (accion.tipo)`. En `ENVIAR`: `{ ...state, estado: "enviando", error: null, mensajes: [...state.mensajes, {id: idUsuario, rol: "user", texto}, {id: idAsistente, rol: "assistant", texto: ""}] }`. En `CHUNK`: guard de `state.mensajes.length === 0`; `const ultimo = state.mensajes[state.mensajes.length - 1]`; guard de `ultimo.rol !== "assistant"`; `const actualizado = { ...ultimo, texto: ultimo.texto + accion.delta }`; `{ ...state, estado: "streaming", mensajes: [...state.mensajes.slice(0, -1), actualizado] }`. En `ERROR`: `{ ...state, estado: "error", error: accion.mensaje }` (no toques `mensajes`). En `COMPLETAR`/`CANCELAR`: `{ ...state, estado: "idle" }`. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/chat-reducer-streaming/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/chat-reducer-streaming.md` — no la mires antes de intentarlo de verdad.
