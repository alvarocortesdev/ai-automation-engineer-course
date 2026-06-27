---
ejercicio_id: fase-6/precision-recall-f1
fase: fase-6
sub_unidad: "6.0"
version: 1
---

# Rúbrica — Precision, recall y F1 desde una verdad de referencia

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que más se evalúa aquí no es la aritmética (es simple), sino: (1) que los **casos borde** de denominador cero se manejen sin reventar, y (2) que el alumno entienda el **trade-off** precision/recall y por qué F1 es la media armónica. Una solución que pasa los tests pero cuyo autor no sabe cuándo priorizar recall **no** es excelente.

## Objetivos evaluados

- **O1** — Contar TP/FP/FN comparando etiquetas reales contra predichas.
- **O2** — Calcular precision, recall y F1 a partir de esos conteos, con sus casos borde.
- **O3** — Explicar el trade-off precision/recall y cuándo priorizar cada uno.

## Criterios y niveles

### C1 — Corrección del conteo y las métricas · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `contar` confunde FP con FN, o las fórmulas están invertidas (precision con FN, recall con FP); los tests no pasan. |
| **en-progreso** | El conteo es correcto pero alguna métrica usa el denominador equivocado, o `evaluar` no compone bien (recalcula a mano en vez de reusar). |
| **competente** | Todos los tests pasan: el ejemplo del RAG da precision 0.60, recall 0.75, F1 ≈ 0.667; `evaluar` devuelve el dict con las tres claves. |
| **excelente** | `evaluar` se apoya en `contar` + las tres funciones (no duplica lógica); nombres y estructura claros; F1 reusa precision y recall ya calculados. |

### C2 — Manejo de casos borde (denominador cero) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `precision(0,0)` o `f1(0,0)` lanzan `ZeroDivisionError`; el eval revienta con un modelo que no predice positivos. |
| **en-progreso** | Maneja un caso borde pero no todos (p. ej. protege precision pero no F1), o devuelve `None` en vez de `0.0`. |
| **competente** | Los tres denominadores cero devuelven `0.0`; `f1(1.0, 0.0)` devuelve `0.0` (no 0.5); distinto largo en `contar` lanza `ValueError`. |
| **excelente** | El patrón del caso borde es uniforme y legible (`x / y if y else 0.0`), y el alumno explica por qué `f1(1.0, 0.0)=0` es lo correcto (la armónica castiga el desequilibrio). |

### C3 — Comprensión del trade-off (el write-up calza con el razonamiento) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue precision de recall, o cree que "más alto siempre es mejor en ambas a la vez" sin ver la tensión. |
| **en-progreso** | Define precision y recall correctamente pero no da un ejemplo de cuándo priorizar uno sobre otro. |
| **competente** | Da un ejemplo defendible: recall alto para no perder positivos (cáncer, recuperar docs en RAG); precision alta cuando un falso positivo es caro (spam que oculta un correo real). |
| **excelente** | Conecta con accuracy: explica por qué engaña con clases desbalanceadas, y por qué por eso se usan precision/recall/F1 (hilo transversal: evals como ship-gate). |

## Errores típicos a marcar

- **FP y FN intercambiados** en `contar` (el error #1): revisar contra el caso `[1,1,0,1,0,0]` vs `[1,0,0,1,1,0]` → (2,1,1).
- **Fórmulas cruzadas**: precision usando FN, recall usando FP.
- **Denominador cero sin proteger**: `ZeroDivisionError` en vez de `0.0`.
- **F1 como promedio aritmético** `(p+r)/2` en vez de media armónica: `f1(1.0,0.0)` daría 0.5 (mal) en vez de 0.0.
- **Confiar en accuracy**: si en el write-up el alumno propone "medir con accuracy", marcar el problema de clases desbalanceadas.
- (transversal) No añadir el caso borde propio; persigue "que pase" sin entender qué fija cada test.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Importa `from sklearn.metrics import ...` pese a que se pide a mano: copió la respuesta sin hacer la operación.
- Implementación correcta pero el alumno no sabe responder "¿en spam prefieres precision o recall, y por qué?".
- Vocabulario avanzado (macro/micro-average, AUC) impropio del nivel, sin poder explicarlo: señal de plantilla genérica de IA.
- **Verificación sugerida:** dale un caso nuevo a mano (TP=3, FP=1, FN=6) y pídele precision y recall en voz alta. Si entendió, dice 0.75 y 0.33 razonando; si dependió de la IA, se traba o necesita correr código.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el código de la solución.**

- **Pista (nivel 1):** "Tu conteo está bien. Revisa qué denominador usa cada métrica: precision mira lo que *predijiste* positivo, recall mira los positivos *reales*. ¿Cuál de los dos comparte el numerador TP con un FP y cuál con un FN?"
- **Pregunta socrática (nivel 2):** "Si tu modelo predice un solo caso, acierta, y se pierde los otros nueve positivos: ¿qué precision tiene? ¿qué recall? ¿te parece un buen modelo? ¿Qué número debería 'castigar' eso, el promedio o F1?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu F1 usa `(p+r)/2`. Pruébalo con `p=1.0, r=0.0`: te da 0.5, como si el modelo fuera mediocre, cuando en realidad es inútil (no recupera nada). La media armónica `2pr/(p+r)` da 0 ahí: por eso es la correcta. Cámbiala y vuelve a correr el test de F1."

## Conexión con el proyecto / capstone

- Estas métricas son el **eval harness versionado** del **Capstone F6 (Plataforma RAG)** —entregable del Definition of Done (punto 5): el número que sube o baja entre versiones y que, en un gate de CI, **bloquea un deploy si el recall del retriever empeora**. Quien las calculó a mano sabe leer y defender ese número en una entrevista.
