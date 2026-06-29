---
ejercicio_id: track-0/evidencia-ai-augmented
fase: track-0
sub_unidad: "T0.9"
version: 1
---

# Rúbrica — Reframe + mapa de evidencia del skill AI-augmented

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio**: si
> el alumno entiende que el skill AI-augmented es *criterio con que diriges y verificas* (no velocidad ni
> abstinencia) y si sabe traducirlo a **evidencia abrible**. No hay un único reframe correcto, pero sí
> framings correctos e incorrectos: presumir velocidad o esconder el uso de IA es señal de no haberlo
> entendido.

## Objetivos evaluados
- **O1** — Explicar el framing honesto (multiplicador con criterio, no muleta) y diagnosticar un framing
  que resta.
- **O2** — Producir evidencia concreta y verificable: mapear los cuatro músculos a artefactos abribles.

## Criterios y niveles

### C1 — Diagnóstico del framing · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No clasifica el framing, o lo llama "AI-augmented" sin ver el problema (acepta la autodescripción como buena). |
| **en-progreso** | Identifica que "algo falla" pero no nombra el cuadro (vibe-coder) ni por qué resta en entrevista. |
| **competente** | Nombra el cuadro **vibe-coder** y explica por qué resta: velocidad sin criterio, indefendible, suena a alguien gobernado por la herramienta. |
| **excelente** | Además detecta la **oportunidad desperdida**: el candidato SÍ tiene material de criterio (escribió la lógica de pagos a mano, sabe programar) pero lo esconde por creer que "admitir que no usó IA lo hace ver mal" —exactamente al revés. |

### C2 — Narrativa reescrita (criterio, no velocidad; sin sobreventa ni ocultamiento) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Repite la sobreventa ("10x", "la IA hace todo") o vuela al otro extremo ("no uso IA"). |
| **en-progreso** | Mejora el tono pero sigue hablando de productividad/velocidad en vez de criterio; o es genérica ("uso IA responsablemente"). |
| **competente** | Habla de **criterio** (spec propio, review contra tests, evals, cuándo-NO), es verificable, y no sobrevende ni oculta. 4–6 frases decibles. |
| **excelente** | Conecta explícitamente con **Primero-Sin-IA** ("la uso para multiplicar, no para pensar"), reincorpora el dato escondido (la lógica de pagos sin IA) **como fortaleza**, y suena natural para decir en voz alta. |

### C3 — Mapa de evidencia (artefactos concretos y abribles) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Faltan músculos, o los "artefactos" son cualidades abstractas ("código limpio", "buenas prácticas"). |
| **en-progreso** | Cubre los 4 músculos pero algún artefacto es vago ("mis commits", "mi repo") sin decir *qué* commit/archivo. |
| **competente** | Los **4 músculos** mapeados, cada uno a un artefacto **abrible y específico** (un `spec.md` antes del código; un ADR de rechazo; un `evals/` con número y gate; un ADR de no-delegar). |
| **excelente** | Al menos un artefacto **ya existe** y lo enlaza a su repo del curso; distingue artefactos que tiene de los que va a crear (con dónde). |

### C4 — Honestidad sobre el músculo débil · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **competente** | Identifica con honestidad cuál músculo no podría demostrar hoy y propone un plan. |
| **excelente** | El músculo débil que nombra es coherente con su mapa (no dice "evals" si justo ahí puso el mejor artefacto), y el plan es accionable (qué artefacto, cuándo). |

## Errores típicos a marcar
- **Reframe que sigue vendiendo velocidad:** cambiar "10x" por "muy productivo" no es reframear; el eje es **criterio**, no rapidez.
- **Esconder el uso de IA:** virar al purista ("no la uso") por miedo a verse junior —desperdicia el skill y suena falso si el repo dice lo contrario.
- **Artefactos abstractos:** "código de calidad", "buenas prácticas" no son evidencia abrible; un reclutador no puede *abrir* eso. Exige archivo/commit/ADR concreto.
- **Olvidar el músculo cuándo-NO:** mapear solo spec/review/evals y saltarse el de abstención —es el más escaso y el insumo se lo regala (la lógica de pagos a mano).
- (transversal) no conectar con Primero-Sin-IA: el reframe gana mucho cuando dice que la IA multiplica pero no piensa por él.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Reframe pulido y "corporativo" pero genérico, que podría describir a cualquiera y no menciona ningún artefacto específico de SU repo.
- Mapa con artefactos plausibles pero que el alumno no podría señalar en su repo si se le pide abrirlos.
- **Verificación sugerida:** pedir que abra **uno** de los artefactos del mapa en su repo real, o que explique en una frase, sin notas, "por qué el skill se prueba y no se declara". Si lo interiorizó, le sale; si lo generó, vuelve a los adjetivos.

## Feedback sugerido (graduado)
> Nunca reescribir el reframe por el alumno.
- **Pista (nivel 1):** "Subraya cada frase de tu reframe que un reclutador NO podría verificar abriendo tu repo. Si sobreviven varias, todavía estás declarando, no probando."
- **Pregunta socrática (nivel 2):** "¿Tu narrativa habla de cuán rápido vas, o de cómo decides qué delegar y cómo verificas lo delegado? El candidato escribió la lógica de pagos sin IA y lo esconde: ¿eso es una debilidad que ocultar o tu mejor evidencia de criterio?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Reescribe empezando por el criterio: spec propio → review contra tus tests → evals con gate → un caso donde NO delegaste y por qué. Para el mapa, cada celda debe ser un archivo o commit que alguien pueda abrir; si no existe, anótalo como 'a crear' con su ruta. Y di la verdad sobre tu músculo más débil —esa honestidad es parte del skill."

## Conexión con el proyecto / capstone
- Este reframe es el guion del write-up de trade-offs de cualquier capstone de [T0.5] y la respuesta-ancla
  de la práctica de entrevista [T0.3]. El mapa de evidencia es, literalmente, el checklist de lo que debe
  existir en tus repos de [T0.6] para que el skill sea creíble. En remoto-USD, todo esto se dice en inglés
  ([T0.1]).
