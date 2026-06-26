---
ejercicio_id: fase-2/tdd-dividir-gasto
fase: fase-2
sub_unidad: "2.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Dividir un gasto en partes justas (TDD de una regla real)

## Implementación canónica (`solucion.py`)

```python
def dividir_gasto(monto_clp: int, personas: int) -> list[int]:
    if personas <= 0:
        raise ValueError("personas debe ser un entero positivo")
    if monto_clp < 0:
        raise ValueError("monto_clp no puede ser negativo")
    base, resto = divmod(monto_clp, personas)
    return [base + 1 if i < resto else base for i in range(personas)]
```

Verificado contra `acceptance_test.py`: comportamientos 1–7 e invariantes en verde.

## El recorrido TDD esperado (lo que la bitácora debería reflejar)

| Ciclo | 🔴 Test | 🟢 Código mínimo | 🔵 Refactor |
|---|---|---|---|
| 1 | `dividir_gasto(100, 2) == [50, 50]` | `[monto // personas] * personas` | — |
| 2 | `dividir_gasto(100, 3) == [34, 33, 33]` | **rompe** el del ciclo 1 (suma 99) → `divmod` + repartir resto | reescribe a `divmod` + comprensión |
| 3 | `dividir_gasto(10, 4) == [3, 3, 2, 2]` | pasa gratis (la regla del resto ya generaliza) | — |
| 4 | `dividir_gasto(0, 3) == [0, 0, 0]` | pasa gratis (`divmod(0,3) == (0,0)`) | — |
| 5 | `dividir_gasto(100, 1) == [100]` | pasa gratis | — |
| 6 | `dividir_gasto(100, 0)` → `ValueError` | guarda `if personas <= 0` | — |
| 7 | `dividir_gasto(-100, 2)` → `ValueError` | guarda `if monto_clp < 0` | — |
| 8 | invariante `sum(...) == m` (caso no exacto) | pasa gratis si el reparto es correcto | — |

El punto pedagógico central: el **ciclo 2 es el que diseña la función**. El ciclo 1 se
resuelve con división entera ingenua; el ciclo 2 la **rompe** porque `[33,33,33]` suma 99,
y *ese rojo* es el que obliga a introducir `divmod` y el reparto del resto. Que los ciclos
3–5 pasen "gratis" es la firma de la triangulación: una vez que el diseño correcto aparece
(forzado por un test), los casos siguientes ya quedan cubiertos.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Orden de las guardas vs. el cálculo.** La validación va **antes** de `divmod`. Si el
   alumno calcula primero, `personas == 0` revienta con `ZeroDivisionError` antes de llegar
   al `raise` — el test de error podría incluso pasar (lanza *una* excepción), pero por la
   razón equivocada. Verificar que es `ValueError` explícito, no un crash de división.
2. **A quién le toca el resto.** La convención del enunciado: las **primeras** `resto`
   personas reciben el peso de más. `[base + 1 if i < resto else base ...]` lo cumple.
   Dárselo a las últimas (`i >= personas - resto`) también satisface las invariantes y es
   aceptable, pero entonces `dividir_gasto(100,3)` daría `[33,33,34]` y fallaría el caso
   concreto del acceptance. Si el alumno eligió esa convención, su propio test concreto
   debe reflejarla — y el acceptance fija `[34,33,33]`, así que la referencia manda.
3. **Invariante vs. caso.** El test 8 debe afirmar una **propiedad** (`sum == monto`,
   `len == personas`, `max-min <= 1`) sobre varias entradas, idealmente con
   `@pytest.mark.parametrize`. Un único `assert ... == [34,33,33]` NO es un invariante.
4. **Tipos.** El contrato es **enteros** (pesos CLP). Usar `/` produce floats y rompe la
   igualdad con listas de int; debe ser `//` / `divmod`.

## Rango de soluciones aceptables
- **Bucle explícito** en vez de comprensión: válido si reparte igual.
- **Acumular y repartir el resto en una segunda pasada** (`partes = [base]*personas; for i in range(resto): partes[i] += 1`): equivalente y legible.
- **Resto a las últimas personas** (`[34,33,33]` → `[33,33,34]`): aceptable como convención *solo si* sus propios tests concretos la reflejan; pero el acceptance provisto fija el resto a las primeras, así que para pasarlo debe alinearse a esa convención.
- **Validar con `personas < 1`** en vez de `<= 0`: equivalente para enteros.
- ❌ **No aceptable como "excelente":** pesos ponderados por persona, soporte de decimales/`Decimal`, redondeo configurable u otras generalizaciones que ningún test del enunciado pide. Código no exigido por un test → contradice O1 y suele delatar copia.
