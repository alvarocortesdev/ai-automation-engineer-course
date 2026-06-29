---
ejercicio_id: track-0/curaduria-portafolio
fase: track-0
sub_unidad: "T0.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de **curaduría**: hay
> una selección de referencia, pero el alumno puede defender variantes razonables —lo que se mide es el
> **criterio**, sobre todo el repo trampa y la defensa de la estrella.

# Solución de referencia — Cura el portafolio: mata el 80% idéntico

## Clasificación de referencia (señal vs ruido)

| # | Repo | Veredicto | Por qué |
|---|---|---|---|
| 1 | `todo-app-react` | **ruido** | Tutorial de YouTube; lo tiene cualquiera, no demuestra juicio. |
| 2 | `weather-dashboard` | **ruido** | Clon de curso; consume una API, sin decisión propia. |
| 3 | `100-days-of-code` | **ruido** | Mini-scripts de un challenge; ejercicio, no proyecto. |
| 4 | `ticket-triage-agent` | **señal** ★ | Propio; decide y **actúa**, con HITL y manejo de fallas. La estrella. |
| 5 | `pdf-chatbot` | **ruido (trampa)** | RAG-de-tutorial: parece "de IA" pero es el "hola mundo" copiado, sin eval ni reranking. No diferencia. |
| 6 | `rag-knowledge-platform` | **señal** | Propio; RAG **de producción** (reranking, ragas, observabilidad, desplegado). |
| 7 | `nextjs-starter-fork` | **ruido** | Fork sin cambios reales; no es trabajo propio. |
| 8 | `homehub` | **señal** | Propio; fullstack en uso real con tests y CI/CD. |
| 9 | `crypto-price-tracker` | **ruido** | Script de tutorial. |

## Vitrina de referencia (2-3) y archivo

- **En la vitrina:** `ticket-triage-agent` (estrella), `rag-knowledge-platform`, `homehub`.
- **Archivar/esconder:** 1, 2, 3, 5, 7, 9. No se borran necesariamente (puede haber código reutilizable),
  pero **salen del perfil** para no diluir la señal.

## La estrella: por qué el agéntico

`ticket-triage-agent` va de pin #1 porque:
1. Demuestra el **otro pilar** del rol ("Automation Engineer"), no solo "sé usar un LLM".
2. Es lo que el RAG genérico **no puede** mostrar: un sistema que **decide y actúa en el mundo**.
3. El **manejo de fallas** (validación de salida antes de ejecutar, HITL para acciones sensibles,
   least-privilege, techo de costo) es justo la madurez que separa semi-senior de "pegué llamadas a una
   API". Es lo más difícil de fakear.

El RAG de producción (#6) es la **segunda** estrella —sólido, pero "RAG" es lo que el reclutador ve en cada
portafolio; diferencia menos. HomeHub tercero, como prueba de amplitud fullstack.

## Mapeo a skills del mercado (referencia)

| Proyecto | Skill del hiring manager |
|---|---|
| `ticket-triage-agent` | orquestación de LLMs + manejo de fallas + integración de sistemas |
| `rag-knowledge-platform` | retrieval, evaluación (ragas) y observabilidad de IA |
| `homehub` | fullstack TS + CI/CD + estados completos (a11y) |

## El "80% idéntico" (referencia)

Los repos descartados comparten que **los tiene cualquiera**: salen del mismo puñado de tutoriales, no
demuestran decisiones propias, y son intercambiables entre miles de candidatos. No solo no suman: **restan**,
porque en el escaneo de 10 s bajan la calidad percibida promedio de los buenos. Curar es esconder el ruido
para que la señal se vea.

## Puntos donde el corrector debe mirar
1. **El repo trampa (`pdf-chatbot`).** Es el discriminador del ejercicio: muchos lo dejan en la vitrina por
   ser "de IA". Que sea RAG no lo hace señal; que sea **de tutorial, sin eval ni reranking**, lo hace ruido.
   Detectarlo y explicarlo = `excelente` en C1.
2. **Estrella mal elegida.** Pinear el RAG (#6) o un tutorial por encima del agéntico indica que no captó el
   argumento "decide + actúa + maneja fallas".
3. **"Más es mejor".** Dejar 5+ repos visibles contradice "profundidad sobre volumen".
4. **Mapeo a tecnologías, no skills.** "Python/React" en vez de la capacidad que el proyecto prueba.

## Rango de soluciones aceptables
- Defender `homehub` como segunda estrella en vez del RAG es aceptable si el argumento es bueno (amplitud
  fullstack vs profundidad IA) —siempre que el agéntico siga siendo #1.
- Mantener `pdf-chatbot` visible es aceptable **solo** si el alumno lo replantea explícitamente como "RAG de
  producción" con eval/reranking (es decir, deja de ser el de tutorial). Mantenerlo tal cual = error.
- Una vitrina de 2 (sin HomeHub) es válida si se justifica enfoque en los dos pilares (IA + automatización).
