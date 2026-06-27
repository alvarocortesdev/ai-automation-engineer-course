# Ejercicio 4.11 B — Diseña los estados y la seguridad de una UI de chat de IA

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.11` UI para apps de IA
**Ruta:** crítica · **Modalidad:** razonamiento / diseño (sin código) · **Timebox:** 35 min

## 🎯 Objetivo

Inventariar los **seis estados de primera clase** de una UI de chat de IA y diagnosticar un componente con defectos reales: faltan estados, no hay streaming, no hay optimistic UI, y un **XSS** por renderizar salida de un LLM como HTML. Produces un **documento de diseño**, como en una revisión de UX/seguridad, antes de escribir una sola línea de código.

## 📋 Contexto

La lección insiste en que, si tienes claros los estados y los riesgos de renderizar salida de un modelo, las herramientas (`useChat`, `streamText`) son detalles. Este ejercicio entrena ese músculo conceptual. Alimenta directo al **Capstone F4**, donde tendrás que dibujar cada estado y sanitizar la salida del LLM como gate de seguridad.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Lee `respuesta-buggy.md` y razona en tu documento. **Sin IA.**
2. Solo entonces, consulta la **documentación oficial**: <https://ai-sdk.dev/docs/ai-sdk-ui/chatbot> y <https://owasp.org/www-community/attacks/xss/>.
3. **Solo al final**, usa IA para *revisar y cuestionar* tu diseño —no para *generártelo*.
4. Mañana, explícale a alguien (o al espejo) por qué el streaming "se siente más rápido" sin acelerar nada, en menos de un minuto. Si no te sale, no lo aprendiste.

## 🛠️ Instrucciones

1. Lee `respuesta-buggy.md` (el componente de chat de IA a diagnosticar).
2. Escribe tu análisis en `diseno-chat.md` (ya tiene la estructura con los huecos a completar). **No escribes código de implementación**: es un documento de diseño.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **Inventario de estados**: los **seis** estados (vacío/enviando/streaming/completado/error/cancelado), con qué ve el usuario y qué transición activa cada uno.
- [ ] **Diagnóstico del buggy**: cada defecto de `respuesta-buggy.md` nombrado, con el patrón de la lección que lo arregla.
- [ ] **Seguridad**: el riesgo de XSS de renderizar salida del LLM como HTML y la regla correcta; una línea conectándolo con OWASP de la Fase 3.
- [ ] **Accesibilidad**: dos medidas concretas para el texto en vivo (`aria-live`, foco, affordance de cancelar).
- [ ] **Trade-off**: por qué streaming + optimistic UI frente a esperar la respuesta completa, y el costo vs el beneficio.
- [ ] Puedes **defender tu diseño sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el inventario, copia la tabla de la sección 4.6 de la lección y exprésala con tus palabras. Para el componente buggy, contrasta cada línea contra el *non-example* de la sección 5: espera la respuesta completa (sin streaming), no muestra el mensaje del usuario (sin optimistic UI), no tiene estados (ni pensando, ni error, ni cancelar), y usa `dangerouslySetInnerHTML` (XSS). Para seguridad, la regla es la sección 4.7: React escapa el texto en `{}`; el peligro es solo `dangerouslySetInnerHTML`. Para a11y, piensa cómo un lector de pantalla se entera de que llegó texto nuevo. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/estados-ui-chat-ia/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/estados-ui-chat-ia.md` — no la mires antes de intentarlo de verdad.
