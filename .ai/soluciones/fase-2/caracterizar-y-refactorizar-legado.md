---
ejercicio_id: fase-2/caracterizar-y-refactorizar-legado
fase: fase-2
sub_unidad: "2.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Caracteriza y refactoriza código legado (sin red)

## Paso 1 — Red de caracterización canónica (`test_solucion.py`)

```python
import pytest
from solucion import etiqueta_envio

@pytest.mark.parametrize("peso, zona, esperado", [
    # zona 1 (local) — bordes 500 y 2000
    (499, 1, "local-ligero"),
    (500, 1, "local-medio"),
    (1999, 1, "local-medio"),
    (2000, 1, "local-pesado"),
    # zona 2 (nacional) — mismos umbrales
    (499, 2, "nacional-ligero"),
    (500, 2, "nacional-medio"),
    (1999, 2, "nacional-medio"),
    (2000, 2, "nacional-pesado"),
    # zona 3 (internacional) — umbral DISTINTO: 1000
    (999, 3, "internacional-estandar"),
    (1000, 3, "internacional-especial"),
    # zona desconocida: HOY se comporta como internacional (rareza preservada)
    (100, 5, "internacional-estandar"),
    (5000, 5, "internacional-especial"),
])
def test_caracteriza_etiqueta_envio(peso, zona, esperado):
    assert etiqueta_envio(peso, zona) == esperado
```

Estos `esperado` son el **golden master**: lo que la función hace hoy (verificado).
No son "lo correcto"; son "lo que hay". Toda la suite pasa contra el código original.

## Paso 2 — Refactor canónico (`solucion.py`), comportamiento idéntico

```python
UMBRAL_MEDIO = 500
UMBRAL_PESADO = 2000
UMBRAL_INTERNACIONAL = 1000


def tamano_por_peso(peso_gramos):
    if peso_gramos < UMBRAL_MEDIO:
        return "ligero"
    if peso_gramos < UMBRAL_PESADO:
        return "medio"
    return "pesado"


def etiqueta_envio(peso_gramos, zona):
    if zona == 1:
        return f"local-{tamano_por_peso(peso_gramos)}"
    if zona == 2:
        return f"nacional-{tamano_por_peso(peso_gramos)}"
    # zona 3 y CUALQUIER otra: comportamiento legado preservado a propósito.
    if peso_gramos < UMBRAL_INTERNACIONAL:
        return "internacional-estandar"
    return "internacional-especial"
```

> Verificado de forma **exhaustiva** (peso 0–3000, zonas 0/1/2/3/4/5/99): la versión
> refactorizada devuelve exactamente lo mismo que la original para todos los casos,
> incluida la `zona` desconocida.

## Mapa smell → refactoring (lo que `notas.md` debería contener)

| Smell | Refactoring | Detalle |
|---|---|---|
| Duplicated Code (zona 1 ≈ zona 2: mismos umbrales 500/2000) | Extract Function (`tamano_por_peso`) | el corazón del ejercicio |
| Nested Conditional (`if` dentro de `if` dentro de `else`) | Decompose Conditional / guardas con `return` | aplanar a 3 guardas |
| Mysterious structure (prefijo de zona disperso) | Replace literal con composición `f"{prefijo}-{tamano}"` | una sola plantilla |
| Magic Numbers (500, 2000, 1000) | Replace Magic Literal with Symbolic Constant | constantes nombradas |

## Razonamiento paso a paso (el orden que debió recorrer)
1. **Red primero.** Escribe el `parametrize` golden master y córrelo → **verde** contra el código sin tocar. (Si el alumno refactorizó antes de esto, es C1/C2 incompleto sin importar cuán bonito quede.)
2. **Extract `tamano_por_peso`** y úsalo en zonas 1 y 2. Correr → verde.
3. **Aplanar** los condicionales a guardas con `return`. Correr → verde.
4. **Componer** con f-string el prefijo + tamaño. Correr → verde.
5. **Anotar** en `notas.md` que la `zona` desconocida se preservó a propósito (deuda separada).

## Puntos resbalosos (donde el corrector debe mirar)
1. **La rareza de la `zona` desconocida es el examen real.** El refactor "ingenuo" tiende a meter un `if zona == 3` explícito y dejar las demás zonas sin rama → cambia el comportamiento de `zona=5` (rompería el test de caracterización). La referencia preserva la semántica del `else` original: "zona 3 **y cualquier otra**". Si el alumno "arregló" la zona 5 (devolver error / "desconocida"), **cambió el comportamiento** → C3 incompleto, aunque parezca "más correcto". Eso es exactamente la lección de los dos sombreros.
2. **Umbral distinto en internacional (1000, no 500/2000).** Si el alumno intenta reusar `tamano_por_peso` para zona 3, rompe la caracterización. La rama internacional es genuinamente distinta.
3. **Bordes con `<` vs `<=`.** El original usa `<`: 500 → "medio" (no "ligero"). Un test con `<=` mal copiado fallaría; cazar.
4. **El `esperado` no se toca al refactorizar.** Si el alumno cambió algún `esperado` en el paso 2, dejó de ser caracterización.

## Rango de soluciones aceptables
- **`tamano_por_peso` que devuelva un enum/constante** en vez de strings: válido si compone igual.
- **Un dict `{1: "local", 2: "nacional"}`** para el prefijo doméstico + fallback internacional: válido y elegante.
- **Mantener `if/elif/else`** en `tamano_por_peso` en vez de guardas: equivalente.
- **Comentar la `zona` desconocida como `# TODO: fix en commit aparte`** y dejar un test marcado `xfail` para el comportamiento *deseado* futuro: **excelente** (demuestra los dos sombreros como flujo).
- **No extraer el prefijo a un dict** (dejar dos `if` con f-string): aceptable, sigue eliminando la duplicación del tamaño.
- Lo que **no** es aceptable: cualquier versión donde `etiqueta_envio(700, 5)` deje de devolver `"internacional-estandar"`.
