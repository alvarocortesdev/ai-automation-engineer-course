---
ejercicio_id: fase-1/tests-con-fixtures-parametrize
fase: fase-1
sub_unidad: "1.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diseñar tests con fixtures y parametrize

El módulo `agenda.py` NO se modifica. El entregable es `test_agenda.py`. Suite canónica:

```python
import pytest
from agenda import (
    AgendaCorrupta,
    cargar_eventos,
    guardar_eventos,
    proximos,
)


# --- Fixture propia: datos de ejemplo, frescos para cada test ---
@pytest.fixture
def eventos_demo():
    return [
        {"fecha": "2026-06-30", "titulo": "deadline informe"},
        {"fecha": "2026-07-01", "titulo": "café con Ada"},
        {"fecha": "2026-07-15", "titulo": "dentista"},
    ]


# --- Disco aislado con tmp_path ---
def test_guardar_y_cargar_es_round_trip(tmp_path, eventos_demo):
    ruta = tmp_path / "agenda.json"
    guardar_eventos(ruta, eventos_demo)
    assert cargar_eventos(ruta) == eventos_demo


def test_archivo_inexistente_devuelve_lista_vacia(tmp_path):
    ruta = tmp_path / "no_existe.json"        # deliberadamente NO lo creamos
    assert cargar_eventos(ruta) == []


def test_archivo_corrupto_lanza_agenda_corrupta(tmp_path):
    ruta = tmp_path / "rota.json"
    ruta.write_text("esto no es json {", encoding="utf-8")
    with pytest.raises(AgendaCorrupta):
        cargar_eventos(ruta)


# --- proximos() parametrizado (incluye el borde del >=) ---
@pytest.mark.parametrize("hoy, titulos_esperados", [
    ("2026-06-01", ["deadline informe", "café con Ada", "dentista"]),  # todos futuros, ordenados
    ("2026-07-01", ["café con Ada", "dentista"]),                      # hoy == fecha de un evento: se incluye
    ("2026-07-16", []),                                                # hoy posterior a todos
])
def test_proximos_filtra_y_ordena(eventos_demo, hoy, titulos_esperados):
    resultado = [e["titulo"] for e in proximos(eventos_demo, hoy)]
    assert resultado == titulos_esperados


def test_proximos_devuelve_ordenado_aunque_la_entrada_no_lo_este():
    desordenados = [
        {"fecha": "2026-08-10", "titulo": "b"},
        {"fecha": "2026-08-01", "titulo": "a"},
    ]
    assert [e["titulo"] for e in proximos(desordenados, "2026-01-01")] == ["a", "b"]
```

## Razonamiento (qué demuestra cada test)

1. **`tmp_path`** es un `pathlib.Path` a un directorio temporal único por test que pytest borra al
   terminar. Por eso el round-trip, el inexistente y el corrupto **no dejan basura ni dependen del
   orden**. Ese aislamiento es el punto central del ejercicio.
2. **La fixture `eventos_demo`** centraliza los datos de ejemplo. Cada test que la pide recibe una
   **invocación fresca** (un `list` nuevo): aunque un test mutara la lista, no contaminaría a otro.
3. **`parametrize`** comprime tres escenarios de `proximos` en una función. El caso `("2026-07-01", ...)`
   es el más informativo: prueba que el filtro es `>=` (incluye el evento de ese mismo día), no `>`.
4. **`pytest.raises(AgendaCorrupta)`** verifica el modo de fallo sin un `try/except` manual (que podría
   dar un falso verde si la excepción no se lanza).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Ruta fija en vez de `tmp_path`.** Si el alumno usa `"agenda.json"` o `/tmp/agenda.json`, el test
   ensucia el repo/sistema y puede pisarse con otros. Es el error #1.
2. **No probar el borde `>=`.** Omitir un `hoy` igual a una fecha de evento deja sin verificar la
   decisión de diseño más fácil de romper.
3. **Atrapar la corrupción con `try/except`** sin re-lanzar ni `pytest.fail`: si la excepción NO se
   lanza, el test pasa igual → falso verde. `pytest.raises` evita eso.
4. **Fixture que afirma.** Poner `assert` dentro de la fixture en vez de en el test; la fixture solo
   prepara datos.
5. **Comparar listas de dicts vs. listas de títulos.** Ambas válidas; comparar títulos suele ser más
   legible para `proximos`, pero comparar los dicts completos también es correcto.

## Rango de soluciones aceptables
- **Datos de ejemplo inline (sin fixture)** en algún test puntual: aceptable, pero el objetivo pide una
  fixture reutilizada en ≥ 2 tests; si no existe ninguna, baja en C2.
- **Comparar `proximos` por dict completo** en vez de por título: válido.
- **Más o menos casos parametrizados**: bien mientras incluya el borde del `>=` y el caso vacío.
- **Usar `tmp_path_factory` o un `conftest.py`**: válido pero innecesario; si aparece junto a otras
  señales (mocking de `open`, `scope="session"` sin motivo), considerar dependencia-IA.
- **Caso borde propio:** cualquiera defendible (lista de eventos vacía → `proximos` devuelve `[]`;
  evento sin clave `fecha` provocaría `KeyError`, etc.).
