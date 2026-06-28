---
ejercicio_id: fase-7/star-schema-medallion-diseno
fase: fase-7
sub_unidad: "7.5a"
version: 1
---

# Rúbrica — Diseñar un star schema + clasificar en capas medallion

> Rúbrica **analítica** para un ejercicio **a-mano** de diseño. Se evalúa la **calidad de las
> decisiones de modelado**, no la prosa. Un alumno puede copiar definiciones de un blog; otro puede
> declarar un grain inequívoco y justificar cada desnormalización contra su esquema. La rúbrica
> distingue ambos. El corrector **no** entrega el diseño: guía con pistas hasta que el alumno lo
> reconstruya.

## Objetivos evaluados

- **O1** — Diseñar un star schema (hechos + dimensiones) desde el OLTP, declarando el **grain** en una
  frase.
- **O2** — Clasificar transformaciones en bronze / silver / gold con justificación.
- **O3** — Decidir ELT vs ETL justificando por la **causa**, no por la sigla.

## Criterios y niveles

### C1 — Star schema y declaración del grain · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay grain declarado, o es ambiguo ("a nivel de curso/estudiante"); mezcla medidas con claves; copia el OLTP sin reorganizar. |
| **en-progreso** | Declara un grain plausible pero impreciso; identifica algunas dimensiones pero deja medidas en dimensiones o claves sueltas; no separa hechos de contexto con claridad. |
| **competente** | Grain en **una frase inequívoca** ("una fila = una inscripción de un estudiante a un curso"); `fact_inscripciones` separa **medidas** (`precio_pagado`, conteo) de **claves** (estudiante, curso, fecha); dimensiones coherentes (`dim_curso`, `dim_estudiante`, `dim_fecha`). |
| **excelente** | Además identifica que categoría e instructor son atributos **dentro de `dim_curso`** (no dimensiones del hecho), y razona el grain como **contrato** que evita doble conteo aguas arriba. |

### C2 — Desnormalización justificada · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No desnormaliza (replica el OLTP en 3NF con tablas puente), o desnormaliza sin explicar. |
| **en-progreso** | Desnormaliza algo pero la justificación es "porque sí" o "es lo que se hace". |
| **competente** | Al menos una desnormalización explícita (categoría/instructor dentro de `dim_curso`) con la razón: **menos joins por query de lectura sobre millones de filas**. |
| **excelente** | Contrasta explícitamente con el principio de F3: en OLTP normalizas para escribir seguro; aquí desnormalizas porque **cambió el objetivo** (minimizar joins de lectura), aceptando redundancia que se escribe poco y se lee mucho. |

### C3 — Clasificación medallion · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Clasifica al azar o no justifica; confunde bronze con "la fuente" o gold con "todo lo limpio". |
| **en-progreso** | La mayoría bien, pero confunde silver/gold (p. ej. pone la tabla resumen del dashboard en silver) o mete el transporte en bronze. |
| **competente** | T1→bronze, T3/T4/T6→silver, T2/T5→gold, con razón en media línea; reconoce que **T1 es lo más cercano a bronze tras el transporte** y que el resumen de gerencia (T5) es gold. |
| **excelente** | Nota que **T2 (star schema) y T5 (resumen)** son ambas gold pero con propósito distinto (modelo de consumo vs tabla pre-agregada para un dashboard), y que la deduplicación (T3) es la frontera que hace confiable a silver. |

### C4 — Decisión ELT vs ETL por su causa · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Elige sin justificar, o justifica con moda ("ELT porque es lo moderno"). |
| **en-progreso** | Elige ELT correctamente pero la causa es vaga. |
| **competente** | Elige **ELT** y lo justifica por la **causa**: compute del warehouse barato/elástico → cargar crudo y transformar después con SQL versionado; iterar métricas sin re-extraer. |
| **excelente** | Reconoce el matiz: ELT es el default **porque** se abarató el compute, pero nombra una condición (PII regulada, anonimizar antes de cargar) que justificaría ETL —muestra que entiende el trade-off, no un dogma. |

## Errores típicos a marcar

- **Grain ausente o ambiguo** — el error #1. Sin grain en una frase, todo el diseño es inestable.
- Tratar `categoria` e `instructor` como **dimensiones del hecho** en vez de atributos de `dim_curso`.
- Replicar el OLTP normalizado y llamarlo "star schema" (snowflake completo sin razón).
- Poner la tabla resumen del dashboard (T5) en silver "porque ya está limosa" en vez de gold.
- Meter el transporte (T-extracción) como si fuera bronze; bronze es el crudo **ya cargado**.
- Justificar ELT "porque es lo moderno" sin nombrar el costo de compute.
- (transversal) No mencionar que el grain/ELT debería quedar como **ADR** (spec-driven), ni el costo
  de re-computar agregaciones (costo/latencia), en una entrega que aspira a excelente.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Diseño con vocabulario impecable ("conformed dimensions", "slowly changing dimensions tipo 2") pero
  **sin atarlo al esquema de cursos dado** —como si describiera un caso genérico de blog.
- Grain perfecto en prosa pero medidas/claves mal separadas en la tabla concreta: señal de copiar la
  teoría sin aplicarla.
- **Verificación sugerida:** pedir que justifique, sobre **su** `dim_curso`, qué columna desnormalizó y
  desde qué tabla del OLTP vino; y que diga qué pasaría con el grain si una inscripción tuviera dos
  pagos. Si diseñó de verdad, responde al instante.

## Feedback sugerido (graduado)

> Nunca entregar el diseño completo antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "Empieza por una sola frase: *una fila de `fact_inscripciones` representa…*. Si
  no la puedes cerrar sin ambigüedad, ahí está el problema, no en las dimensiones."
- **Pregunta socrática (nivel 2):** "En F3 te dijeron que NO repitieras la categoría en cada fila.
  ¿Qué cambió aquí para que repetirla dentro de `dim_curso` sea lo correcto? ¿Qué optimizas ahora que
  antes no?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa en dos columnas tu tabla de
  hechos: *números que sumo* (medidas) y *hacia qué dimensión apunto* (claves). El instructor y la
  categoría no son ninguna de las dos a nivel de hecho: son atributos de `dim_curso`. Y para medallion,
  pregúntate por cada T si deja el dato crudo, confiable, o listo-para-consumo."

## Conexión con el proyecto / capstone

Este diseño es el plano que materializarás con dbt en
[7.5b](../../../src/content/docs/fase-7-automatizacion/7-5b-dbt.mdx) y el cimiento del contexto de
datos del capstone agéntico: el agente consulta cifras que salen de una tabla de hechos como la que
modelaste aquí. El grain y la decisión ELT/ETL son material directo de un **ADR** del capstone.
