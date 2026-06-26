---
ejercicio_id: fase-3/prisma-ts-decidir-orm
fase: fase-3
sub_unidad: "3.6"
version: 1
---

# Rúbrica — Decide: Prisma o SQLAlchemy para tres proyectos

> Rúbrica **analítica** de un ejercicio de **razonamiento**. No hay respuesta única: se evalúa la **calidad del criterio**, no qué ORM eligió. Una elección "rara" bien defendida con criterios y trade-offs vale más que la elección "esperada" justificada con un eslogan. El error a marcar es decidir por moda ("Prisma es más moderno") o por chovinismo de lenguaje ("Python es mejor").

## Objetivos evaluados
- **O1** — Decidir con criterios concretos (lenguaje/equipo, control de SQL, ecosistema, IA).
- **O1b** — Nombrar el trade-off de cada elección y qué evidencia la cambiaría.

## Criterios y niveles

### C1 — Calidad del criterio de decisión · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige por eslogan ("más moderno", "más popular", "mejor lenguaje") o sin justificar. No aparece el criterio del **lenguaje del equipo**. |
| **en-progreso** | Justifica con algún criterio real pero superficial (solo "es de Node" / "es de Python") sin conectar con el contexto concreto de cada escenario (Next.js, RAG, legacy). |
| **competente** | Cada decisión se apoya en criterios concretos y pertinentes: lenguaje del equipo (el ORM no fuerza cambiar de lenguaje), ecosistema (Next.js↔Prisma, IA-Python↔SQLAlchemy), y necesidad de control de SQL. Las tres elecciones son defendibles. |
| **excelente** | Además, en el escenario ambiguo (típicamente el 2 o un caso límite) expone la **tensión** explícitamente (Prisma es más cómodo, pero el ecosistema Python y las queries vectoriales empujan a SQLAlchemy) en vez de fingir que es obvio. |

### C2 — Trade-offs y evidencia que cambia la decisión · mapea: O1b
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Vende su elección como perfecta; no nombra ningún costo. No dice qué lo haría cambiar de opinión. |
| **en-progreso** | Menciona un costo genérico ("tiene curva de aprendizaje") sin atarlo al escenario, o solo en uno de los tres. |
| **competente** | Cada escenario nombra un costo real de la elección (Prisma: menos control fino del SQL; SQLAlchemy: curva más empinada, menos type-safety automática) y un dato que cambiaría la decisión. |
| **excelente** | Los costos son específicos del caso (p. ej. "en el RAG, si Prisma no soporta bien el operador de `pgvector` que necesito, el SQL crudo me obliga a `$queryRaw` y pierdo parte de la ventaja") y la evidencia-que-cambia-la-decisión es accionable. |

## Errores típicos a marcar
- **Decidir por moda o popularidad** ("Prisma es lo nuevo", "todos usan X") en vez de por contexto.
- **Chovinismo de lenguaje** ("Python/TS es superior") en vez de "el equipo ya está en ese lenguaje".
- **Vender una opción como perfecta**: no nombrar ningún costo es la señal #1 de razonamiento inmaduro.
- **Forzar un cambio de lenguaje** por el ORM (recomendar SQLAlchemy a un equipo 100% TS "porque es más serio"): el ORM raramente justifica reescribir el stack.
- **No reconocer ninguna ambigüedad**: tratar los tres como obvios delata que no pensó las tensiones.
- (transversales) ausencia de un solo trade-off defendible; confundir "lo que yo sé usar" con "lo correcto para el proyecto".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Texto pulido que recita ventajas genéricas de cada ORM (copiables de cualquier comparativa) pero sin aterrizarlas en los detalles de cada escenario (Next.js, pgvector, legacy Node).
- Tres decisiones "de manual" sin una sola tensión ni costo específico — sospechosamente limpias.
- **Verificación sugerida:** pedir, en voz alta, "defiéndeme la elección opuesta en el escenario 2: ¿qué tendría que ser verdad para que Prisma fuera la mejor opción en un servicio de IA?". Quien razonó puede argumentar el contrafactual; quien copió se queda sin material.

## Feedback sugerido (graduado)
> Es razonamiento: el feedback empuja a defender mejor, no a "la respuesta correcta".
- **Pista (nivel 1):** "¿Cuál es el primer criterio que descarta media decisión casi siempre? Pista: tiene que ver con en qué lenguaje ya trabaja el equipo."
- **Pregunta socrática (nivel 2):** "Para el servicio de IA en Python, ¿qué pierdes si metes un ORM de Node en un stack Python? ¿Y qué te da el ecosistema Python que el cliente type-safe de Prisma no compensa?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El eje dominante es el lenguaje/ecosistema del equipo, no una superioridad técnica abstracta. Reescribe cada decisión añadiendo (a) el criterio que más pesó y (b) un costo concreto de tu elección."

## Conexión con el proyecto / capstone
- Esta decisión es justo un **ADR** del Capstone F3 (la elección de la capa de datos). Poder escribir "elegí SQLAlchemy sobre Prisma porque el stack es Python y sirvo IA, aceptando perder el cliente type-safe" es el tipo de trade-off defendible que pide el Definition of Done de la fase.
