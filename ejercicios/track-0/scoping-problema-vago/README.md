# Ejercicio T0.8 — Convierte un pedido vago en un mini-spec (discovery)

> **Modalidad: diseño/razonamiento (sin código, sin IA primero).** El cliente nunca te describe un
> problema: te describe una **solución que se imaginó**. Tu trabajo de Forward-Deployed Engineer es cavar
> hasta el problema real con las preguntas correctas *antes* de escribir una línea de código, y salir con
> un **mini-spec**. El código más caro del mundo es el que resuelve el problema equivocado.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.8` Lane Forward-Deployed / cliente-facing
**Ruta:** profundización · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Convertir un problema de negocio vago en un **mini-spec técnico** aplicando el banco de 7
  preguntas de discovery (outcome, usuario, proceso actual, costo de error, datos, restricciones,
  rebanada mínima) **antes** de codear.
- **O2** — Separar la **solución imaginada** del cliente del **problema real**, y acotar una rebanada
  mínima de valor que sea entregable.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 40 min). No le pidas a la IA que haga el discovery por ti.
2. Solo entonces relee la sección "Los cuatro músculos" y el ejemplo resuelto de la lección si dudaste.
3. **Solo al final**, usa IA para *revisar* tu mini-spec —no para generarlo.
4. Mañana, toma un pedido vago real de tu semana (del trabajo, de un familiar, de un proyecto) y repite
   el ejercicio de memoria.

## 📋 El pedido a trabajar

Lee `pedido-cliente.md` (en esta carpeta): el mensaje **vago** de un stakeholder de negocio. Lo trabajas
como si fueras el FDE que recibió ese mensaje y tiene 40 minutos antes de la reunión de discovery.

## 🛠️ Tu tarea (en este orden)

En `discovery.md` (parte de `discovery.starter.md`):

1. **Detecta la solución imaginada:** nombra qué *solución* propuso el cliente y por qué **no** debes
   construirla aún. ¿Cuál es el problema que podría haber detrás del pedido literal?
2. **Aplica el banco de 7 preguntas:** para cada una (outcome, usuario, proceso actual, costo de error,
   datos, restricciones, rebanada mínima), escribe **la pregunta que harías** y la **respuesta que
   supones** (un supuesto razonable; márcalo claramente como supuesto, no como hecho).
3. **Escribe el mini-spec** con la estructura: problem statement · métrica de éxito (con al menos un
   número) · en-scope (MVP) · fuera-de-scope · restricciones · rebanada mínima de valor · supuestos y
   preguntas abiertas.
4. **Cierra con la pregunta de mayor riesgo:** ¿cuál pregunta, si la respuesta fuera distinta a tu
   supuesto, **más** cambiaría el diseño? Ese es el riesgo número uno de tu scope.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La **solución imaginada** está nombrada y **separada** del problema real.
- [ ] Las **7 preguntas** aparecen, cada una con su respuesta-supuesto **marcada como supuesto**.
- [ ] El **mini-spec** tiene métrica de éxito con **un número** y un **fuera-de-scope** explícito.
- [ ] La **rebanada mínima de valor** es genuinamente pequeña y entregable (no "todo el sistema").
- [ ] Está identificada la **pregunta de mayor riesgo** del scope.
- [ ] Puedes **explicar por qué el spec va al final y no al principio sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El truco está en NO escribir la solución imaginada del cliente en tu spec. Si pidió "un chatbot" pero el
proceso real que describe es "dos personas clasifican correos a mano", el problema es **clasificar/
enrutar**, no responder —y tu spec no debería decir "chatbot". Para el costo de error, pregúntate qué
pasa si el sistema se equivoca en el peor caso: si es grave, eso te obliga a **human-in-the-loop** o a
mayor precisión, y eso es una decisión técnica que sale de una pregunta de negocio. Para la rebanada
mínima: si el cliente quiere resolver 5 cosas, pregúntale cuál **duele más** y haz solo esa primero. El
mini-spec es el **producto** de las preguntas, por eso va al final.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/scoping-problema-vago.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/scoping-problema-vago.md` — no la mires
antes de intentarlo. El corrector evaluará tu **criterio de discovery** (sobre todo que no codees la
solución imaginada y que acotes un MVP real), no que tu spec coincida palabra por palabra con un ejemplo.
