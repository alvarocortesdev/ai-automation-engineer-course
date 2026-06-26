---
ejercicio_id: fase-1/tests-con-fixtures-parametrize
fase: fase-1
sub_unidad: "1.6"
version: 1
---

# Rúbrica — Diseñar tests con fixtures y parametrize

> Rúbrica **analítica** atada a los `objetivos`. El módulo `agenda.py` es correcto; el alumno
> NO arregla código, **diseña tests**. Evaluar el aislamiento (`tmp_path`), la reutilización
> de datos (`@pytest.fixture`) y la compresión de casos (`parametrize`), no solo "que pase verde".

## Objetivos evaluados
- **O1** — Aislar el estado de un test que toca disco con `tmp_path` (sin tocar el repo ni depender del orden).
- **O2** — Extraer datos de prueba a un `@pytest.fixture` propio y reutilizarlo.
- **O3** — Cubrir múltiples casos con `@pytest.mark.parametrize` y el error con `pytest.raises`.

## Criterios y niveles

### C1 — Aislamiento del estado (`tmp_path`) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Usa una ruta fija (`"agenda.json"`, `/tmp/...`) que ensucia el repo o el sistema; o no testea el round-trip. |
| **en-progreso** | Usa `tmp_path` para el round-trip pero crea un archivo real fuera de él para otro test, o deja basura. |
| **competente** | Todo lo que toca disco usa `tmp_path`; round-trip, inexistente y corrupto, ninguno deja archivos. |
| **excelente** | Explica por qué `tmp_path` evita tests frágiles (no dependen del orden ni de estado previo); el test del inexistente apunta a una ruta que deliberadamente no crea. |

### C2 — Reutilización con fixtures · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Repite la misma lista de eventos literal en cada test (copy-paste). |
| **en-progreso** | Define una fixture pero la usa en un solo test, o mete lógica de aserción dentro de la fixture. |
| **competente** | `@pytest.fixture` con los eventos de ejemplo, reutilizada en ≥ 2 tests; la fixture solo *prepara*, no afirma. |
| **excelente** | Entiende que cada test recibe una invocación fresca de la fixture (no comparten estado mutable) y lo aprovecha. |

### C3 — Cobertura de casos (`parametrize` + `raises`) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `proximos` probado con un solo caso; falta el caso corrupto o no usa `pytest.raises`. |
| **en-progreso** | Varios casos de `proximos` pero copiados (sin `parametrize`), o el corrupto atrapado con `except` manual en vez de `pytest.raises`. |
| **competente** | `proximos` con `@pytest.mark.parametrize` (≥ 3 casos incl. límites), corrupto con `pytest.raises(AgendaCorrupta)`, +1 caso borde propio. |
| **excelente** | Casos límite pensados (un `hoy` igual a la fecha de un evento — el `>=` lo incluye; un `hoy` posterior a todos → `[]`); verifica también el **orden** que devuelve `proximos`. |

## Errores típicos a marcar
- **Ruta fija en vez de `tmp_path`**: crea `agenda.json` en el repo; frágil y sucio. Es el error #1 del ejercicio.
- **No probar el `>=` de `proximos`**: omitir el caso donde `hoy` coincide con la fecha de un evento (debe incluirse) pierde el borde más informativo.
- **Atrapar la corrupción con `try/except` en vez de `pytest.raises`**: un `try/except` que no re-lanza puede hacer pasar el test aunque NO se lance la excepción (falso verde).
- **Fixture que afirma**: poner `assert` dentro de la fixture en vez de en el test; la fixture solo prepara datos.
- **Copiar la lista de eventos en cada test** en lugar de una fixture.
- **Modificar `agenda.py`** para "facilitar" el test: está prohibido; se testea tal cual.
- (transversal testing) tests que dependen del orden de ejecución (estado compartido entre tests): justo lo que `tmp_path` y las fixtures frescas evitan.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Uso de fixtures avanzadas no pedidas (`scope="module"`, `conftest.py`, `monkeypatch`, mocking de `open`) cuando `tmp_path` simple basta: sofisticación impropia del nivel.
- Mockear el sistema de archivos en vez de usar `tmp_path` (que escribe archivos reales y desechables): señal de pegar una receta genérica sin entender que `tmp_path` ya resuelve el aislamiento.
- No puede explicar por qué cada test recibe una fixture fresca ni por qué `tmp_path` se borra solo.
- **Verificación sugerida:** pedir que prediga qué pasaría si dos tests usaran la misma ruta fija y corrieran en cierto orden; y que muestre dónde, en su suite, un test podría contaminar a otro (la respuesta correcta: no puede, gracias a `tmp_path`/fixtures).

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu test del round-trip escribe un archivo. ¿Dónde queda ese archivo cuando termina el test? Si quedó en tu carpeta, hay una fixture que lo resuelve."
- **Pregunta socrática (nivel 2):** "Si dos de tus tests usan la misma ruta de archivo y pytest los corre en cierto orden, ¿pueden pisarse? ¿Qué te garantiza `tmp_path` que una ruta fija no?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Pide `tmp_path` como parámetro del test y arma la ruta con `ruta = tmp_path / 'agenda.json'`. Para el corrupto: `ruta.write_text('{roto', encoding='utf-8')` y `with pytest.raises(AgendaCorrupta): cargar_eventos(ruta)`. Para `proximos`, parametriza `(hoy, esperado)` e incluye un `hoy` igual a la fecha de un evento. Revisa la sección 4.6 y reintenta antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Testear módulos correctos con `tmp_path`/fixtures/`parametrize` es la mecánica con que probarás la persistencia y la lógica del **Capstone F1**, y la base del refactor con red de tests de la Fase 2.
