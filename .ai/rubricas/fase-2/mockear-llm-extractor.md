---
ejercicio_id: fase-2/mockear-llm-extractor
fase: fase-2
sub_unidad: "2.11"
version: 1
---

# Rúbrica — Mockear el LLM: suite para un extractor de pedidos

> Rúbrica **analítica** atada a los `objetivos`. El producto no es "que pase
> verde": es una suite que prueba **el código que rodea al LLM** de forma
> determinista (con fakes), cubre las ramas de error y **caza el mutante**. El
> SUT es la verdad; si el alumno lo modificó, la evaluación se invalida. Señal
> clave de comprensión: el alumno entiende que **nada** de su suite prueba la
> calidad del modelo (eso es un eval).

## Objetivos evaluados
- **O1** — Tests deterministas con un fake/stub que devuelve respuestas fijas (sin red ni tokens).
- **O2** — Verificar prompt (spy), parseo y tres ramas de error (no-JSON, cantidad inválida, vacío sin llamar).
- **O3** — La suite atrapa bugs (caza el mutante) y el alumno distingue unit test de eval.

## Criterios y niveles

### C1 — Cobertura de comportamiento con fakes deterministas · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No usa un fake/stub (o llama al modelo real); falta el happy path o el parseo no se ejercita (el fake devuelve un dict ya parseado en vez de un string). |
| **en-progreso** | Hay happy path con fake-string, pero faltan ramas de error, o el fake imita mal la frontera (devuelve dict/objeto en vez de texto). |
| **competente** | Happy path con fake que devuelve **texto** (string) y afirma el `Pedido`; cubre las tres ramas de error con `pytest.raises(ExtraccionInvalida)`: no-JSON, cantidad inválida y mensaje vacío. |
| **excelente** | Además distingue ramas de error vecinas (JSON malformado vs. clave faltante vs. valor fuera de rango como casos separados), usa `parametrize` para los casos de cantidad inválida, o prueba `construir_prompt` como función pura aparte. |

### C2 — Verificación de interacción (spy) y mock solo en la frontera · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No verifica el prompt, o mockea de más (parchea `json.loads`/la validación), o el test de vacío no comprueba que el modelo NO se llamó. |
| **en-progreso** | Verifica el prompt pero de forma frágil (compara el string completo en vez de `in`), o no afirma `assert_not_called` en el caso vacío. |
| **competente** | Usa un `Mock` como spy y afirma que el prompt enviado **contiene** el mensaje (`call_args`); el caso de mensaje vacío usa un `Mock` y afirma `assert_not_called()`; solo se mockea la frontera (la lógica corre real). |
| **excelente** | Además afirma `assert_called_once()` cuando corresponde y razona por qué esa aserción de interacción se justifica (consultar el modelo es el contrato de la función). |

### C3 — La suite atrapa bugs (autochequeo con mutante) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | La suite queda verde contra `mutante_a` (no lo caza) o el alumno no hizo el autochequeo. |
| **en-progreso** | Caza el mutante por accidente (sin entender qué caso lo logra) o no revirtió el import a `solucion`. |
| **competente** | La suite se pone **roja** contra `mutantes.mutante_a` gracias al caso de cantidad inválida; revirtió el import. |
| **excelente** | Documenta en `notas.md` qué caso atrapó al mutante y reconoce el hueco de su primera versión. |

### C4 — Comprensión: unit test vs eval · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que algún test prueba que "el modelo extrae bien". |
| **competente** | Explica que sus asserts verifican su pegamento (parseo/validación) porque la respuesta la escribió él en el fake; medir si el modelo acierta es un eval. |
| **excelente** | Además ubica dónde correría ese eval (dataset etiquetado + métrica, gate del pipeline, Fase 6) y por qué no va en la suite unitaria (costo/latencia/determinismo). |

## Errores típicos a marcar
- **Fake que devuelve un dict ya parseado** (`{"producto": ...}`) en vez de un **string**: el test nunca ejercita el parser, justo lo que más se rompe en producción.
- **Llamar al modelo real** en el test (lento, flaky, caro, necesita API key) — confunde la suite unitaria con un eval/smoke.
- **Sobre-mockeo**: parchear `json.loads` o la validación interna; deja de probar el parseo/validación.
- **No incluir el caso de cantidad inválida**: sin él, `mutante_a` sobrevive.
- **No afirmar `assert_not_called()`** en el mensaje vacío: no comprueba que no se gastó una llamada.
- **Modificar `solucion.py`** para "facilitar" el test: invalida el ejercicio.
- Afirmar que algún test prueba la **calidad** del modelo (es un eval, no un unit test).
- (transversal costo/latencia) no notar que mockear la frontera es lo que mantiene la suite gratis y rápida.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Suite "perfecta de una", con fixtures sofisticadas o `mocker.patch` del SDK (que aquí no hace falta, porque la frontera se inyecta) — delata código pegado más que razonado.
- Caza el mutante pero no sabe **qué caso** lo logra ni por qué.
- No puede explicar por qué su fake debe devolver texto y no un dict.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga contra qué caso se pondría roja su suite frente a `mutante_a`, y que explique por qué ningún assert prueba la calidad del modelo.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu fake devuelve un string o un dict? La frontera real devuelve texto. Y corre el autochequeo con `mutante_a`: si queda verde, ¿qué validación no estás ejercitando?"
- **Pregunta socrática (nivel 2):** "En tu test de happy path, la respuesta 'café/2' la escribiste tú en el fake. Entonces, ¿qué está probando el assert exactamente? ¿Prueba que el modelo extrae bien?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Añade un caso con `cantidad: -3` esperando `ExtraccionInvalida` (eso caza al mutante). Usa un `Mock` para el spy del prompt y para el caso vacío (`assert_not_called`). No parchees `json.loads`. Repasa la sección 4.4 de la lección antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es el ensayo en pequeño de cualquier parte del **Capstone F2** que toque un LLM: aislar la llamada como un *port* inyectable y construir su red de tests deterministas, dejando la calidad de la salida para un eval (Fase 6). El ADR "la llamada al LLM se inyecta como callable" nace de aquí.
