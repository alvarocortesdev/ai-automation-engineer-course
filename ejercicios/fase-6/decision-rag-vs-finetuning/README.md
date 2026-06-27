# Ejercicio 6.13 — Decisión: RAG, fine-tuning, híbrido o ninguno

> **Modalidad: diseño / razonamiento (sin código).** No hay tests ni función que
> implementar. Entregas un documento donde **decides y justificas**, para cinco peticiones
> reales, si corresponde RAG, fine-tuning, ambos (híbrido) o ninguno. Es exactamente la
> pregunta de entrevista "¿cuándo fine-tuning y cuándo RAG?" y el ADR que escribes en un
> proyecto serio.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.13` Fine-tuning en sistema híbrido
**Ruta:** opcional / profundización · **Timebox:** 40 min · **Modalidad:** a-mano (diseño)

## 🎯 Objetivo

Para cinco peticiones distintas, elegir y **justificar**: (a) **RAG / fine-tuning / híbrido
/ ninguno**, (b) el **eje dominante** que manda la decisión (¿conocimiento, comportamiento,
o un prompt basta?), (c) si es híbrido, **qué cubre cada parte**, y (d) **qué eval de una
línea** zanjaría la duda. No hay una única respuesta correcta: se evalúa la **calidad del
trade-off**.

## 📋 Contexto

El error #1 de quien recién entra a IA es proponer fine-tuning para "enseñarle hechos" al
modelo —que es trabajo de RAG—. El error #2 es creer que RAG y fine-tuning son alternativas
excluyentes, cuando los sistemas serios usan ambos en ejes distintos. Si no puedes derivar
cada decisión del eje dominante —ni nombrar qué eval lo confirmaría— el entrevistador o el
cliente te desarma. Este ejercicio entrena ese músculo. En el capstone de la fase usarás
esto para escribir el ADR de "por qué (no) fine-tuneamos".

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba), apoyándote solo en la lección.
2. Para cada caso, pregúntate **primero**: "¿lo que le falta al modelo es **conocimiento**
   (hechos/datos) o **comportamiento** (forma/estilo/tarea repetida)? ¿O un prompt ya
   basta?". Deja que esa pregunta guíe el resto.
3. Solo al final, usa IA para *atacar* tus decisiones, no para escribirlas.
4. Mañana, **reescribe de memoria** el eje que decide RAG vs fine-tuning. Si no puedes, no
   lo aprendiste todavía.

## 🛠️ Instrucciones

Crea un archivo `decisiones.md` en esta carpeta. Resuelve los **cinco** casos usando, para
cada uno, esta plantilla exacta:

```markdown
## Caso N

- **Eje dominante:** <conocimiento | comportamiento | un-prompt-basta | mixto> — por qué.
- **Decisión:** <RAG | fine-tuning | híbrido | ninguno> — derivada del eje, no "el mejor".
- **Si es híbrido:** qué cubre RAG (los hechos) y qué cubre el fine-tuning / prompt (la forma).
- **Riesgo si eligieras mal:** una consecuencia concreta (p. ej. fine-tunear hechos → alucina y no se actualiza).
- **Eval de una línea:** qué medirías para confirmar la decisión (métrica + sobre qué datos).
```

### Caso 1 — Precios del catálogo

Un retailer quiere que su chatbot responda con los **precios actuales** de su catálogo, que
**cambian cada semana** por promociones.

### Caso 2 — Formato y tono rígidos a alto volumen

Una empresa procesa **millones de tickets al mes** y necesita que el modelo responda
**siempre** en un JSON exacto, con un tono fijo y sin preámbulos. Ya probaron un prompt con
few-shot largo: funciona, pero ese prompt enorme se paga en **cada** uno de los millones de
requests.

### Caso 3 — Asistente legal sobre contratos propios

Un estudio jurídico quiere un asistente que responda **según sus propios contratos**
(documentos privados que cambian cuando entra un cliente nuevo) y que lo haga con la **voz
formal y la estructura** de la firma.

### Caso 4 — Resumir un correo

Un usuario quiere un botón que **resuma en una línea** el correo que está leyendo. Tarea
genérica, sin datos privados ni formato exótico.

### Caso 5 — Tono de marca difícil de describir

Una marca quiere que el modelo escriba con su **voz** particular. No saben **escribir** la
respuesta perfecta, pero frente a dos borradores **siempre saben cuál suena más a la
marca**. Volumen moderado.

> Pista honesta: los cinco casos cubren a propósito los cuatro veredictos (RAG, fine-tuning,
> híbrido, ninguno) y uno de ellos apunta a una técnica de fine-tuning específica que se
> alinea con **preferencias rankeables**. No fuerces que todos sean "híbrido".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los cinco casos resueltos con la plantilla completa.
- [ ] Cada decisión se deriva del **eje dominante** (conocimiento vs comportamiento vs
      un-prompt-basta), no de "el mejor".
- [ ] Al menos un caso es **híbrido** y explica qué cubre RAG y qué cubre el fine-tuning/prompt.
- [ ] Identificas el caso de **"ninguno"** (un prompt basta) y el caso de **"RAG"** (hechos
      cambiantes), sin confundirlos con fine-tuning.
- [ ] Cada caso propone un **eval de una línea** que lo zanjaría (métrica + datos).
- [ ] Puedes **defender oralmente** cada decisión sin leer tus notas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por la pregunta binaria de la lección: **¿conocimiento o comportamiento?** El
conocimiento (hechos, datos frescos, documentos privados) casi siempre es RAG. El
comportamiento (formato, estilo, tono, tarea estrecha repetida) es donde el fine-tuning
*puede* ganar —pero primero intenta un prompt—. Cuando un caso tiene **las dos cosas**, es
híbrido: no elijas, reparte. Y para el caso del "tono que no saben escribir pero sí
rankear", recuerda qué técnica de fine-tuning trabaja con pares `(preferida, rechazada)`.
Revisa la sección "El híbrido por defecto" de la lección antes de mirar la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/decision-rag-vs-finetuning/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad. (Hay varias respuestas defendibles; el corrector evalúa tu
**justificación** y que derives del eje correcto, no que coincidas palabra por palabra.)
