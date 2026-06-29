---
ejercicio_id: track-0/adaptar-cv-a-jd
fase: track-0
sub_unidad: "T0.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de
> **diseño/razonamiento**: el CV de cada alumno será distinto. Lo que se mide es el **criterio de
> adaptación** (extracto correcto, honestidad tengo/no-tengo, reflejar sin inflar, conocer el ATS).

# Solución de referencia — Adapta tu CV a una job description (Northwind Labs)

## 1. Extracto de keywords de referencia

**Must-have (la oferta los exige):**
Python · FastAPI · LLM APIs (OpenAI/Anthropic) · function calling / tool use · RAG (embeddings + vector
DB, pgvector) · retrieval + reranking · PostgreSQL · Docker · CI/CD (GitHub Actions) · **professional
English** · public portfolio/GitHub que **corre**. Blandas implícitas: **end-to-end ownership**, **on-call**,
**specs/ADRs**, evals como gate ("no shippeamos IA que no podemos medir").

**Nice-to-have (suman, no filtran):**
LangGraph · evals tooling (ragas/DeepEval/promptfoo) · observabilidad (Langfuse) · TypeScript/Next.js ·
n8n/Temporal · OWASP LLM Top 10 / guardrails.

> Error frecuente: tratar LangGraph, n8n o Next.js como obligatorios. La oferta los lista en
> **nice-to-have**; faltar uno NO descalifica. Faltar Python, RAG o inglés sí.

## 2. Header + summary de referencia (perfil del curso, en inglés)

```text
CAMILA ROJAS
AI / Automation Engineer
Santiago, Chile (UTC-3) · camila@example.com · linkedin.com/in/camila · github.com/camila

I build agentic automations that classify, extract, decide, and act on external systems,
with human-in-the-loop and evals. Python · FastAPI · RAG (pgvector, reranking) · LLM tool use.
```

Por qué este título: la empresa se nombra a sí misma con "**agentic automations**" que "**act on
external systems**" con "**human-in-the-loop**". El header **espeja** ese énfasis (no "Fullstack
Developer", no "RAG Engineer" a secas). El summary reusa términos **literales** de la JD que el perfil
posee: classify/extract/decide/act, human-in-the-loop, evals, FastAPI, RAG, tool use.

## 3. Skills de referencia (espeja, must-haves primero)

```text
Python · FastAPI · LLM APIs (OpenAI/Anthropic) · function calling / tool use · RAG ·
pgvector · reranking · PostgreSQL · Docker · CI/CD (GitHub Actions) · evals (ragas) ·
Langfuse · LangGraph
```

Orden = prioridad de la oferta (must-haves arriba, nice-to-have al final). **Solo** lo defendible con un
capstone. Si el alumno no tiene LangGraph real, lo deja fuera y, a lo sumo, lo nombra como gap a cerrar
—no lo mete en Skills.

## 4. Tres elementos ATS-rompedores (referencia)

| Elemento omitido | Por qué |
|---|---|
| **Foto** | No aporta texto parseable; en remoto-USD no se usa (sesgo/legal); algunos parsers se confunden. |
| **Dos columnas / tabla de skills** | El ATS lee de arriba-abajo, izquierda-derecha: una columna lateral se intercala con el cuerpo y sale un puré; las barras de "nivel" no son texto extraíble. |
| **Headers no estándar / info en header-footer** | El ATS busca etiquetas literales (Experience/Projects/Skills/Education); "Mi viaje" no matchea, y muchos parsers ignoran el header/footer del documento. |

## 5. Decisión de postulación de referencia

**Postular marcando un gap.** El perfil cumple todos los must-have (Python, FastAPI, RAG, pgvector,
Docker, CI/CD, inglés, GitHub que corre) y varios nice-to-have (evals, Langfuse). El único hueco es
Temporal/durable execution, que es nice-to-have → **se postula igual** (es una postulación "stretch"
sana del pipeline de T0.2), idealmente con una línea honesta sobre estar cerrando ese gap. No postular
sería dejar pasar una oferta para la que el perfil **califica**.

## Puntos donde el corrector debe mirar
1. **Keyword stuffing.** Meter en Skills toda keyword de la oferta (incluida una que no domina) es el
   error central. Reflejar lo defendible = honesto; copiar la JD = peligroso.
2. **Must-have vs nice-to-have confundidos.** Tratar LangGraph/n8n como obligatorios lleva a auto-
   descartarse sin razón, o a inflar para "cumplir".
3. **Header que no espeja el énfasis.** Si la oferta grita "agentic" y el header dice "Fullstack", el
   alumno no leyó cómo la empresa se nombra a sí misma.
4. **Formato.** No nombrar ningún elemento ATS-rompedor, o creer que un PDF de diseño siempre parsea.

## Rango de soluciones aceptables
- Un título de rol distinto es válido si refleja el énfasis (p. ej. "AI Engineer (Agentic Automation)").
- Marcar honestamente varios "no-tengo" y decidir **no** postular es válido **si** se justifica (faltan
  must-haves reales), no por inseguridad ante nice-to-haves.
- Entregar en español es aceptable (pierde el bonus de inglés) **salvo** que el alumno olvide que la
  oferta exige inglés profesional y no lo registre como gap —eso sí es un error de lectura.
- Cualquier set de Skills es válido mientras **espeje la oferta y sea defendible**; lo no válido es
  stuffear o no adaptar.
