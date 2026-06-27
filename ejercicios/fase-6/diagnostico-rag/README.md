# Ejercicio 6.7 — Diagnóstico de un RAG que falla + elección de técnica

> **Modalidad: diagnóstico/diseño (Primero-Sin-IA).** Sin código. Te enfrentas a tres
> casos de un RAG en producción que da malas respuestas y tienes que **diagnosticar**
> dónde nace cada falla y **elegir la técnica** que la arregla, descartando
> alternativas. Es exactamente lo que te preguntan en una entrevista de AI Engineer:
> "tu RAG devuelve basura, ¿qué revisas y en qué orden?". A mano y sin IA hasta cerrar
> tu intento.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.7` RAG a fondo
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Para cada caso: ubicar la **causa raíz** en la etapa correcta del pipeline
(`chunk → embed → store → retrieve → rerank → generate`), elegir la **palanca**
(hybrid search, Contextual Retrieval, reranking, Agentic RAG o GraphRAG), **descartar**
al menos una alternativa con una razón, y describir **cómo lo medirías** (qué eval).
Más una decisión de índice (HNSW vs IVFFlat) y una de seguridad multi-tenant.

## 📏 Primero-Sin-IA

1. **Antes de escribir**, dibuja de memoria el pipeline RAG completo y el **orden de
   diagnóstico** (recall primero, ranking después, generación al final).
2. Resuelve los casos **solo** (timebox arriba). No abras la lección hasta tener un
   borrador.
3. Solo entonces vuelve a la lección para validar tu razonamiento.
4. **Solo al final**, usa IA para *cuestionar* tus elecciones (que te haga de abogado
   del diablo), nunca para generar el diagnóstico.
5. Mañana, **reescribe el árbol de diagnóstico de memoria**.

## 🛠️ Instrucciones

Crea `diagnostico.md` en esta carpeta. Resuelve los **tres casos** y las **dos
decisiones** usando la plantilla de abajo. Sé concreto: nombra la etapa, la técnica y
la métrica.

### Caso A — El RAG ignora los códigos exactos
Un asistente sobre manuales técnicos. El usuario pregunta por el **código de error
exacto `E_4521`**. El RAG responde con generalidades sobre "errores de conexión". Al
inspeccionar, el chunk que documenta `E_4521` **existe en el corpus** pero **no
aparece** entre los 150 candidatos recuperados.

### Caso B — Chunks relevantes, respuesta vaga
Un asistente sobre reportes financieros. A la pregunta "¿cuánto creció ACME el último
trimestre?", los chunks recuperados **son del tema correcto** (hablan de crecimiento
trimestral) pero la respuesta sale **vaga y a veces mezcla empresas**. Al revisar los
chunks, muchos dicen cosas como "la empresa creció 3% el trimestre" **sin nombrar la
empresa ni el período**.

### Caso C — Preguntas que cruzan documentos
Una base de conocimiento de una consultora. La pregunta "¿qué consultores que
trabajaron en el proyecto Atlas reportan a la misma gerente?" **siempre falla**, aunque
la información está repartida en varios documentos (un doc por consultor, otro de
organigrama, otro del proyecto). El RAG trae chunks sueltos y no logra conectar los
hechos.

### Decisión 1 — HNSW vs IVFFlat
Tu vector DB (pgvector) te deja elegir el índice. Escenario: **2 millones de chunks**,
**inserciones constantes** (documentos nuevos cada hora) y **recall alto** es lo más
importante; tienes RAM de sobra. ¿Qué índice eliges y por qué? ¿Qué cambiaría si la
RAM fuera escasa?

### Decisión 2 — Seguridad multi-tenant
Tu RAG sirve a varios clientes desde el mismo índice. Diseña el **metadata filtering**
para que un cliente nunca vea chunks de otro. ¿Por qué debe ser **fail-closed**? ¿Qué
pasa, en concreto, si falla _open_?

## 📋 Plantilla de respuesta (por cada caso)

```markdown
### Caso X
- **Síntoma:** (qué se observa)
- **Etapa del pipeline donde nace:** (chunk / embed / store / retrieve / rerank / generate)
- **Causa raíz:** (en una o dos frases, qué está mal de fondo)
- **Técnica/palanca que lo arregla:** (hybrid / Contextual Retrieval / reranking / Agentic RAG / GraphRAG / prompt de generación)
- **Alternativa descartada + por qué:** (al menos una)
- **Cómo lo mediría:** (qué eval; p. ej. recall@k, faithfulness)
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres casos resueltos con la plantilla completa.
- [ ] Cada elección de técnica **descarta** al menos una alternativa con una razón
      (no "uso X porque es mejor").
- [ ] Cada caso dice **cómo lo medirías** (una métrica concreta, no "probaría a ver").
- [ ] La Decisión 1 nombra la **restricción dominante** y el efecto de cambiarla.
- [ ] La Decisión 2 propone un filtro **fail-closed** y describe el incidente si falla
      _open_.
- [ ] Puedes **explicar sin notas** el orden de diagnóstico (recall → ranking →
      generación) y por qué ese orden y no al revés.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/diagnostico-rag/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
