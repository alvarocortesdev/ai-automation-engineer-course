---
ejercicio_id: fase-5/mapeo-primitivos-azure
fase: fase-5
sub_unidad: "5.6"
version: 1
---

# Rúbrica — Mapea una app de IA a primitivos de Azure

> Rúbrica **analítica** atada a los `objetivos` del contrato. No hay test automático: **el `mapeo.md`
> es el corazón** y se corrige por la calidad del razonamiento, no por una respuesta única. Distintas
> elecciones de servicio pueden ser correctas si la justificación (perfil de carga, costo, seguridad)
> es sólida.

## Objetivos evaluados

- O1: Mapear cada componente a su primitivo (5.5) y al servicio Azure correcto, con justificación.
- O2: Decidir serverless (Functions) vs. compute sostenido (App Service) por el perfil de carga.
- O3: Defender dos trade-offs con argumento de costo/seguridad/latencia, no marketing.

## Mapeo de referencia (checklist del corrector)

> No es la única respuesta válida; es el ancla para detectar huecos.

- Recepción de email a ráfagas → **serverless / Functions** (escala a cero entre emails).
- Clasificación → **inferencia / Azure OpenAI** (llamada a LLM).
- Búsqueda en KB → **búsqueda-DB / Azure AI Search** *o* **pgvector** (según volumen).
- Generación del borrador → **inferencia / Azure OpenAI**.
- API web para agentes (tráfico sostenido) → **compute / App Service**.
- Almacenamiento de tickets → **storage / Blob Storage** (o una DB administrada).
- IAM transversal → **Managed Identity / Entra ID** (sin claves).

## Criterios y niveles

### C1 — Mapeo correcto (primitivo + servicio + porqué) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 5 componentes, o servicios sin primitivo, o "porque es de Azure" como única razón. |
| **en-progreso** | Mapea casi todo pero confunde un primitivo (p. ej. pone la API en Functions) o no justifica. |
| **competente** | ≥5 componentes con primitivo + servicio + una razón ligada al perfil de carga. |
| **excelente** | Todo mapeado, con IAM explícito y al menos un caso "compro vs. construyo" bien argumentado. |

### C2 — Serverless vs. compute (juicio de carga) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Todo en un solo servicio, o no distingue evento de tráfico sostenido. |
| **en-progreso** | Separa Functions y App Service pero la razón es vaga ("uno es más nuevo"). |
| **competente** | Ingest/clasificación por evento → Functions; API → App Service; con el porqué (ráfaga vs. sostenido). |
| **excelente** | Razona escala-a-cero/costo y latencia de cold start, y dónde eso cambiaría la decisión. |

### C3 — Trade-offs defendidos · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay trade-offs, o son afirmaciones de marketing ("Azure es seguro"). |
| **en-progreso** | Dos trade-offs pero con un solo lado, sin el escenario donde gana el otro. |
| **competente** | Dos trade-offs con ambos lados y el escenario que inclina cada uno (costo/seguridad/latencia). |
| **excelente** | Cuantifica o ejemplifica (PTU con tráfico alto/predecible; pgvector con KB pequeña ya en Postgres) y nombra el riesgo de vendor lock-in. |

## Errores típicos a marcar

- "Úsalo porque es de Azure": vendor lock-in disfrazado de decisión. Debe pesar costo/features/volumen.
- Poner la API web en Functions (cold start + tráfico sostenido = mala elección) o el ingest en App Service (pagar encendido por una ráfaga).
- Tratar Managed Identity y "clave en variable de entorno" como equivalentes (la identidad elimina el secreto; la variable solo lo esconde).
- Olvidar el IAM en el diagrama (no marca ninguna relación de Managed Identity).
- Decir "AI Search siempre" sin reconocer que pgvector puede ser más barato/simple en volúmenes chicos.

## Señales de dependencia-IA

- Lista exhaustiva y perfecta pero **sin un solo "no usaría X aquí"** propio (la IA rara vez se contradice a sí misma).
- Trade-offs genéricos y simétricos sin un escenario concreto del brief.
- Usa nombres de servicio muy nuevos pero no puede explicar a qué primitivo corresponden.
- Diagrama impecable que no calza con la tabla (señal de dos fuentes pegadas).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Para cada componente, ¿corre por un evento o atiende tráfico sostenido? Eso decide Functions vs. App Service. ¿Marcaste el IAM en el diagrama?"
- **Pregunta socrática (nivel 2):** "Si los emails llegan 30 veces al día y la API la consultan todo el día, ¿por qué tendría sentido tenerlos en servicios distintos? ¿Qué pagas en cada caso?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El ingest por email es serverless (Functions, escala a cero); la API es compute sostenido (App Service). Para el trade-off de PTU, ánclalo en tráfico alto y predecible; para AI Search vs. pgvector, en el volumen de la KB. Revisa la tabla del 4.1 y el 4.5."

## Conexión con el proyecto / capstone

- Es el paso de diseño antes de construir: el alumno aprende a posar una app sobre Azure con criterio, de modo que el Capstone F5 (si elige Azure) no sea "servicios al azar" sino decisiones defendibles con ADRs.
