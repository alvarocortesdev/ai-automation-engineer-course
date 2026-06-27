---
ejercicio_id: fase-5/pipeline-matriz-gate
fase: fase-5
sub_unidad: "5.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). El write-up **no tiene respuesta
> única**: mide si el alumno distingue `needs`/`if`, nombra la branch protection, y pesa el costo de la
> matriz con un ejemplo propio. Una respuesta contraria bien fundada es `competente`/`excelente`.

# Solución de referencia — Pipeline completo: matriz, caché, gate y trade-offs

## `release.yml` de referencia (una versión correcta)

```yaml
name: Release

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v8
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v8
      - run: uv build
      - uses: actions/upload-artifact@v7
        with:
          name: dist
          path: dist/

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v7
      - run: ./deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

## Write-up de referencia (respuestas defendibles)

**(a) `needs: build` + `if:` — ortogonales.** `needs:` es una dependencia de **ejecución**: no empieces
`deploy` hasta que `build` (y, transitivamente, `test`) termine en verde. `if:` es un **filtro de cuándo**
corre el job: solo en un push a `main`, nunca en un PR. Uno responde "¿después de qué?", el otro "¿solo si?".
No son redundantes: sin `if:`, el deploy correría también al construir desde un PR; sin `needs:`, podría
intentar deployar en paralelo a un build aún no terminado.

**(b) Secret de repo vs de environment.** Un **secret de repo** está disponible para cualquier workflow/job
del repositorio. Un **secret de environment** (`production`) solo se expone a los jobs que declaran
`environment: production`, y el environment puede tener **reglas de protección** (aprobación manual,
restricción de ramas, espera). Uso: el token de **prod** va como secret del environment `production`
(blindado, con aprobación); valores compartidos no sensibles o de **staging** pueden ir a nivel de repo o a
un environment `staging` distinto. La ventaja clave: separar prod de staging y exigir una puerta antes de
tocar producción.

**(c) El gate de PR real.** El `release.yml` **reporta** verde/rojo pero no impide el merge. Para bloquear
un PR con CI en rojo hay que configurar, fuera del YAML, una **branch protection rule / ruleset** sobre
`main` (Settings → Rules) con **"Require status checks to pass before merging"**, marcando el check `test`
como obligatorio. Eso pone el botón de merge en gris hasta que el pipeline pase. El workflow es el examen;
la branch protection es el reglamento que hace obligatorio aprobarlo.

**(d) Trade-off de la matriz.** La matriz de 3 versiones = 3× los minutos de CI (y 3× el costo). **Se
justifica** cuando hay usuarios reales corriendo el código en esas versiones —p. ej. una **librería pública**
que declara soporte para 3.11–3.13: cada celda cubre el riesgo real de "rompe en 3.11 pero no en 3.13".
**Es desperdicio** cuando el código corre en un solo runtime controlado —p. ej. un **servicio interno** que
solo se despliega en un contenedor con Python 3.13: ahí la matriz multiplica costo sin cubrir ningún riesgo
que exista. La pregunta no es "¿puedo?", es "¿qué riesgo concreto cubre cada celda?".

## Notas para el corrector

- Variantes válidas: usar `actions/cache` explícito en vez de `enable-cache: true`; un `build` con
  `python -m build` en vez de `uv build`; `environment` como mapeo `{ name: production }`. El test las acepta.
- **Gotcha YAML 1.1:** `on:` se parsea como `True`; no es error del alumno.
- Penaliza solo el **fondo**: secret en claro, deploy no gated, o creer que el `if:` bloquea el merge. La
  forma exacta del YAML tiene grados de libertad.
- Si el write-up está impecable pero el YAML falla (o viceversa), nómbralo: en un ejercicio mixto se evalúan
  ambos. Un razonamiento prestado de IA suele sonar a documentación sin ejemplo propio en (b) y (d).
</content>
