# 2.10 — Presupuesto de la pirámide: qué merece e2e y qué no

**Fase:** Fase 2 — Ingeniería de software · **Lección:** [`2.10` Playwright e2e](/fase-2-ingenieria/2-10-playwright-e2e/)
**Ruta:** opcional/profundización · **Timebox:** 30–40 min · **Modalidad:** a mano (razonamiento)

## 🎯 Objetivo

Sin escribir un solo test: ejercitar el **juicio de pirámide** que un entrevistador
busca. Dado un conjunto de escenarios, decidir cuáles merecen un test e2e (caro, pero
valioso para flujos críticos) y cuáles se cubren mejor con tests más baratos, y escribir
la **política de e2e** que le propondrías a tu equipo. Saber **cuántos** e2e escribir es
tan importante como saber escribirlos.

## 📋 Contexto

Lee `escenarios.md`: describe 8 escenarios candidatos a test de una app de finanzas
(login, agregar gasto, cálculo de total, validación de campo, flujo de pago, formateo de
fecha, endpoint de API y render de un gráfico). Alguien propuso "testearlos todos". Tu
trabajo es poner orden con la pirámide.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Decide con tu criterio antes de buscar.
2. Solo entonces, consulta [The Practical Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html)
   y las [best practices de Playwright](https://playwright.dev/docs/best-practices).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. En 3 días, defiende tu política en voz alta como si te entrevistaran.

## 🛠️ Instrucciones

1. **Clasifica** en `decisiones.md` cada uno de los 8 escenarios como
   `e2e` / `integración` / `unit` / `no-testear`, con **una frase** de justificación
   anclada en dos preguntas:
   - ¿es un **flujo crítico de usuario de punta a punta** (si se rompe, pierdes plata o
     usuarios)?
   - ¿el **costo/fragilidad** de un e2e se justifica, o un test más barato (unit/integración)
     da la misma confianza?
2. **Escribe `politica-piramide.md`** (máx. 1 página) que responda, con argumentos:
   - ¿Cuántos e2e y sobre qué? (criterio "poco y crítico"; pirámide, no cono de helado.)
   - ¿Qué regla de **selectores** adoptamos y por qué? (rol/label vs. CSS.)
   - ¿Cuál es la regla sobre **esperas/`sleep`s**? (web-first assertions, prohibir `waitForTimeout`.)
   - ¿Cuándo corren los e2e en **CI** y por el costo de qué? (críticos en cada PR vs. el resto nightly.)

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 8 escenarios tienen clasificación **y** justificación ligada a valor/costo.
- [ ] Reconociste que solo **1–2 flujos críticos** (login, flujo de pago) merecen e2e.
- [ ] El cálculo del total, la validación y el formateo de fecha van a **unit** (lógica pura).
- [ ] Tu política propone la forma de **pirámide** (no "un e2e por feature" = cono de helado).
- [ ] Tu política adopta selectores por rol y **prohíbe** `waitForTimeout` como estabilizador, con la razón.
- [ ] Tu política reconoce el **costo** del e2e y propone una cadencia de CI realista.
- [ ] Puedes defender **sin notas** por qué meter el cálculo del total a un e2e es desperdiciar la pirámide.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `decisiones.md` — la tabla de clasificación de los 8 escenarios con justificación.
- `politica-piramide.md` — tu política de e2e (máx. 1 página).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Heurística: va a **e2e** lo que es (a) un flujo de usuario **de punta a punta** y (b)
**crítico**. Va a **unit** la **lógica pura** que puede equivocarse pero no necesita
navegador. Va a **integración** la **frontera** entre tu código y un sistema (DB, API).
Pregúntate por cada uno: "si esto se rompe, ¿qué pasa?" y "¿necesito un navegador real
para verificarlo, o un test 100× más barato da la misma certeza?". El gráfico de terceros:
testea que **el dato** llegue, no los píxeles. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluidos `decisiones.md` y `politica-piramide.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/playwright-presupuesto-e2e.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/playwright-presupuesto-e2e.md`
— no la mires antes de intentarlo de verdad.
