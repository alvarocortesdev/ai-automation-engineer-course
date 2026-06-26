---
ejercicio_id: fase-2/tdd-sumador-de-texto
fase: fase-2
sub_unidad: "2.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Sumador de texto (kata de TDD desde cero)

## Implementación canónica (`solucion.py`)

```python
def sumar(numeros: str) -> int:
    if numeros == "":
        return 0
    partes = numeros.replace("\n", ",").split(",")
    valores = [int(p.strip()) for p in partes]
    negativos = [v for v in valores if v < 0]
    if negativos:
        raise ValueError(f"no se permiten negativos: {negativos}")
    return sum(valores)
```

Verificado contra `acceptance_test.py`: los 7 comportamientos en verde.

## El recorrido TDD esperado (lo que la bitácora debería reflejar)

| Ciclo | 🔴 Test | 🟢 Código mínimo | 🔵 Refactor |
|---|---|---|---|
| 1 | `sumar("") == 0` | `return 0` (fake it) | — |
| 2 | `sumar("1") == 1` | `return int(numeros)` si no vacío | — |
| 3 | `sumar("1,2") == 3` | `split(",")` + `sum(int(p) ...)` | — |
| 4 | `sumar("1,2,3,4") == 10` | **pasa gratis** (triangulación: el split ya generaliza) | — |
| 5 | `sumar("1\n2,3") == 6` | normalizar antes de separar | `replace("\n", ",")` antes del split |
| 6 | `sumar(" 1 , 2 ") == 3` | `.strip()` por parte | — |
| 7 | `sumar("1,-2,3")` → `ValueError` | filtrar negativos y `raise` | — |

Puntos pedagógicos que la bitácora **debería** evidenciar:
- **Fake it** en el ciclo 1 (un `return 0` literal) y, opcionalmente, en el 2 (`return 1` antes de generalizar a `int(numeros)`).
- **Triangulación** en el 4: el comportamiento "cualquier cantidad" no requiere código nuevo si el 3 se resolvió con `split` + `sum`. Que salga gratis es la señal de que el diseño correcto apareció solo.
- **Refactor real** en el 5: en vez de un `if "\n" in numeros` especial, se *normaliza* el separador. Ese es el momento "limpio en verde".

## Puntos resbalosos (donde el corrector debe mirar)
1. **`int("")` revienta.** Entradas con separador al borde (`"1,2\n"`, `"1,,2"`) producen una parte vacía y `int("")` lanza `ValueError` — pero de parseo, no de negativo. El enunciado **no** pide cubrir esto; no penalizar su ausencia, pero si el alumno lo detecta y lo deja documentado como límite, suma (es justo el pensamiento de borde que se busca).
2. **Mensaje del error.** El criterio pide que el mensaje **incluya** el negativo. `f"...{negativos}"` con la lista cumple; `match="-2"` en el test lo verifica. Si reporta solo el primero en vez de todos, sigue siendo competente.
3. **Orden de validación.** Filtrar negativos **después** de convertir a `int` es lo natural. Si valida sobre strings (`"-"` in parte) es frágil; comentar.
4. **`strip()` dónde.** Aplicado por parte (`int(p.strip())`) cubre `" 1 , 2 "`. Un `numeros.strip()` global NO basta (no limpia los internos).

## Rango de soluciones aceptables
- **Separar con regex** (`re.split(r"[,\n]", numeros)`) en vez de `replace`+`split`: válido y hasta más directo; no es sobre-ingeniería aquí.
- **Reduce/loop manual** en vez de `sum(...)`: válido.
- **Guarda de vacío implícita:** algunos resuelven `""` filtrando partes vacías en vez del `if numeros == ""`. Aceptable si el resultado es 0.
- **Validar negativos lanzando en el primero** (sin juntar la lista): cumple el criterio mínimo aunque reportar todos es mejor.
- ❌ **No aceptable como "excelente":** soporte de delimitadores custom (`"//;\n..."`), longitud máxima, ignorar números > 1000 u otras reglas del kata avanzado que el enunciado no pidió. Eso es código no exigido por ningún test → contradice O1/O2 y suele delatar copia.
