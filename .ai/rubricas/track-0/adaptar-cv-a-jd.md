---
ejercicio_id: track-0/adaptar-cv-a-jd
fase: track-0
sub_unidad: "T0.7"
version: 1
---

# Rúbrica — Adapta tu CV y headline a una job description (keywords + ATS)

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio de
> adaptación**: extraer bien las keywords, ser honesto con el tengo/no-tengo, reflejar sin inflar, y
> conocer qué rompe un ATS. No hay un único CV correcto, pero sí criterios correctos: un alumno puede
> adaptar distinto y estar bien si lo justifica; puede "matchear" inflando y estar mal.

## Objetivos evaluados
- **O1** — Extraer keywords (must-have vs nice-to-have) y mapearlas honestamente contra lo que posee.
- **O2** — Adaptar header/summary/skills reflejando los términos de la oferta; nombrar lo que rompe un ATS.

## Criterios y niveles

### C1 — Extracto de keywords (must-have vs nice-to-have) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No separa must-have de nice-to-have, o pierde la mayoría de las keywords de la oferta. |
| **en-progreso** | Lista keywords pero mezcla ambas categorías, o confunde must-have (Python, FastAPI, RAG, English) con nice-to-have (LangGraph, n8n, Next.js). |
| **competente** | Separa correctamente must-have y nice-to-have y captura las principales de la JD. |
| **excelente** | Captura también keywords "blandas" implícitas (end-to-end ownership, on-call, specs/ADRs, "AI we can measure" = evals) además de las técnicas. |

### C2 — Honestidad del mapeo (tengo / no-tengo) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Marca todo como "tengo" sin criterio, o no marca. |
| **en-progreso** | Marca tengo/no-tengo pero infla (declara dominar algo que no tiene evidencia). |
| **competente** | Mapeo honesto: distingue lo que puede defender con un capstone de lo que no, incluyendo "parcial". |
| **excelente** | Liga cada "tengo" a una evidencia concreta (qué capstone lo prueba) y cada "no-tengo" a un plan de cierre de gap. |

### C3 — Header + summary + skills adaptados (reflejar, no inflar) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | CV genérico sin adaptar, o copia la JD entera (stuffing). |
| **en-progreso** | Adapta algo pero el título no refleja el énfasis de la oferta, o el summary no usa términos de la JD. |
| **competente** | Título de rol alineado al énfasis (agéntico/automatización), summary con términos literales de la JD que sí posee, Skills que espeja must-haves primero. |
| **excelente** | Rechaza explícitamente meter una keyword que no domina; el orden de Skills replica la prioridad de la oferta; coherencia con el header de GitHub (T0.6). |

### C4 — Conocimiento de ATS (formato) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra elementos ATS-rompedores, o nombra cosas irrelevantes. |
| **en-progreso** | Nombra 1-2 elementos sin explicar por qué rompen el parser. |
| **competente** | Nombra ≥3 (tablas/columnas, foto, headers no estándar, gráficos de nivel, info en header/footer) con la razón correcta (el ATS lee texto plano de arriba-abajo). |
| **excelente** | Explica el mecanismo (columnas se intercalan, imágenes no aportan texto, headers no estándar no matchean las etiquetas que el ATS busca) y conecta con la doble puerta ATS→humano. |

### C5 — Decisión de postulación y comunicación · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **competente** | Decisión clara (postular / postular marcando gap / no) justificada, conectada al pipeline de T0.2. |
| **excelente** | Decisión "stretch" calibrada: postula aunque le falte un nice-to-have, con un gap concreto a cerrar; todo en inglés correcto. |

## Errores típicos a marcar
- **Keyword stuffing:** meter en Skills toda keyword de la oferta, incluidas las que no domina → se cae en la entrevista técnica.
- **No adaptar:** entregar el CV genérico tal cual ("ya lo tengo hecho") → rankea peor en el ATS.
- **Título que no refleja el énfasis:** poner "Fullstack Developer" para una oferta que grita "agentic automation".
- **Confundir must-have con nice-to-have:** tratar LangGraph/n8n (nice) como obligatorio, o RAG/English (must) como opcional.
- **Formato no examinado:** no nombrar ningún elemento ATS-rompedor, o creer que "PDF bonito" siempre parsea.
- (transversal) ignorar que la oferta exige inglés profesional; entregar todo en español.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Extracto de keywords exhaustivo y perfecto pero el mapeo tengo/no-tengo es genérico o todo "sí" (no razonó su propio perfil).
- Header/summary pulidos que usan keywords que el alumno no puede explicar si se le pregunta.
- **Verificación sugerida:** pedir que tome una must-have que marcó como "tengo" y explique, sin notas, qué capstone la prueba y qué decisión técnica tomó ahí. Si la tiene, lo dice; si la stuffeó, se nota.

## Feedback sugerido (graduado)
> Nunca reescribir el CV por el alumno.
- **Pista (nivel 1):** "Cuenta cuántas de tus Skills puedes defender con un proyecto real. Las que no, ¿qué hacen ahí? Reflejar es honesto; inflar te quema en la entrevista."
- **Pregunta socrática (nivel 2):** "¿Cómo se nombra la empresa a sí misma en la oferta? Si repite 'agentic', 'act on external systems', 'human-in-the-loop', ¿tu header está apuntando a ese lane o a otro?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa must-have de nice-to-have, marca con honestidad qué tienes, y construye Skills solo con lo defendible, must-haves primero. Para el ATS: una columna, texto plano, headers estándar, sin foto."

## Conexión con el proyecto / capstone
- Cada oferta del pipeline de [T0.2] recibe una versión adaptada de este CV; el header debe coincidir con el de tu GitHub [T0.6]. El capstone del track es conseguir el trabajo: adaptar bien es lo que hace que el ATS deje pasar tu CV al humano que decide.
