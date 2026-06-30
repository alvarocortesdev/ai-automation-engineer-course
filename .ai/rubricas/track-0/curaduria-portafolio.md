---
ejercicio_id: track-0/curaduria-portafolio
fase: track-0
sub_unidad: "T0.5"
version: 1
---

# Rúbrica — Cura el portafolio: mata el 80% idéntico

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio de
> curaduría**: por qué este repo es señal y aquel es ruido, por qué esta es la estrella, y si el alumno
> detecta el repo trampa. No hay una única selección "correcta", pero sí criterios correctos. Un alumno
> puede elegir una vitrina distinta y estar bien si **justifica** con el criterio adecuado; puede elegir la
> "correcta" por la razón equivocada y estar mal.

## Objetivos evaluados
- **O1** — Curar (señal vs ruido), justificar la profundidad sobre el volumen, nombrar el "80% idéntico".
- **O1b** — Defender la estrella (agéntico por encima del RAG genérico).
- **O2** — Mapear cada sobreviviente a una *skill* concreta del mercado.

> Curaduría de referencia (el corrector la conoce; **no la entrega como atajo**): vitrina =
> `ticket-triage-agent` (estrella), `rag-knowledge-platform`, `homebase`. Ruido a archivar: 1, 2, 3, 5, 7, 9.
> Repo trampa: `pdf-chatbot` (#5) —tiene "IA"/chatbot pero es un RAG-de-tutorial, ruido disfrazado de señal.

## Criterios y niveles

### C1 — Clasificación señal vs ruido · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No clasifica todos los repos, o clasifica sin justificar (etiqueta sin criterio). |
| **en-progreso** | Clasifica los 9 pero confunde el repo trampa (`pdf-chatbot`) con señal por ser "de IA", o marca como ruido un proyecto propio sólido. |
| **competente** | Los 9 clasificados con justificación coherente; los 3 propios como señal, los tutoriales como ruido. |
| **excelente** | Además detecta y nombra el repo trampa (`pdf-chatbot`): un RAG-de-tutorial que *parece* señal y explica por qué no diferencia. |

### C2 — Selección y estrella (profundidad > volumen) · mapea: O1, O1b
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Deja casi todo en la vitrina ("más es mejor"), o no elige estrella. |
| **en-progreso** | Reduce a 2-3 pero la justificación de la estrella es débil ("es el más nuevo", "me gustó más") sin el argumento de diferenciación. |
| **competente** | Vitrina de 2-3, resto archivado explícitamente; elige el agéntico de estrella y argumenta por qué encabeza. |
| **excelente** | Defiende el agéntico vs el RAG con el argumento fuerte: demuestra *decidir + actuar + manejar fallas*, lo que el RAG genérico no puede; conecta "curar es decir que no" con la señal percibida en 10 s. |

### C3 — Mapeo a skills del mercado · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No mapea, o mapea a tecnologías sueltas ("Python", "React") sin la skill que prueban. |
| **en-progreso** | Mapea pero de forma genérica ("hace IA", "es fullstack") sin el lenguaje de una oferta real. |
| **competente** | Cada sobreviviente mapeado a una skill concreta y verosímil de una oferta (p. ej. "orquestación de LLMs con manejo de fallas"). |
| **excelente** | Conecta el mapeo con los gaps del funnel de T0.2 (destaca lo que el mercado pidió) y descarta de la vitrina lo que no mapea a nada pedido. |

### C4 — Comprensión demostrada (el "80% idéntico") · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra el patrón, o lo confunde con "tener pocos proyectos". |
| **en-progreso** | Lo menciona pero superficial ("son tutoriales") sin el porqué de la *invisibilidad*. |
| **competente** | Nombra el patrón: los repos descartados los tiene cualquiera, no demuestran juicio, y diluyen la señal. |
| **excelente** | Liga el patrón a la mecánica del escaneo de 10 s y al promedio percibido: el ruido baja la calidad percibida de los buenos. |

## Errores típicos a marcar
- **Confundir el repo trampa** (`pdf-chatbot`) con señal por ser "de IA": el error central del ejercicio.
- **"Más es mejor"**: dejar 5-9 repos en la vitrina porque "muestran trabajo".
- **Estrella mal elegida**: pinear el RAG genérico o un tutorial por encima del agéntico.
- **Mapeo a tecnologías, no a skills**: "Python/React" en vez de la capacidad que el proyecto prueba.
- **Justificación ausente**: clasificar sin una línea de porqué (etiqueta sin criterio).
- (transversal) ignorar el README en inglés como factor de "muestra-bilidad" para roles remoto-USD.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Una curaduría perfecta pero con justificaciones genéricas que no podrían venir de *razonar* cada repo
  (texto plantilla que calza con cualquier portafolio).
- Detecta el repo trampa pero no puede explicar *por qué* un RAG-de-tutorial no diferencia si se le pide.
- **Verificación sugerida:** pedir que cure un portafolio distinto de 6 repos inventado al momento, o que
  defienda en voz alta por qué archivaría `100-days-of-code`. Si curó de verdad, lo resuelve; si dependió
  de la IA, se traba en el criterio.

## Feedback sugerido (graduado)
> Nunca dar la curaduría de referencia antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Revisa el repo #5 otra vez. Tiene 'chatbot' en el nombre, pero ¿lo construiste tú
  con criterio propio, o lo tiene cualquiera que vio el mismo tutorial?"
- **Pregunta socrática (nivel 2):** "De tus tres proyectos propios, ¿cuál es el más difícil de *fakear*?
  ¿Cuál demuestra que tu sistema decide y actúa, no solo que responde preguntas? ¿Por qué eso importa más
  para un rol de Automation Engineer?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El criterio que falta es 'profundidad sobre
  volumen': el ruido no es neutral, baja la señal percibida de tus buenos proyectos en el escaneo de 10 s.
  Reclasifica archivando todo tutorial y vuelve a justificar la estrella con el argumento agéntico-vs-RAG."

## Conexión con el proyecto / capstone
- El capstone del track-0 es **conseguir el trabajo**. Curar bien es lo que hace que tus capstones técnicos
  (F6/F7) se vean; alimenta directamente [T0.6 GitHub profesional] (pins) y [T0.7 CV] (qué destacar).
