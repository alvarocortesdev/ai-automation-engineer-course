# Ejercicio 4.5 B — Depura un panel lleno de useEffect

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.5` React + TypeScript
**Ruta:** crítica · **Modalidad:** a-mano (diagnóstico escrito) · **Timebox:** 30 min

## 🎯 Objetivo

Depurar, **leyendo** (no ejecutando), un componente con cinco `useEffect`: identificar cuáles están rotos, **nombrar el antipatrón exacto** de cada uno, explicar su consecuencia observable y describir el arreglo mínimo. Cuatro están mal; **uno está bien**: reconocer el correcto cuenta tanto como cazar los rotos.

## 📋 Contexto

Esta es la habilidad que más se evalúa en una entrevista de React y la que más bugs te ahorra en el [Capstone F4](/fase-4-frontend/proyecto/): saber cuándo un `useEffect` sobra. La interfaz de chat con streaming del capstone vive o muere por usar efectos solo para lo que son (sincronizar con sistemas externos) y nada más.

## 📏 Primero-Sin-IA

1. Diagnostica **solo**, a mano, leyendo `PanelBuggy.tsx` (timebox arriba). **No lo ejecutes.**
2. Solo entonces, consulta la **documentación oficial**: <https://react.dev/learn/you-might-not-need-an-effect> y <https://react.dev/learn/synchronizing-with-effects>.
3. **Solo al final**, usa IA para *revisar* tu diagnóstico —no para que te lo escriba.
4. Mañana, vuelve a diagnosticar de memoria. Si no nombras las cuatro categorías, no lo aprendiste.

## 🛠️ Instrucciones

1. Abre `PanelBuggy.tsx` y léelo como en un *code review*. Hay cinco efectos numerados (`EFECTO 1` … `EFECTO 5`).
2. Completa `diagnostico.md` (la plantilla ya está). Para **cada** efecto:
   - **Veredicto:** ¿bien o mal?
   - Si está mal, **nombra el antipatrón** (estado derivado disfrazado de efecto / dependencia faltante / falta de cleanup → race condition / debió ser event handler).
   - **Consecuencia observable** (render de más, datos viejos en pantalla, fuga de recursos, doble disparo, etc.).
   - **Arreglo:** en palabras + el mínimo código necesario (no reescribas todo el componente).
   - Para el efecto **correcto**, explica por qué es un uso legítimo de `useEffect`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los cinco efectos tienen veredicto.
- [ ] Identificaste correctamente cuál es el efecto **bien hecho** y justificaste por qué.
- [ ] Para los cuatro rotos, nombraste el **antipatrón exacto** (no descripciones vagas).
- [ ] Cada arreglo es concreto y mínimo; no propones reescribir el componente entero.
- [ ] Puedes **explicar sin notas** la regla general: "`useEffect` solo sincroniza con sistemas externos; lo derivable se calcula en el render; las respuestas a interacciones van en el handler".

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para cada efecto pregúntate, en este orden:
1. ¿Esto se podría **calcular en el render** a partir de props/estado en vez de guardarlo en estado? → estado derivado.
2. ¿El array de deps incluye **todo** lo que el efecto lee (props y estado)? Si lee algo que no está, su valor queda "congelado" (stale). → dependencia faltante.
3. ¿El efecto arranca algo asíncrono o una suscripción que habría que **cancelar** al cambiar deps o al desmontar? → falta cleanup (race condition / fuga).
4. ¿Esto ocurre como **respuesta a una interacción** del usuario y no como sincronización con un sistema externo? → debió ser event handler.

Uno de los cinco pasa las cuatro preguntas sin problema: ese es el correcto. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/depurar-efectos-react/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/depurar-efectos-react.md` — no la mires antes de intentarlo de verdad.
