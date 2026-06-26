---
ejercicio_id: fase-2/pytest-suite-envios
fase: fase-2
sub_unidad: "2.6"
version: 1
---

# Rúbrica — Suite pytest para un módulo de envíos

> Rúbrica **analítica** atada a los `objetivos`. El producto no es "que pase verde":
> es una suite que **atrapa bugs reales** (los mutantes) sin acoplarse a la
> implementación. Evaluar la **forma** de la suite (parametrize, fixture,
> mock-en-frontera) tanto como su verde. El SUT es la verdad; si el alumno lo
> modificó, la evaluación se invalida.

## Objetivos evaluados
- **O1** — Implementar una suite con `parametrize` (con bordes) y `pytest.raises` sobre lógica pura.
- **O2** — Usar una `fixture` para inyectar el doble de la frontera.
- **O3** — Mockear solo la frontera (`tasa_usd`) y dejar `costo_envio` real, demostrado al cazar dos mutantes.

## Criterios y niveles

### C1 — Cobertura de comportamiento con parametrize y errores · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `parametrize`, o <3 casos, o no testea el error (`pytest.raises`). |
| **en-progreso** | Hay `parametrize` con algunos casos pero sin el **borde** del redondeo de kg (2.0 vs 2.1), o sin zona remota, o sin caso de socio; falta el `pytest.raises`. |
| **competente** | `parametrize` con ≥5 casos incluyendo el borde 2.0/2.1, zona remota y socio; un `pytest.raises(ValueError)` para peso ≤ 0; los `esperado` son correctos (calculados del SUT, no inventados). |
| **excelente** | Además usa `pytest.approx` para los montos con float, ids legibles, y cubre un borde extra defendible (p. ej. el redondeo a 2 decimales del descuento). |

### C2 — Fixture y mock en la frontera (no en la lógica) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Mockea `costo_envio` (la lógica), o no testea `cotizar`, o no usa fixture. |
| **en-progreso** | Testea `cotizar` pero crea el doble inline en cada test en vez de una `fixture`, o mockea de más (p. ej. también `_kg_facturables`). |
| **competente** | Una `@pytest.fixture` provee el doble de `tasa_usd`; `cotizar` se testea con esa frontera mockeada y `costo_envio` **real**; afirma el resultado en USD. |
| **excelente** | Además afirma la **interacción** con la frontera (`Mock(return_value=...)` + `assert_called_once()`) entendiendo que esa aserción se justifica porque consultar la tasa es el contrato de `cotizar`. |

### C3 — La suite atrapa bugs (autochequeo con mutantes) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | La suite queda verde contra uno o ambos mutantes (no los caza), o el alumno no hizo el autochequeo. |
| **en-progreso** | Caza un mutante pero no el otro (le falta el caso borde o el caso socio). |
| **competente** | La suite se pone **roja** contra `mutante_a` (borde 2.1) y `mutante_b` (caso socio); revirtió el import a `solucion`. |
| **excelente** | Documenta en `notas.md` qué caso atrapó cada mutante y reconoce qué hueco tenía su primera versión. |

## Errores típicos a marcar
- **Inventar los `esperado`** ejecutando el SUT primero y copiando la salida sin entender el cálculo (corre el riesgo de "fijar" un bug si el SUT tuviera uno): se pide calcular leyendo el código.
- **Mockear `costo_envio`** dentro del test de `cotizar`: ya no prueba el cálculo, solo aritmética con un número inventado (sobre-mockeo).
- **No incluir el borde 2.0/2.1 kg**: sin él, `mutante_a` (floor) pasa desapercibido.
- **No incluir un caso `es_socio=True`**: sin él, `mutante_b` pasa desapercibido.
- **Comparar floats con `==`** en vez de `pytest.approx` (los montos con descuento son float).
- **Modificar `solucion.py`** para "facilitar" el test: invalida el ejercicio.
- (transversal spec-driven) pensar la tabla de `parametrize` como una especificación: si no aparece, la suite suele tener huecos.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Suite "perfecta de una", con `mocker.patch` de cosas que no son fronteras o con fixtures sofisticadas (`scope`, `params`) impropias del nivel, que delatan código pegado más que razonado.
- Los `esperado` son todos correctos pero el alumno no sabe **de dónde sale** ninguno (no puede recomputar `costo_envio(2.1, ...)` a mano).
- No puede explicar por qué `costo_envio` no se mockea y `tasa_usd` sí.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga contra qué mutante se pondría roja su suite y por qué; y que recompute a mano el costo de un caso del `parametrize`.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu tabla de `parametrize` tiene un caso de 2.0 kg y otro de 2.1 kg? Corre el autochequeo con `mutante_a`: si queda verde, ahí está el hueco."
- **Pregunta socrática (nivel 2):** "En el test de `cotizar`, ¿qué estás verificando realmente si mockeas `costo_envio`? ¿Qué parte del comportamiento queda sin probar?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Deja `costo_envio` real en el test de `cotizar`; mockea solo `tasa_usd` con la fixture. Para cazar los mutantes, añade el par 2.0/2.1 kg y un caso `es_socio=True`. Repasa la sección 4.4 de la lección antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es el ensayo en pequeño del **Capstone F2 (Refactor + suite de tests)**: ahí construirás la red de tests de tu propia API con esta misma disciplina (muchos unit sobre la lógica, mock solo en las fronteras) que hará seguro el refactor.
