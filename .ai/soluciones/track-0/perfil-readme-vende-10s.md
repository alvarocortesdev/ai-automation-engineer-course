---
ejercicio_id: track-0/perfil-readme-vende-10s
fase: track-0
sub_unidad: "T0.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Ojo: este ejercicio es de
> **diseño/comunicación**. No existe una única respuesta correcta —el perfil de cada alumno será
> distinto—; esta es una **referencia ejemplar** + el criterio para juzgar otras entregas.

# Solución de referencia — Escribe tu perfil README que vende en 10 segundos

## Respuesta canónica (ejemplo de entrega "excelente", en inglés)

```markdown
# Jane Doe — AI / Automation Engineer

I build agentic automations that classify, decide, and act on real systems —
with evals, guardrails, and failure handling.

## What I build
- **agentic-invoice-pipeline** — invoices → an AI classifies/extracts → decides →
  writes to the ERP. Idempotent, DLQ, agent eval gate, cost ceiling. [demo](…) · [write-up](…)
- **rag-docs-platform** — production RAG: hybrid search, reranking, versioned eval
  harness, traces in Langfuse. [demo](…)
- **homebase** — fullstack app with real users; includes a public post-mortem of a prod failure. [demo](…)

## Stack
Python · TypeScript · FastAPI · PostgreSQL · Docker · LangGraph

## Reach me
[LinkedIn](…) · jane@example.com
```

### Política de pins (entregable, no se publica)
- **Pin 1: agentic-invoice-pipeline** — es el capstone agéntico (Fase 7), el nicho menos saturado; es
  lo que me diferencia del 80% de portafolios. Va primero a propósito.
- **Pin 2: rag-docs-platform** — RAG de producción con eval harness; demuestra el hilo de evals.
- **Pin 3: homebase** — usuarios reales + post-mortem público; la narrativa de "falla en producción"
  que un homelab puro no tiene.

### Justificación de recorte (entregable, no se publica)
- **Omití el GIF de bienvenida** — ocupa el espacio más valioso (lo primero que se ve) sin responder
  quién/qué/cómo te contacto.
- **Omití el muro de 30 badges** — divide la atención y diluye los 6 skills que de verdad domino; un
  muro dice "no sé priorizar".
- **Omití stats cards / streak / trofeos** — son vanity metrics: miden actividad, no capacidad de
  ingeniería, y un reclutador no contrata por un gráfico verde.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **10 segundos, 3 preguntas.** Quién eres + qué construyes + cómo te contacto. Todo elemento compite
   por esos segundos; si no responde una de las tres, resta.
2. **Hero line falsable y de nicho.** "Apasionado por la tecnología" sirve para cualquiera y no es
   falsable. "Construyo automatizaciones agénticas con evals y manejo de fallas" sí dice algo y apunta
   a un nicho concreto.
3. **Los pins son la prueba, el stack es contexto.** Lo que convence no es la lista de tecnologías, es
   el resultado y la dificultad de cada capstone. Por eso "what I build" pesa más que "stack".
4. **Curar = borrar.** Un perfil de senior es escaso y deliberado. La sección de recorte demuestra que
   el alumno entiende la densidad de señal, no solo que sabe agregar cosas.
5. **Inglés + hilo transversal = Excelente.** El README en inglés materializa el gate de T0.1; nombrar
   evals/observabilidad/usuarios reales eleva el perfil sobre el promedio.

## Puntos resbalosos (donde el corrector debe mirar)
- **Hero line genérica** disfrazada de concreta ("desarrollador full-stack apasionado por crear
  soluciones innovadoras" = nada).
- **Proyectos = tecnología**, no resultado ("app en React" en vez de "qué hace + por qué es difícil").
- **Stack inflado** (>10 tecnologías, varias usadas una vez).
- **Pinear todo** o pinear tutoriales en vez de capstones.
- **Sección de recorte recitada** ("las vanity metrics son malas") pero el perfil sigue lleno de ruido:
  incoherencia entre lo que dice y lo que hace.

## Rango de soluciones aceptables
- Cualquier hero line concreta y falsable que nombre rol + qué construye cuenta, sin importar el nicho
  exacto (no todos apuntan a agéntico).
- Los 3 proyectos pueden ser distintos y estar "en progreso" si son reales; lo que no es válido es
  inventarlos o usar tutoriales como capstones.
- El idioma puede ser español si el alumno apunta al mercado local (pierde el bonus de inglés, no es
  un error). Lo **no** válido: hero line genérica, stack-muro, o un perfil sin recorte justificado.
