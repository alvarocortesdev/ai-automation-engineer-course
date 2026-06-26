---
ejercicio_id: fase-2/capstone-refactor-tests
fase: fase-2
sub_unidad: "2.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es la **vara de
> medir** del capstone, no un molde a copiar: el alumno puede llegar a un diseño
> distinto y estar igual de bien (ver "Rango de soluciones aceptables"). Úsala
> sólo para detectar el error, nombrar la misconception y graduar pistas (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Capstone F2: Refactor + suite de tests

## Respuesta canónica (qué debe demostrar la entrega)

No hay "una" solución correcta: hay un **proceso** correcto y una **evidencia**
mínima. Una entrega de nivel *competente* demuestra, sobre el `despensa.py`
provisto (o sobre la app de Fase 1 del alumno):

1. **Caracterización antes del primer cambio.** El commit que añade
   `tests/test_caracterizacion.py` (verde) **precede** a cualquier commit que
   toque producción. Esto es lo primero que mira el corrector en el historial.
2. **Refactor que conserva el comportamiento**, con un **núcleo puro** extraído.
3. **Mutation score reportado** (partida → final) con tests de **borde exacto**.
4. **`SPEC.md` + `ARQUITECTURA.md` (inglés) + 2–3 ADRs** + **CI verde** +
   **Conventional Commits**.

### Diseño de referencia (uno válido, no el único)

```python
# despensa/core.py  — núcleo PURO: sin open(), sin print(); 100% testeable.
from datetime import date, datetime

STOCK_MINIMO = 2
DIAS_PARA_VENCER = 3


def _dias_hasta(vence: str, hoy: date) -> int:
    return (datetime.strptime(vence, "%Y-%m-%d").date() - hoy).days


def evaluar(item: dict, hoy: date) -> str | None:
    """Decide la alerta de un item. Pura: misma entrada → misma salida."""
    partes: list[str] = []
    if item["cantidad"] <= STOCK_MINIMO:
        partes.append("STOCK BAJO")
    vence = item.get("vence")
    if vence:
        dias = _dias_hasta(vence, hoy)
        if dias < 0:
            partes.append("VENCIDO")
        elif dias <= DIAS_PARA_VENCER:
            partes.append("POR VENCER")
    return " + ".join(partes) if partes else None
```

```python
# despensa/app.py  — adapters delgados a los bordes (I/O y presentación).
import json
from datetime import date

from despensa.core import evaluar


def cargar(archivo: str) -> list[dict]:
    with open(archivo, encoding="utf-8") as f:
        return json.load(f)


def alertas(items: list[dict], hoy: date) -> list[str]:
    salida = []
    for item in items:
        alerta = evaluar(item, hoy)
        if alerta is not None:
            salida.append(f"{item['nombre']}: {alerta}")
    return salida


def run(archivo: str, hoy: date | None = None) -> list[str]:
    hoy = hoy or date.today()
    resultado = alertas(cargar(archivo), hoy)
    for linea in resultado:
        print(linea)
    return resultado
```

Qué cambió y **por qué** (cada punto es un ADR candidato):

- **SRP / núcleo puro (DIP light).** La decisión vive en `evaluar`, sin tocar
  disco ni stdout. Por eso ahora se puede testear con un `dict` y una fecha, sin
  fixtures de archivos. `run` mantiene firma y salida → la caracterización sigue
  verde.
- **Magic numbers nombrados.** `2` → `STOCK_MINIMO`, `3` → `DIAS_PARA_VENCER`.
- **Nombres honestos.** `x`→`item`, `d`/`dias` explícitos, `res`→`salida`, f-strings.
- **`with open(...)`** en vez de `open`/`close` manual (recurso seguro).

## Análisis de mutation (el corazón de la evaluación)

Con **solo** la caracterización (la suite de partida), los mutantes que **mueren**
son los de **valores y strings** (la caracterización afirma la salida exacta:
`"STOCK BAJO"`, `"VENCIDO"`, `"POR VENCER"`, el formato `nombre: alerta`). Los que
**sobreviven** son los de **comparación/umbral**, porque los datos de ejemplo **no
tocan ningún borde exacto** (cantidades 0,1,5,10; días 2,-6,grande):

| Mutación sobre el umbral | ¿Sobrevive con solo caracterización? | Test de borde que lo mata |
|---|---|---|
| `cantidad <= STOCK_MINIMO` → `cantidad < STOCK_MINIMO` | **sí** (ningún item tiene cantidad == 2) | `evaluar({cantidad:2}) == "STOCK BAJO"` |
| `STOCK_MINIMO` 2 → 3 (constante) | **sí** (ningún item tiene cantidad == 3) | `evaluar({cantidad:3}) is None` |
| `dias < 0` → `dias <= 0` | **sí** (ningún item vence **hoy** exacto) | `evaluar(vence==hoy) == "POR VENCER"` |
| `dias <= DIAS_PARA_VENCER` → `dias < DIAS_PARA_VENCER` | **sí** (ningún item con dias == 3) | `evaluar(vence==hoy+3) == "POR VENCER"` |
| `DIAS_PARA_VENCER` 3 → 4 (constante) | **sí** (ningún item con dias == 4) | `evaluar(vence==hoy+4) is None` |

> **El sutil:** en `dias == 0` (vence **hoy**) el comportamiento correcto es
> **POR VENCER**, no VENCIDO —porque `0` no es `< 0`, y `0 <= 3`—. El test de ese
> borde mata el mutante `< 0` → `<= 0`. Un alumno que afirma "vencido hoy = VENCIDO"
> no leyó su propio código.

### Suite fortalecida de referencia (mata a los sobrevivientes)

```python
# tests/test_evaluar.py
from datetime import date, timedelta
from despensa.core import evaluar

HOY = date(2026, 6, 26)
def iso(dias): return (HOY + timedelta(days=dias)).strftime("%Y-%m-%d")

def test_stock_en_el_minimo_exacto_alerta():        # mata <= → <
    assert evaluar({"nombre": "x", "cantidad": 2}, HOY) == "STOCK BAJO"

def test_stock_uno_sobre_el_minimo_sin_alerta():    # mata constante 2 → 3
    assert evaluar({"nombre": "x", "cantidad": 3}, HOY) is None

def test_vence_hoy_es_por_vencer_no_vencido():      # mata dias < 0 → <= 0
    assert evaluar({"nombre": "x", "cantidad": 9, "vence": iso(0)}, HOY) == "POR VENCER"

def test_vence_en_el_borde_de_dias_alerta():        # mata dias <= 3 → < 3
    assert evaluar({"nombre": "x", "cantidad": 9, "vence": iso(3)}, HOY) == "POR VENCER"

def test_vence_un_dia_despues_del_borde_sin_alerta():  # mata constante 3 → 4
    assert evaluar({"nombre": "x", "cantidad": 9, "vence": iso(4)}, HOY) is None
```

`mutmut` genera **más** mutantes que los 5 de la tabla; el patrón es idéntico
(los vivos son siempre de comparación en bordes que la suite no pincha). El
mutation score sube a ~100% sobre el núcleo tras estos tests; el **line coverage
no se mueve** (ya estaba alto) — la prueba de que el coverage nunca fue la métrica.

## Razonamiento paso a paso (cómo debió llegar el alumno)
1. **Red primero.** Corre la herramienta, copia la salida real, la fija en la
   caracterización. Verde → permiso para tocar producción.
2. **Un smell, un commit.** Nombra god function → extrae `evaluar`. Nombra magic
   numbers → constantes. Verde en cada paso.
3. **Mide la fuerza real.** `mutmut run` → sobreviven los de umbral → agrega tests
   de **borde exacto** → re-corre hasta no dejar sobrevivientes no-equivalentes.
4. **Documenta y automatiza.** ADRs de las decisiones dudadas; CI verde.

## Puntos resbalosos (dónde mira el corrector)
1. **Caracterización tardía o ausente.** Si el commit de caracterización **no**
   precede al refactor, O1 cae a *en-progreso* aunque el código final sea bueno:
   no probó que conservó el comportamiento.
2. **Borde exacto, no aproximado.** `cantidad == 1` o `== 3` NO matan el mutante
   `<=`→`<`; solo `cantidad == 2` lo hace. `vence` en `hoy+2` no mata `<=3`→`<3`;
   debe ser `hoy+3`. Un alumno que usa "cerca del borde" no entendió.
3. **`dias == 0` = POR VENCER, no VENCIDO.** El error conceptual más común aquí.
4. **Coverage vs mutation.** Si entrega "X% coverage" como prueba de calidad,
   marcar C2 *incompleto* aunque el coverage sea 100%.
5. **Sobre-abstracción.** Una `AlertStrategy` abstracta + Factory para dos reglas
   `if` es pattern-itis; el buen alumno lo evita y lo dice en un ADR.
6. **`run` cambió de firma/salida.** Si el refactor altera el orden de las líneas
   o el formato, rompió el comportamiento: no es refactor.

## Rango de soluciones aceptables
- **Diseño:** cualquier separación que aísle un núcleo testeable sin I/O es válida
  —función pura, `@dataclass` con método, clase `Despensa` con repos inyectados—.
  No exigir ports & adapters formales (eso es Fase 3); SRP + DIP *light* basta.
- **Sujeto:** si el alumno refactoriza **su** app de Fase 1 en vez de `despensa.py`,
  evaluar el **proceso y la evidencia** con la misma rúbrica; no esperar este
  diseño concreto ni estos mutantes.
- **Lenguaje:** si portó a TS/Node (Vitest + Stryker en vez de pytest + mutmut),
  es válido siempre que el razonamiento de bordes y el ciclo sean los mismos.
- **Mutation score:** no exigir 100%. Un score < 100% es aceptable **si** los
  sobrevivientes están justificados (equivalentes, con la entrada que *debería*
  distinguirlos argumentada). Penalizar perseguir 100% con aserciones artificiales.
- **ADRs:** 2 ADRs sólidos > 5 triviales. Lo que importa es que documenten
  decisiones **dudadas** (incluida una abstracción **no** creada), no solo lo obvio.
- **Bonus (no exigible):** logging estructurado en vez de `print` (semilla de
  observabilidad, Fase 5) y mutation como gate de CI suman a *excelente*, no son
  requisito de *competente*.
