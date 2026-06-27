# Ejercicio 6.5 — Decisión: modelo de embeddings + chunking

> **Modalidad: diseño / razonamiento (sin código).** No hay tests ni función que
> implementar. Entregas un documento donde **decides y justificas** la arquitectura
> de embeddings para tres escenarios reales. Esto es exactamente lo que defiendes en
> una entrevista de AI Engineer y lo que escribes como ADR en el capstone.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.5` Embeddings y búsqueda semántica
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Elegir, para tres escenarios distintos, un **modelo de embeddings** (local vs API,
dimensiones, idioma) y una **estrategia de chunking** (tamaño + solape, o por qué no
aplica), nombrando en cada caso la **restricción dominante** y al menos un **riesgo
concreto**. La meta no es "acertar la respuesta única": no la hay. Es **justificar un
trade-off defendible**.

## 📋 Contexto

En el Capstone F6 vas a escribir un ADR ("Architecture Decision Record") explicando
por qué elegiste tal modelo y tal chunking. Si no puedes defender esa decisión con la
restricción dominante (privacidad / costo / latencia / idioma / calidad), el revisor
—o el entrevistador— te desarma. Este ejercicio entrena justo ese músculo.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba), apoyándote solo en la lección.
2. Para cada escenario, identifica **primero** la restricción que manda y deja que
   ella guíe el resto de las decisiones.
3. Solo al final, usa IA para *revisar y cuestionar* tu razonamiento — no para
   generarlo. Pídele que ataque tus trade-offs, no que los escriba.

## 🛠️ Instrucciones

Crea un archivo `decisiones.md` en esta carpeta. Resuelve los **tres** escenarios
usando, para cada uno, esta plantilla exacta:

```markdown
## Escenario N

- **Restricción dominante:** <privacidad | costo | latencia | idioma | calidad> — por qué manda aquí.
- **Modelo:** <local vs API; cuál familia; dimensiones; idioma> — justificación en 1–2 frases.
- **Chunking:** <tamaño en palabras/tokens + solape, o "no aplica porque…"> — ligado al tipo de documento.
- **Riesgo concreto:** <un problema que podría aparecer y cómo lo mitigarías>.
```

### Escenario 1 — Buscador interno de manuales técnicos

Una empresa quiere un buscador sobre sus **manuales técnicos en español** (cientos de
PDFs largos). **Los datos no pueden salir de la infraestructura de la empresa** (es
información sensible de ingeniería). Los manuales están llenos de **códigos de error
exactos** como `E_4521` y referencias de pieza `SKU-99213`. Volumen moderado de
documentos, búsquedas internas de empleados.

### Escenario 2 — Chatbot de soporte de e-commerce internacional

Un e-commerce con clientes en **varios idiomas** quiere un chatbot que busque en su
base de **FAQs cortas** (1–3 frases cada una). Reciben **millones de consultas al
mes**, así que el **costo y la latencia por consulta** importan mucho. Los datos no
son especialmente sensibles (son FAQs públicas).

### Escenario 3 — Deduplicar un dataset de productos

Antes de entrenar un modelo interno, el equipo necesita **limpiar un dataset de 2
millones de descripciones de productos en inglés** (cada una un párrafo) eliminando
**casi-duplicados** (el mismo producto descrito dos veces con palabras distintas).
Es un trabajo **batch, de una sola vez**: la latencia no importa, pero el **costo
total** de embeber 2M de textos sí.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres escenarios resueltos con la plantilla completa.
- [ ] Cada decisión de **modelo** nombra la restricción dominante, no "el mejor".
- [ ] Cada decisión de **chunking** justifica el tamaño (o el "no aplica") ligado al
      tipo de documento.
- [ ] Al menos un escenario nombra un **riesgo concreto** real (p. ej. la semántica
      falla con identificadores exactos → hybrid search).
- [ ] Puedes **defender oralmente** cada decisión sin leer tus notas.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/decision-embeddings-chunking/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad. (Recuerda: hay varias respuestas defendibles; el corrector
evalúa tu **justificación**, no que coincidas palabra por palabra.)
