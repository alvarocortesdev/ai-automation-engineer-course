---
ejercicio_id: fase-6/decision-rag-vs-finetuning
fase: fase-6
sub_unidad: "6.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir** de un ejercicio de diseño: hay varias respuestas defendibles. Úsala para juzgar
> la **calidad del trade-off** y que la decisión se derive del eje correcto, no para exigir
> coincidencia literal.

# Solución de referencia — RAG, fine-tuning, híbrido o ninguno

> Respuestas **canónicas y defendibles**, no las únicas. Lo que importa: que cada decisión
> **se derive del eje dominante** (conocimiento vs comportamiento vs un-prompt-basta) y que
> el eval propuesto pueda confirmarla.

## Caso 1 — Precios del catálogo

- **Eje dominante:** conocimiento, y encima **cambiante** (precios que se mueven semanal).
- **Decisión:** **RAG**. Se indexa el catálogo y se recupera el precio real en cada query.
- **Si es híbrido:** N/A.
- **Riesgo si eligieras mal:** fine-tunear precios → el modelo los **aproxima y alucina**,
  y el día que sube uno sigue diciendo el viejo; corregirlo exige re-entrenar (otra GPU).
  Con RAG se actualiza editando una fila/documento.
- **Eval de una línea:** exactitud factual del precio sobre un set de preguntas con respuesta
  conocida (¿el precio devuelto coincide con el del catálogo?), medida tras cambiar precios.

## Caso 2 — Formato y tono rígidos a alto volumen

- **Eje dominante:** comportamiento (forma: JSON exacto + tono), tarea estrecha y repetida.
- **Decisión:** primero **un buen prompt + few-shot + structured outputs**; **fine-tuning
  (SFT con LoRA)** *solo si* a millones de requests el prompt largo sale caro y la
  consistencia exigida no se logra con prompt. El gatillo del FT aquí es **costo a escala +
  consistencia**, no "enseñar" nada.
- **Si es híbrido:** N/A (no hay conocimiento privado en juego; es pura forma).
- **Riesgo si eligieras mal:** fine-tunear de entrada sin probar prompt → semanas de GPU
  para algo que un prompt resolvía; o ignorar el costo del prompt largo a millones de
  requests.
- **Eval de una línea:** % de respuestas con **JSON válido y formato correcto** sobre 200+
  tickets reales, comparando baseline (prompt) vs candidato fine-tuneado, junto al **$/request**.

## Caso 3 — Asistente legal sobre contratos propios

- **Eje dominante:** **mixto** — conocimiento (qué dicen *estos* contratos, privados y
  cambiantes) **y** comportamiento (voz formal + estructura de la firma).
- **Decisión:** **híbrido**.
- **Si es híbrido:** **RAG** cubre los hechos (recupera el contrato relevante; se re-indexa
  cuando entra un cliente nuevo) — no-negociable, no se fine-tunean hechos. El **fine-tuning
  o, primero, el prompt** cubre la voz formal y la estructura (comportamiento).
- **Riesgo si eligieras mal:** fine-tunear los contratos → alucina cláusulas y filtra datos
  sensibles horneados en los pesos (riesgo de gobernanza: difícil de "borrar"). Usar solo
  prompt sin RAG → responde de memoria genérica, no según *estos* contratos.
- **Eval de una línea:** doble métrica → exactitud factual/grounding sobre preguntas con
  respuesta en los contratos (RAG) + un juez de "registro formal de la firma" sobre un set
  de respuestas (comportamiento), baseline vs candidato.

## Caso 4 — Resumir un correo

- **Eje dominante:** **un-prompt-basta**. Tarea genérica, sin datos privados ni forma exótica.
- **Decisión:** **ninguno**. Una instrucción de una línea a un modelo decente lo resuelve.
- **Si es híbrido:** N/A.
- **Riesgo si eligieras mal:** fine-tunear o montar RAG aquí = complejidad y costo
  injustificados ("quemar plata por deporte").
- **Eval de una línea:** un juez ligero (o muestra manual) de calidad del resumen sobre
  20–30 correos; si el prompt ya pasa, no hay nada que optimizar.

## Caso 5 — Tono de marca difícil de describir

- **Eje dominante:** comportamiento (la **voz** de la marca), pero con un matiz: no saben
  **escribir** la respuesta perfecta, solo **rankear** cuál de dos suena mejor.
- **Decisión:** **fine-tuning**, y específicamente **DPO** (Direct Preference Optimization),
  que entrena con pares `(preferida, rechazada)` — justo lo que tienen. SFT encaja peor
  porque exige respuestas-modelo escritas, que aquí no saben producir.
- **Si es híbrido:** N/A (salvo que también necesiten hechos de marca → ahí entraría RAG).
- **Riesgo si eligieras mal:** intentar SFT sin respuestas de referencia claras → dataset
  pobre; o intentar describir el tono en un prompt cuando ni ellos saben describirlo.
- **Eval de una línea:** preferencia humana (o LLM-as-judge) en comparaciones ciegas
  candidato-vs-baseline sobre N borradores: ¿con qué frecuencia eligen la salida del modelo
  alineado?

## Puntos resbalosos (donde el corrector debe mirar)

1. **Fine-tunear el Caso 1** (hechos cambiantes): el error más grave; márcalo siempre.
2. **No detectar el híbrido del Caso 3** (resolverlo como solo-RAG o solo-FT).
3. **Saltar a FT en el Caso 2** sin pasar por el prompt, o sin nombrar el costo a escala.
4. **Caso 4 sobre-ingenierizado** (RAG/FT para resumir un correo).
5. **Caso 5 como SFT** sin notar que es preferencias rankeables → DPO.
6. Evals ausentes o no-medibles ("preguntarle a la IA", "ver si se siente mejor").

## Rango de soluciones aceptables

- En el Caso 2, si el alumno argumenta que el prompt **nunca** alcanzará la consistencia a
  ese volumen y va directo a FT, es defendible **siempre que** nombre el costo a escala y
  proponga medirlo.
- En el Caso 5, aceptar SFT es defendible **solo si** el alumno explica cómo construiría
  respuestas de referencia; DPO es la respuesta más fina y demuestra dominio.
- En el Caso 3, el orden "prompt primero, FT solo si el eval lo justifica" es tan válido como
  proponer FT de la forma directamente, mientras el RAG de los hechos esté presente.
- Cualquier eval concreto y pertinente cuenta; no se exige el de arriba. Plantearlo como
  **baseline vs candidato** es señal de `excelente`, no requisito.
- Mencionar el riesgo de gobernanza (FT hornea datos, RAG permite borrar) en el Caso 3 es
  señal de dominio, no obligatorio.
