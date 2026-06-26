---
ejercicio_id: fase-3/nestjs-vs-fastapi-decidir
fase: fase-3
sub_unidad: "3.10"
version: 1
---

# Rúbrica — Decide: FastAPI, NestJS o Express

> Rúbrica **analítica** de un ejercicio de **razonamiento**. No hay respuesta única: se evalúa la **calidad del criterio**, no qué framework eligió. Una elección "rara" bien defendida con criterios y trade-offs vale más que la "esperada" justificada con un eslogan. Los errores a marcar son decidir por moda ("NestJS es más profesional") o por chovinismo de lenguaje ("Python es mejor").

## Objetivos evaluados
- **O1** — Decidir con criterios concretos (lenguaje del equipo/sistema, tamaño, IA, estructura necesaria).
- **O2** — Nombrar el trade-off de cada elección y qué evidencia la cambiaría.
- **O3** — Defender FastAPI por ecosistema en una app de IA en Python, sin chovinismo de lenguaje.

## Criterios y niveles

### C1 — Calidad del criterio de decisión · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige por eslogan ("más moderno", "más profesional", "mejor lenguaje") o sin justificar. No aparece el criterio del **lenguaje del equipo/sistema**. |
| **en-progreso** | Justifica con algún criterio real pero superficial (solo "es de Node" / "es de Python") sin atarlo al contexto de cada escenario (RAG, 40 endpoints, webhook chico). |
| **competente** | Cada decisión se apoya en criterios pertinentes: lenguaje/ecosistema del equipo (no forzar cambio de lenguaje), tamaño y número de dominios (estructura vs simplicidad), e integración con IA. Las tres son defendibles. |
| **excelente** | Además expone una **tensión** explícita donde la elección no es obvia (típicamente B —¿Express con estructura propia o NestJS?— o un caso límite) en vez de fingir que todo es trivial. |

### C2 — Trade-offs y evidencia que cambia la decisión · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Vende su elección como perfecta; no nombra ningún costo ni qué lo haría cambiar. |
| **en-progreso** | Menciona un costo genérico ("tiene curva de aprendizaje") sin atarlo al escenario, o solo en uno de los tres. |
| **competente** | Cada escenario nombra un costo real (NestJS: ceremonia/curva; Express: tienes que inventar la estructura; FastAPI: no comparte tipos con un front TS) y un dato que cambiaría la decisión. |
| **excelente** | Los costos son específicos del caso y la evidencia-que-cambia-la-decisión es accionable (p. ej. "si la fintech planeara extraer microservicios en Go, reconsideraría el monolito NestJS"). |

## Errores típicos a marcar
- **Decidir por moda/popularidad** ("NestJS es lo que se usa", "todos están en X").
- **Chovinismo de lenguaje** ("Python/TS es superior") en vez de "el equipo y el sistema ya están en ese lenguaje".
- **NestJS para el webhook chico (C)** "porque es más profesional": es overkill; señal de no entender el costo de la estructura.
- **Forzar FastAPI en el equipo 100% TS (B)** "porque Python es mejor": el framework no debería justificar reescribir el stack.
- **Vender una opción como perfecta**: no nombrar ningún costo es la señal #1 de razonamiento inmaduro.
- **No reconocer ninguna ambigüedad** en los tres.
- (transversales) ausencia de un solo trade-off defendible; confundir "lo que yo sé usar" con "lo correcto para el proyecto".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Texto pulido que recita ventajas genéricas de cada framework (copiables de cualquier comparativa) sin aterrizarlas en RAG/40-endpoints/webhook.
- Tres decisiones "de manual" sin una sola tensión ni costo específico — sospechosamente limpias.
- **Verificación sugerida:** pedir el contrafactual del escenario A: "¿qué tendría que ser verdad para que NestJS fuera la mejor opción en la plataforma RAG?". Quien razonó puede construirlo (p. ej. que el equipo fuera TS y el RAG se sirviera vía un SDK Node maduro); quien copió se queda sin material.

## Feedback sugerido (graduado)
> Es razonamiento: el feedback empuja a defender mejor, no a "la respuesta correcta". **Nunca dar la solución.**
- **Pista (nivel 1):** "¿Cuál es el primer criterio que descarta media decisión casi siempre? Pista: tiene que ver con en qué lenguaje ya vive el equipo y el resto del sistema."
- **Pregunta socrática (nivel 2):** "Para la plataforma RAG en Python, ¿qué pierdes si metes un backend Node en un stack Python de IA? ¿Y qué te da NestJS en la fintech de 40 endpoints que Express te obligaría a construir a mano?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El eje dominante es el lenguaje/ecosistema del equipo y el tamaño del proyecto, no una superioridad técnica abstracta. Reescribe cada decisión añadiendo (a) el criterio que más pesó y (b) un costo concreto de tu elección."

## Conexión con el proyecto / capstone
- Esta decisión es justo un **ADR** del Capstone F3 (la elección del framework de backend). Poder escribir "elegí FastAPI sobre NestJS porque el stack es Python y sirvo IA, aceptando dejar fuera el ecosistema Node" es el tipo de trade-off defendible que pide el Definition of Done de la fase.
