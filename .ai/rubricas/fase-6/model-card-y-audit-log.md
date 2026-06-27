---
ejercicio_id: fase-6/model-card-y-audit-log
fase: fase-6
sub_unidad: "6.15"
version: 1
---

# Rúbrica — Model card + audit log a prueba de manipulación

> Rúbrica **analítica** atada a los `objetivos` del contrato. El código tiene un contrato
> verificable (los tests pasan o no); la model card es un documento donde se evalúa el
> **criterio** (out-of-scope y limitaciones honestas), no la prosa. El corrector lee la
> solución de referencia **al final**, tras formar su juicio.

## Objetivos evaluados

- **O1** — Audit log: redactar PII, encadenar con hash chain, verificar integridad.
- **O2** — Model card: uso previsto, out-of-scope, datos, evaluación, limitaciones, gobernanza.
- **O3** — Conectar gobernanza con observabilidad y privacidad (qué se loguea, qué no, por qué).

## Criterios y niveles

### C1 — Audit log correcto (tests verdes) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests rojos; o `verificar_cadena` solo mira los enlaces sin recomputar el hash (no detecta un campo manipulado). |
| **en-progreso** | Pasa la cadena íntegra pero no detecta tamper o reordenamiento; o `registrar` no valida campos requeridos. |
| **competente** | Todos los tests pasan: redacta email + dígitos, valida requeridos, encadena con prev_hash, y `verificar_cadena` detecta tamper y reordenamiento. |
| **excelente** | Además: hash determinista con JSON canónico (`sort_keys`), excluye `record_hash` del contenido hasheado de forma explícita, y añade un test propio significativo (cadena vacía, o tamper-con-recompute que rompe el enlace siguiente). |

### C2 — Privacidad: nunca PII en claro · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El registro guarda `input_text` crudo, o no redacta antes de loguear. |
| **competente** | El registro guarda solo `input_redacted`; el crudo no aparece; emails y dígitos largos quedan como `<REDACTADO>`. |
| **excelente** | Razona (en código o write-up) por qué loguear PII en claro crea un pasivo, y por qué los números cortos no se redactan (minimizar falsos positivos sin perder la señal). |

### C3 — Model card con criterio · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Campos vacíos o genéricos ("funciona bien, sin limitaciones"); sin out-of-scope. |
| **en-progreso** | Llena uso previsto y datos, pero los out-of-scope/limitaciones son vagos o copiados. |
| **competente** | Declara uso previsto, out-of-scope concretos ("no decide sobre personas", "no da consejo legal"), datos (corpus/fecha/PII), evaluación con números y limitaciones reales (alucina si falla el retrieval, cutoff). |
| **excelente** | Out-of-scope y limitaciones específicos del sistema (no plantilla); ata la evaluación a métricas desagregadas; sección de gobernanza con tier correcto (limitado → Art. 50) y alcance; escrita en inglés claro. |

### C4 — Tier de gobernanza y conexión · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No declara tier, o lo pone mal (un RAG de soporte como "alto riesgo" sin justificar). |
| **competente** | Tier limitado → Art. 50 (avisar que es una IA); resuelve el alcance extraterritorial; menciona el audit log como mecanismo de accountability. |
| **excelente** | Conecta `request_id` del audit log con la traza de observabilidad (5.10) y la evaluación con el eval harness (6.9); nombra al humano responsable. |

## Errores típicos a marcar

- `verificar_cadena` que **no recomputa** el hash → no detecta un campo editado (falso "íntegro").
- Incluir `record_hash` dentro del contenido que se hashea → imposible recomputarlo después.
- Guardar `input_text` crudo "por si acaso" → pasivo de privacidad.
- Hash no determinista (dict sin `sort_keys`, o incluir el orden de inserción).
- Model card con out-of-scope vacío o "ninguna limitación" (la sección que protege, ausente).
- Clasificar el RAG de soporte como alto riesgo sin que decida sobre personas.
- (transversal) perseguir que pase el happy-path sin el test de tamper; no añadir test propio.

## Señales de dependencia-IA

- Código con un esquema de hashing sofisticado (Merkle tree completo, firmas) impropio del
  nivel y que no se pidió, sin poder explicar el hash chain simple.
- Model card pulida y genérica idéntica a un template, sin out-of-scope específicos del sistema.
- **Verificación sugerida:** pídele que explique, sin notas, por qué editar el registro del
  medio rompe la verificación. Si lo razonó, habla de que el hash cambia y rompe el enlace del
  siguiente; si lo copió, repite "es como blockchain" sin el mecanismo.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca pegar el código de la solución.**

- **Pista (nivel 1):** "¿Tu `verificar_cadena` recomputa el `record_hash` de cada registro, o
  solo compara los `prev_hash`? Si solo mira los enlaces, ¿cómo detectarías que alguien editó
  un campo sin tocar los hashes?"
- **Pregunta socrática (nivel 2):** "Si `record_hash` se calcula sobre un contenido que
  **incluye** `record_hash`, ¿podrías volver a calcularlo igual después? ¿Qué tendrías que
  excluir?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Para que el hash sea
  determinista, serializa con `json.dumps(contenido, sort_keys=True)` y excluye `record_hash`
  del `contenido`. Para la model card, tus out-of-scope no pueden ser genéricos: di
  explícitamente que el sistema **no decide sobre personas** y **no es fuente sin cita**."

## Conexión con el proyecto / capstone

- Ambos artefactos son entregables de primera clase del
  [Capstone F6 (Plataforma RAG)](/fase-6-ai-engineering/proyecto/): el audit log enlaza con la
  [observabilidad](/fase-5-devops/5-10-observabilidad/) por `request_id`, y la model card cierra
  con los números del [eval harness (6.9)](/fase-6-ai-engineering/6-9-eval-driven-development/).
  El tier de gobernanza viene del ejercicio hermano `clasifica-y-gobierna`.
