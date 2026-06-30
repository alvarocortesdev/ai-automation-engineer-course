---
ejercicio_id: fase-6/puente-ml-dl
fase: fase-6
sub_unidad: "6.0b"
version: 1
---

# Rúbrica — Defiende tus fundamentos (modo entrevista)

> Rúbrica **analítica** para un ejercicio **a-mano** de razonamiento y comunicación. Lo que se evalúa es la **comprensión demostrada**: que el alumno pueda explicar y diagnosticar con un modelo mental correcto, no que coincida palabra por palabra con la solución de referencia. Un alumno puede usar analogías distintas y estar perfecto; otro puede recitar la definición correcta y delatar, en el ejemplo, que no entendió. La rúbrica distingue ambos.

## Objetivos evaluados
- **O1** — Explicar qué es un modelo, entrenar vs inferir, y de dónde salen los embeddings (vectores aprendidos).
- **O2** — Diagnosticar overfitting vs underfitting con números de train/test y justificar el split.
- **O3** — Explicar la intuición de self-attention con un ejemplo de ambigüedad propio.

> El corrector conoce las respuestas (ver solución de referencia) pero **no se las dicta** al alumno: da feedback graduado y pide que reformule, no entrega el texto.

## Criterios y niveles

### C1 — Modelo, entrenar/inferir, embeddings · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Define "modelo" como base de datos de respuestas o reglas; o confunde entrenar con inferir; o no responde de dónde salen los embeddings. |
| **en-progreso** | Sabe que un modelo tiene pesos y que hay dos fases, pero **no afirma** que en inferencia los pesos no cambian, o cree que el embedding es una propiedad fija del texto. |
| **competente** | Modelo = función con pesos ajustados a datos; entrenar = ajustar pesos / inferir = usarlos congelados (y al llamar una API se infiere); embedding = vector **aprendido**, salida de un modelo. |
| **excelente** | Además explica *por qué* no se mezclan embeddings de dos modelos (espacios distintos) y conecta "llamar a la API = inferir" con que la memoria entre mensajes es contexto, no aprendizaje. |

### C2 — Diagnóstico overfitting/underfitting · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Etiqueta los modelos al azar o sin mirar el gap; no explica por qué se separan los datos. |
| **en-progreso** | Acierta algún caso pero la justificación no usa el gap (train − test), o confunde overfitting (gap alto) con underfitting (ambos bajos). |
| **competente** | A = overfitting (gap ~27), B = underfitting (ambos bajos, sin gap), C = sano (altos y cercanos); justifica cada uno por el gap; explica el split como "medir en datos no vistos para no mentirse". |
| **excelente** | Propone acciones sensatas y específicas (A: más datos / regularización / early stopping, NO más épocas; B: modelo más rico / mejores features) y nombra el *generalization gap*. |

### C3 — Intuición de attention · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "El modelo entiende como un humano" o no logra explicar qué hace attention; sin ejemplo. |
| **en-progreso** | Idea vaga ("mira el contexto") sin ejemplo de ambigüedad o sin ninguna de las dos ventajas. |
| **competente** | Attention = cada token pondera a cuáles otros atender según el contexto (pesos por match), con un ejemplo de ambigüedad **propio** y **al menos una** ventaja (larga distancia / paralelización). |
| **excelente** | Menciona **ambas** ventajas y conecta el "match" con el producto punto de 6.0 (Query·Key); deja claro que es ponderación, no comprensión consciente. |

### C4 — Comprensión demostrada (el ejemplo calza con la definición)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Definiciones correctas pero ejemplos ausentes o que contradicen la definición. |
| **en-progreso** | Ejemplos genéricos o reciclados de la lección (trofeo/maleta), no propios. |
| **competente** | Cada concepto trae un ejemplo/analogía propio coherente con la definición. |
| **excelente** | Los ejemplos son ilustrativos y revelan transferencia (los aplica a su propio dominio: trabajo, HomeBase, etc.). |

## Errores típicos a marcar
- **"El LLM aprende de mis chats"**: confundir contexto (context window) con re-entrenamiento. En inferencia los pesos no cambian.
- **"Más entrenamiento siempre mejora"**: ignora overfitting; sobre-entrenar memoriza.
- **Embedding como propiedad del texto**: no reconoce que es salida de un modelo entrenado → de ahí el error de mezclar embeddings de modelos distintos.
- **Etiquetar por el número de train solo** (A "es bueno porque 99%") sin mirar el gap.
- **Antropomorfizar attention** ("entiende", "presta atención como yo"): es ponderación aprendida vía dot products.
- **Reusar el ejemplo del trofeo** en attention: el enunciado pide uno propio; señal de que copió en vez de razonar.
- (transversal) No conectar el train/test split con el hábito de **evals** (medir sobre lo no visto) pese a que es el mismo principio.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- Redacción pulida y "de manual" pero con un **ejemplo que no calza** con la definición (texto generado sin comprensión).
- Usa terminología avanzada (logits, softmax, multi-head) sin poder explicarla y sin que el enunciado la pida: sofisticación impropia del nivel del puente.
- Diagnóstico de A/B/C correcto pero **sin el cálculo del gap** ni justificación: resultado sin proceso.
- **Verificación sugerida:** pedir que explique en voz alta, con un ejemplo **nuevo en el momento**, por qué dos modelos de embeddings no se pueden mezclar, o que diagnostique un cuarto caso (p. ej. 88% train / 55% test). Si razonó de verdad, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca entregar la explicación redactada. Empujar a que el alumno la reconstruya.
- **Pista (nivel 1):** "Revisa tu respuesta 2: cuando llamas a la API, ¿los pesos del modelo cambian o no? Esa única frase decide si el resto de tu mapa mental es correcto."
- **Pregunta socrática (nivel 2):** "Si un modelo da 99% en train y 72% en test, ¿qué te dice la **diferencia** entre esos dos números, más que cada número por separado? ¿Y qué pasaría si solo hubieras mirado el train?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu explicación de embeddings los trata como algo fijo del texto. Reescríbela partiendo de *cómo se obtienen*: ¿quién produce ese vector? ¿Existía antes de entrenar? De ahí sale, gratis, por qué no se mezclan entre modelos."

## Conexión con el proyecto / capstone
- Estos fundamentos sostienen el **Capstone F6 — Plataforma RAG**: saber que el sistema **infiere** (no aprende), elegir el modelo de embeddings con criterio (no mezclar espacios), y entender que el eval harness mide generalización (train/test split a escala de sistema). Es también la base de toda respuesta de entrevista sobre IA (T0.3).
