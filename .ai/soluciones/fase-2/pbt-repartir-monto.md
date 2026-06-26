---
ejercicio_id: fase-2/pbt-repartir-monto
fase: fase-2
sub_unidad: "2.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Property-based testing: caza el bug del remanente

## Implementación canónica (`solucion.py`)

```python
def repartir_monto(total: int, partes: int) -> list[int]:
    if partes <= 0:
        raise ValueError("partes debe ser >= 1")
    base, resto = divmod(total, partes)
    return [base + 1 if i < resto else base for i in range(partes)]
```

- `divmod(total, partes)` da `(base, resto)`: cada parte recibe `base`, y las primeras `resto` partes
  reciben **una unidad extra** para que la suma cuadre exactamente.
- Para `total >= 0` y `partes >= 1`, todas las partes son no negativas y difieren a lo más en 1.

## Property-based tests canónicos (`test_solucion.py`)

```python
from hypothesis import given, strategies as st

montos = st.integers(min_value=0, max_value=10**9)
cuantas = st.integers(min_value=1, max_value=1000)

@given(montos, cuantas)
def test_la_suma_se_conserva(total, partes):          # P1
    assert sum(repartir_monto(total, partes)) == total

@given(montos, cuantas)
def test_es_lo_mas_parejo_posible(total, partes):     # P2
    r = repartir_monto(total, partes)
    assert max(r) - min(r) <= 1

@given(montos, cuantas)
def test_devuelve_exactamente_n_partes(total, partes):# P3
    assert len(repartir_monto(total, partes)) == partes

@given(montos, cuantas)
def test_todas_las_partes_son_no_negativas(total, partes):  # P4 (nivel excelente)
    assert all(p >= 0 for p in repartir_monto(total, partes))

def test_partes_invalidas_lanzan_valueerror():
    import pytest
    with pytest.raises(ValueError):
        repartir_monto(100, 0)
```

## Razonamiento paso a paso (lo que mide `propiedades.md`)

1. **Por qué P1 es la propiedad estrella.** La versión ingenua `[total // partes] * partes` pasa los
   ejemplos "redondos" (`100/4 → [25,25,25,25]`, suma 100 ✓) pero **pierde el remanente** apenas hay
   resto: `101 // 4 = 25`, devuelve `[25,25,25,25]`, suma **100 ≠ 101**. La propiedad de conservación
   lo detecta en la primera entrada con `total % partes != 0`. El ejemplo a mano no, porque nadie suele
   escribir el caso `101/4` a propósito.
2. **Shrinking.** Cuando una propiedad falla, Hypothesis **reduce** el contraejemplo al más simple que
   sigue fallando. Para P1 contra la versión ingenua, entrega algo como `total=1, partes=2` (`[0,0]`,
   suma 0 ≠ 1), no el monstruo de 9 dígitos donde lo encontró primero. El caso mínimo es el que mejor
   explica el bug.
3. **Tautología (qué NO hacer).** `assert repartir_monto(t, n) == [base + 1 if i < resto else base ...]`
   recomputa el algoritmo dentro del test: prueba que el código es igual a sí mismo, no que es correcto.
   Una propiedad válida afirma una verdad **independiente** del algoritmo (la suma se conserva; las partes
   son parejas), verificable sin reimplementar la función.
4. **Por qué acotar las estrategias.** `st.integers()` sin `max_value` para `partes` puede generar listas
   de millones de elementos → el test tarda o agota memoria. Acotar (`max_value=1000`) mantiene el costo
   bajo sin perder poder de detección. Es el hilo **costo/latencia** aplicado a los propios tests.

## Puntos resbalosos (donde el corrector debe mirar)
1. **P2 escrita como `== 1`** en vez de `<= 1`: falla cuando el reparto es exacto (diferencia 0). Bug común.
2. **`partes` no acotado a `>= 1`**: si la estrategia permite 0 o negativos, la propiedad de suma se
   "rompe" por el `ValueError` esperado, no por un bug real. Las estrategias deben respetar la precondición.
3. **Propiedad que solo cubre el camino feliz acotado** (p. ej. `total` siempre múltiplo de `partes`):
   nunca ejercita el remanente, justo el caso que importa. Verificar que el rango no excluye el resto.
4. **Demostración de P1-vs-ingenua ausente:** sin mostrar que P1 falla contra `[total // partes] * partes`,
   el alumno no demostró que entiende *por qué* la propiedad aporta.

## Rango de soluciones aceptables
- Distribuir el resto a las **últimas** partes en vez de las primeras es igual de válido si la suma y la
  equidad se cumplen (el orden exacto no está en el contrato de las propiedades, aunque los *ejemplos*
  provistos sí fijan "primeras"; si cambian el orden deben ajustar los ejemplos coherentemente).
- Usar `@composite` para generar `(total, partes)` juntos es válido y de nivel excelente.
- `propiedades.md` vale cualquier redacción que (a) nombre la invariante de cada propiedad y (b) demuestre
  el fallo de la versión ingenua. No se exige la palabra "metamórfico", pero el nivel **excelente** la usa.
- **Variante de control para detectar dependencia-IA:** pedir que prediga el caso mínimo que entregaría el
  shrinking si P1 fallara. Quien entendió dice "algo como `total=1, partes=2`"; quien no, se traba.
