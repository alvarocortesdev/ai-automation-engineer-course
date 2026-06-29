---
ejercicio_id: track-0/logros-medibles-xyz
fase: track-0
sub_unidad: "T0.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de
> **comunicación**: no hay una única redacción correcta. Estos son ejemplos ejemplares + el criterio
> para juzgar variantes. Lo que importa es la **estructura** (verbo + número + decisión) y la honestidad.

# Solución de referencia — Reescribe 5 responsabilidades como logros medibles

## Reescrituras de referencia (ejemplo "excelente", en inglés)

| # | Responsabilidad original | Logro medible de referencia |
|---|---|---|
| 1 | Responsable de crear un sistema de automatización con IA. | **Built** a ticket-triage agent that classifies and routes **~200 tickets/day at 94% accuracy [N]**, automating **80% [N]** of manual triage, with **output validation and human-in-the-loop** for sensitive actions. |
| 2 | Trabajé con Python y desarrollé un chatbot. | **Shipped** a customer-support chatbot handling **~500 conversations/week [N]** at **p95 1.3s [N]**, grounded in a RAG index to cut hallucinations, deployed on FastAPI. |
| 3 | Encargado de una aplicación web con base de datos. | **Designed and deployed** a fullstack app serving **8 real users [N]** with full UI states and CI/CD, backed by a normalized PostgreSQL schema and **idempotent** write endpoints. |
| 4 | Ayudé a mejorar el rendimiento de una API. | **Reduced** API p95 latency from **4.2s to 900ms (-79%) [N]** by adding semantic caching and fixing an **N+1 query**, cutting 5xx errors **70% [N]** with retries (backoff + jitter). |
| 5 | Participé en un proyecto de procesamiento de documentos. | **Automated** invoice ingestion of **~1,200 docs/month [N]** with an OCR + LLM extraction pipeline at **96% field accuracy [N]**, eliminating **~30 hours/month [N]** of manual data entry. |

## Razonamiento paso a paso (lo que debe entender el alumno)

1. **Verbo de acción primero.** Cada bullet abre con lo que el candidato *hizo* (Built, Shipped,
   Designed, Reduced, Automated), no con el cargo que tuvo. "Responsable de" describe la silla; el verbo
   describe el resultado.
2. **El número es el corazón.** Un logro sin número no es falsable y no impresiona. El número responde
   "¿cuánto?" en una unidad concreta: /día, %, latencia, usuarios, horas ahorradas. Aquí van marcados
   `[N]` porque son ejemplos; en el CV real se reemplazan por la medición propia.
3. **La decisión técnica prueba criterio.** "Con validación de salida + HITL", "arreglando un N+1",
   "con backoff + jitter", "con caching semántico" — eso separa a alguien que *entiende* de alguien que
   *pegó llamadas a una API*. Es lo que conecta con los hilos transversales del curso.
4. **El antes→después vende.** "De 4.2s a 900ms (-79%)" cuenta una historia de impacto mejor que "mejoré
   la latencia". Cuando hay un baseline, úsalo.
5. **Honestidad del dato.** Marcar `[N]` en el ejercicio es practicar la estructura; **inventar** en el
   CV real es mentir y se cae en la entrevista. Cada número del CV debe poder defenderse.

## Origen honesto de los números (referencia del párrafo final)

Un principiante sin trabajo formal saca los números de sus **capstones instrumentados** (exigidos por
T0.5 y el Definition of Done del curso): la **latencia p95** de las trazas, el **score de eval** (ragas
o el eval harness propio), el **USD/request** del budget de costo, la **cantidad de usuarios reales** de
T0.4, la **cobertura/cantidad de tests**, las **horas que un pipeline ahorra**. Un proyecto de portafolio
serio **es** experiencia citable: los números existen porque se midieron, no porque se inventaron.

## Puntos resbalosos (donde el corrector debe mirar)
- **Verbo débil disfrazado de fuerte:** "Apoyé", "Colaboré en", "Participé" siguen siendo sillas.
- **Número decorativo sin unidad:** "mejoré un 100%" sin decir 100% de qué.
- **Inventar sin marcar:** poner un número como real cuando no se midió, sin `[N]` ni plan de
   verificación → se penaliza como deshonestidad, no como error de estilo.
- **Tecnología en lugar de decisión:** "usé Python y FastAPI" no prueba criterio; la decisión sí.
- **Párrafo final que no aterriza la fuente:** "de mis proyectos" sin nombrar qué métrica ni de dónde.

## Rango de soluciones aceptables
- Cualquier número distinto es válido si la **estructura** está (verbo + impacto + número + decisión) y
  el dato es defendible o está marcado `[N]`.
- En español es aceptable (pierde el bonus de inglés, no es error) si el alumno apunta al mercado local.
- No todos los bullets necesitan decisión técnica, pero **al menos 2** sí; un CV solo de "qué" sin "cómo"
  no prueba seniority.
- Es válido reformular un bullet hacia un proyecto distinto del implícito, siempre que sea real o
  claramente marcado como práctica.
