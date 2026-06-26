---
ejercicio_id: fase-2/pytest-suite-envios
fase: fase-2
sub_unidad: "2.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Suite pytest para un módulo de envíos

## Suite canónica (`test_solucion.py`)

```python
import pytest
from unittest.mock import Mock

from solucion import costo_envio, cotizar


@pytest.mark.parametrize(
    "peso_kg, zona, es_socio, esperado",
    [
        (2.0, "metropolitana", False, 4390),    # 2990 + 700*2
        (2.1, "metropolitana", False, 5090),    # ceil(2.1)=3 -> 2990 + 700*3  (BORDE)
        (1.0, "patagonia", False, 6690),        # 3690 + 3000 recargo remoto
        (2.0, "metropolitana", True, 3731.5),   # 4390 * 0.85  (socio)
        (5.0, "isla", True, 8066.5),            # (2990+3500+3000) * 0.85
    ],
)
def test_costo_envio(peso_kg, zona, es_socio, esperado):
    assert costo_envio(peso_kg, zona, es_socio) == pytest.approx(esperado)


def test_peso_invalido_lanza_value_error():
    with pytest.raises(ValueError, match="mayor que 0"):
        costo_envio(0, "metropolitana", es_socio=False)


@pytest.fixture
def tasa_usd():
    # Mock para poder afirmar que la frontera se consultó. Un `lambda: 950`
    # (stub) también sería válido si solo se afirma el resultado.
    return Mock(return_value=950)


def test_cotizar_convierte_a_usd(tasa_usd):
    # costo_envio(2.0, metropolitana, False) = 4390 CLP; 4390 / 950 = 4.62 USD
    resultado = cotizar(2.0, "metropolitana", False, tasa_usd)
    assert resultado == pytest.approx(4.62)
    tasa_usd.assert_called_once()
```

## Valores de referencia (calculados leyendo el SUT)

| peso_kg | zona | socio | costo_envio | por qué |
|---|---|---|---|---|
| 2.0 | metropolitana | no | 4390 | 2990 + 700·⌈2.0⌉ = 2990+1400 |
| 2.1 | metropolitana | no | 5090 | ⌈2.1⌉=3 → 2990+2100 (**el borde que caza `mutante_a`**) |
| 1.0 | patagonia | no | 6690 | 2990+700 + 3000 remoto |
| 2.0 | metropolitana | sí | 3731.5 | 4390·0.85 (**el caso que caza `mutante_b`**) |
| 5.0 | isla | sí | 8066.5 | (2990+3500+3000)·0.85 = 9490·0.85 |
| cotizar(2.0,met,no, →950) | — | — | 4.62 | 4390/950 = 4.6210… |

## Por qué se mockea `tasa_usd` y NO `costo_envio`
- `tasa_usd` es la **frontera**: en producción es una llamada de red al servicio de tipo de cambio. Mockeada, el test es rápido, determinista y no depende de internet.
- `costo_envio` es **lógica pura**: es justo lo que `cotizar` debe componer bien. Si se mockeara, el test de `cotizar` solo probaría `numero_inventado / 950`, sin verificar el cálculo real → sobre-mockeo.

## Autochequeo con mutantes (el corrector debe pedir evidencia)
- Apuntar el import a `mutantes.mutante_a` (usa `floor`): el caso `(2.1, …)` pasa de esperar `5090` a recibir `4390` → **rojo**. Si la suite no tiene el caso con decimales, queda verde y el mutante "sobrevive".
- Apuntar a `mutantes.mutante_b` (sin descuento socio): el caso `(2.0, …, True)` pasa de `3731.5` a `4390` → **rojo**. Sin un caso `es_socio=True`, sobrevive.
- Una suite que caza ambos demuestra que cubre los dos comportamientos críticos.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`pytest.approx`**: los montos con descuento son float (3731.5, 8066.5); comparar con `==` puede ser frágil en otros casos. No penalizar si usó `==` y pasó, pero comentar que `approx` es la práctica correcta con floats.
2. **Origen de los `esperado`**: deben venir de leer el SUT. Si el alumno solo ejecutó el SUT y copió la salida, funciona, pero hay que verificar (en el check de dominio) que sabe recomputarlos.
3. **Fixture vs. inline**: aceptar `lambda: 950` como stub si solo afirma el resultado; el `Mock` es necesario solo si afirma la interacción. Ambas válidas para "competente"; la interacción sube a "excelente".
4. **No mockear `_kg_facturables`**: es un detalle interno puro; mockearlo es sobre-mockeo.
5. **No modificar `solucion.py`**: si lo tocó, la red ya no garantiza el comportamiento del SUT real.

## Rango de soluciones aceptables
- **Stub `lambda: 950`** en la fixture en vez de `Mock`: válido (no afirma la interacción, pero el ejercicio no la exige estrictamente; mejor si la añade).
- **Casos distintos** en el `parametrize` mientras incluyan el borde 2.0/2.1, una zona remota y un caso de socio.
- **`match=` distinto** en `pytest.raises` (o sin `match`): aceptable; con `match` es más estricto y mejor.
- **Tests separados** en vez de un solo `parametrize` (uno por caso): funciona pero es el smell de duplicación que `parametrize` resuelve; bajar un punto en C1 y comentar.
- **`notas.md`** con el análisis de mutantes: no obligatorio, suma para "excelente".
