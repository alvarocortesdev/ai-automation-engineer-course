---
ejercicio_id: fase-6/break-even-finetuning-vs-prompt
fase: fase-6
sub_unidad: "6.13"
version: 1
---

# Rúbrica — ¿A qué volumen se paga el fine-tuning? (break-even por costo)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **mixto**: hay
> respuesta correcta para el código, pero lo que de verdad se evalúa es el **proceso**
> (predijo a mano antes de medir) y la **comprensión** (entiende que sin ahorro por request
> no hay equilibrio). No basta con tests verdes.

## Objetivos evaluados

- **O1** — Calcular el costo por request del baseline y del fine-tuneado a partir de tokens y pricing por millón.
- **O2** — Calcular el punto de equilibrio en requests donde el fine-tuning iguala al baseline.
- **O3** — Explicar por qué si el fine-tuneado no es más barato por request, el fine-tuning nunca gana por costo.

## Criterios y niveles

### C1 — Corrección de las funciones · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Funciones sin implementar, o fórmula del costo por request mal (p. ej. `/ 1000` en vez de `/ 1e6`, o un solo precio para in y out). |
| **en-progreso** | El costo por request funciona pero el equilibrio está mal (no resta el costo del fine-tuneado, o divide por el costo total en vez del ahorro). |
| **competente** | Las tres funciones pasan todos los tests; el equilibrio = costo_entrenamiento / (c_base − c_ft). |
| **excelente** | `costo_total` se reusa para baseline y fine-tuning (DRY, costo_fijo parametrizado); maneja el ValueError con un mensaje claro, no un `ZeroDivisionError` crudo. |

### C2 — Manejo del caso "no hay equilibrio" · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Deja reventar `ZeroDivisionError`, o devuelve `inf`/negativo en silencio cuando el ahorro es <= 0. |
| **competente** | Lanza `ValueError` explícito cuando el ahorro por request (baseline − ft) es <= 0. |
| **excelente** | En `verificacion.md` explica el **significado de negocio**: un fine-tuneado más caro por token nunca recupera el costo de entrenamiento, por mucho volumen que haya. |

### C3 — Proceso Primero-Sin-IA (predicción antes de medir) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o se nota escrito después de correr los tests (números calcados sin razonamiento). |
| **competente** | `prediccion.md` tiene los cálculos a mano (costo por request de cada lado, ahorro, equilibrio = 50.000) y el ganador a 20.000 requests, con una línea de razonamiento por paso. |
| **excelente** | Predice correctamente que a 20.000 requests gana el **baseline** (aún no se amortiza el entrenamiento) y lo justifica con la posición frente al equilibrio. |

### C4 — Comprensión demostrada (la reflexión calza) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `verificacion.md` ausente o dice "fine-tuning es más barato" sin matiz. |
| **competente** | Explica que el fine-tuning solo gana por costo a volumen alto y sostenido, y solo si ahorra por request; nombra una razón no-costo (formato/estilo/consistencia) para fine-tunear igual. |
| **excelente** | Conecta con el híbrido de la lección: el fine-tuning por costo se decide con un número (el equilibrio), no con intuición, y se confirma con evals (6.9). |

## Errores típicos a marcar

- `/ 1000` en vez de `/ 1e6` (costo 1000× inflado) → `test_costo_por_request_baseline` lo atrapa.
- Un solo precio para in y out, o promediarlos: pasa de casualidad cuando in == out, no aquí.
- Dividir por el **costo total** del fine-tuneado en vez de por el **ahorro** (baseline − ft).
- Olvidar el costo fijo de entrenamiento en `costo_total` del lado fine-tuning.
- Dejar `ZeroDivisionError` o devolver `inf` cuando el ahorro es <= 0 (debe ser `ValueError`).
- En la reflexión, confundir "por encima del equilibrio" (gana fine-tuning) con lo contrario.
- (transversal) tests verdes pero `prediccion.md` escrito a posteriori → se saltó el Primero-Sin-IA.

## Señales de dependencia-IA

- `costo_finetuning.py` impecable pero `prediccion.md` vacío o con números sin razonamiento
  (resolvió con IA y rellenó la predicción al final).
- Tests propios genéricos que no prueban nada nuevo (copia de los existentes).
- **Verificación sugerida:** pídele que explique, sin notas, qué pasa con el equilibrio si el
  modelo fine-tuneado cuesta más por token. Si lo entendió, dice "no hay equilibrio, el
  ahorro es negativo"; si lo copió, titubea o habla de "depende del volumen".

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca escribir el código por el alumno.**

- **Pista (nivel 1):** "El equilibrio se divide por el **ahorro** por request, no por el
  costo total del fine-tuneado. ¿Cuánto te ahorras en **cada** request al acortar el prompt?"
- **Pregunta socrática (nivel 2):** "Si el modelo fine-tuneado costara **más** por request
  que el baseline, ¿existe algún número de requests que recupere los 26 USD de
  entrenamiento? ¿Qué debería hacer tu función en ese caso?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu fórmula del equilibrio está
  bien; te falta el guardia: cuando `c_base − c_ft <= 0`, lanza `ValueError` en vez de dejar
  reventar la división. Y en la reflexión, recuerda que a 20.000 requests gana el baseline
  porque aún no llegaste a los 50.000 del equilibrio."

## Conexión con el proyecto / capstone

- Esta cuenta es la mitad cuantitativa del ADR de "por qué (no) fine-tuneamos" del
  [Capstone F6 (Plataforma RAG)](/fase-6-ai-engineering/proyecto/): el número del equilibrio
  justifica, con datos, no fine-tunear hasta cruzar cierto volumen. Alimenta el budget de
  costo/latencia de [6.16](/fase-6-ai-engineering/6-16-costo-latencia-llmops/) y se decide
  junto a un eval ([6.9](/fase-6-ai-engineering/6-9-eval-driven-development/)) que confirme
  que la calidad no empeora.
