---
ejercicio_id: fase-2/cazar-mutantes-sobrevivientes
fase: fase-2
sub_unidad: "2.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Caza los mutantes que tu coverage no ve

## Respuesta canónica

Con la suite débil de partida (4 tests, 100% line coverage):

| Mutante | Mutación | ¿Sobrevive? | Por qué |
|---|---|---|---|
| **M1** | `puntos >= 100 and es_socio` → `puntos > 100 and es_socio` | **SOBREVIVE** | El único caso que lo distingue es `puntos == 100` con socio; la suite no lo tiene (usa 150). |
| **M2** | `... and es_socio` → `... or es_socio` | muere | `descuento(150, False)`: con `or`, `150>=100 or False` = True → devuelve 30, pero el test espera 20 → falla. |
| **M3** | (2ª línea) `puntos >= 100` → `puntos > 100` | **SOBREVIVE** | Lo distingue `puntos == 100` no socio; la suite no lo prueba. |
| **M4** | `puntos >= 50` → `puntos > 50` | **SOBREVIVE** | Lo distingue `puntos == 50`; la suite usa 70. |
| **M5** | `return 30` → `return 31` | muere | `descuento(150, True)` espera 30; el mutante da 31 → falla. |
| **M6** | `return 10` → `return 11` | muere | `descuento(70, False)` espera 10; el mutante da 11 → falla. |
| **M7** | `return 0` → `return 1` | muere | `descuento(10, False)` espera 0; el mutante da 1 → falla. |

**Sobreviven: M1, M3, M4.** Mutation score de partida ≈ **4/7 ≈ 57%** (sobre estos 7;
`mutmut` real genera más mutantes —cada número y operador— pero el patrón es idéntico:
los sobrevivientes son los de comparación en los bordes).

## Razonamiento paso a paso

La función tiene **tres umbrales de comparación** (`>= 100` dos veces, `>= 50`) y
**cuatro valores de retorno** (30, 20, 10, 0). Regla general:

- **Mutante de valor de retorno / número** (`return 30` → `31`): lo mata *cualquier*
  test que afirme ese retorno exacto. La suite débil ya afirma los cuatro retornos
  (con 150-socio, 150-no-socio, 70, 10), así que M5/M6/M7 mueren de entrada.
- **Mutante de comparación** (`>=` → `>`): solo cambia el comportamiento en el
  **valor exacto del umbral**. `150 >= 100` y `150 > 100` son ambos True; la única
  entrada que los separa es `100`. Como ningún test usa 100 (ni 50), M1/M3/M4 sobreviven.
- **Mutante lógico** (`and` → `or`): se mata con una entrada donde las dos condiciones
  difieran. `descuento(150, False)` tiene `puntos>=100`=True pero `es_socio`=False; con
  `or` el resultado cambia de 20 a 30. La suite ya lo tiene → M2 muere.

## Suite fortalecida (tests que matan a M1, M3, M4)

```python
def test_borde_100_socio_obtiene_30():
    # Distingue M1: con > en vez de >=, 100 caería a la rama de 20.
    assert descuento(100, True) == 30

def test_borde_100_no_socio_obtiene_20():
    # Distingue M3: con > en vez de >=, 100 caería a la rama de 10.
    assert descuento(100, False) == 20

def test_borde_50_obtiene_10():
    # Distingue M4: con > en vez de >=, 50 caería a la rama de 0.
    assert descuento(50, False) == 10
```

Con estos tres tests sumados a los cuatro originales, los 7 mutantes mueren. El
**line coverage sigue en 100%** antes y después: la prueba de que el coverage nunca
fue la métrica que faltaba.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Borde exacto, no aproximado.** `descuento(101, True)` NO mata a M1 (101 > 100 y
   101 >= 100 dan lo mismo). Debe ser `100`. Un alumno que pone 99/101 no entendió.
2. **M3 vs M1.** Ambos mutan un `>= 100`, pero en líneas distintas. M1 (1ª línea,
   con `and es_socio`) lo mata `(100, True)`; M3 (2ª línea) lo mata `(100, False)`.
   Confundirlos lleva a dejar uno vivo.
3. **`mutmut` genera más mutantes.** El alumno verá, por ejemplo, mutaciones de `100`
   a `101`, de `50` a `51`, etc. Eso es esperado; no significa que su predicción de los
   7 esté mal. El score real puede tener decimales distintos a 4/7.
4. **Mutantes equivalentes.** En esta función no hay equivalentes obvios; si el alumno
   afirma haber encontrado uno, pídele que muestre la entrada que *debería* distinguirlo
   y por qué no existe.

## Rango de soluciones aceptables
- Cualquier test que use el **valor exacto del umbral** (100 socio, 100 no-socio, 50)
  y afirme el retorno correcto es válido, aunque agrupe casos con `parametrize`.
- Agregar también los "just below" (`99`, `49`) es bienvenido (refuerza), pero no es
  necesario: el mutante `>=` → `>` ya muere con el borde exacto. No penalizar su
  ausencia ni exigirla.
- Para `O2`, basta con que el alumno reporte el score real y contraste con su
  predicción; no se exige un formato concreto de `mutantes.md`.
- Si el alumno usó `Stryker`/otra herramienta en vez de `mutmut` (p. ej. portó la
  función a TS), es válido siempre que el razonamiento de bordes sea el mismo.
