---
ejercicio_id: fase-5/primer-pipeline-ci
fase: fase-5
sub_unidad: "5.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay variantes válidas: lo que
> importa es que cumpla las propiedades estructurales y que el alumno **pueda explicar** cada decisión.

# Solución de referencia — Tu primer pipeline: lint → test en cada PR

## Cómo usar esta solución

El alumno entrega `.github/workflows/ci.yml`. La señal objetiva es `test_workflow.py` en verde.
La señal **pedagógica** es si puede explicar el orden de steps y el modelo de gate (workflow reporta,
branch protection bloquea). Un YAML verde pero indefendible es `en-progreso`, no `competente`.

## `ci.yml` de referencia (una versión correcta)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v8
        with:
          enable-cache: true
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run pytest
```

## Por qué cada pieza (lo que el alumno debe poder defender)

- **Dos triggers.** `push: { branches: [main] }` verifica lo que entra a la rama principal;
  `pull_request:` (sin filtro) corre en **todos** los PRs — es el check que condicionará el merge.
  Faltar uno es un error frecuente: solo `push` deja los PRs sin check.
- **`permissions: contents: read`.** Mínimo privilegio: el `GITHUB_TOKEN` solo lee el repo. Sin este
  bloque, hereda permisos más amplios. Hábito de seguridad desde el primer pipeline (se profundiza en 5.4).
- **`concurrency` + `cancel-in-progress`.** Opcional pero "excelente": cancela runs viejos del mismo ref
  cuando llegan pushes seguidos. Ahorra minutos = ahorra plata.
- **Orden de steps.** `checkout` **primero** (el runner arranca vacío); luego el toolchain (`setup-uv`),
  luego `uv sync --frozen` (instala EXACTO el lockfile → reproducible), luego lint (rápido, barato fallar
  aquí) y al final los tests (lo más lento).
- **Pins.** `@v7`, `@v8`: nunca `@main` en una action ajena (es código de un tercero con acceso al repo).
  El pin a commit SHA es el siguiente nivel (5.4).

## El punto que cierra el ejercicio (O3)

Aunque el `ci.yml` sea perfecto, **por sí solo no impide mergear un PR con CI en rojo**. Para eso hace
falta configurar, *fuera del YAML*, una **branch protection rule / ruleset** sobre `main` con
**"Require status checks to pass before merging"**, eligiendo el check `test` como obligatorio. El
workflow *reporta* verde/rojo; la branch protection *bloquea*. Si el alumno no menciona esto, no logró O3
aunque el test pase.

## Notas para el corrector

- **Gotcha de YAML 1.1:** la clave `on:` se parsea como el booleano `True` en PyYAML; por eso el test
  acepta `data[True]`. No es un error del alumno; es del parser. No lo penalices.
- Variantes válidas: usar `actions/setup-python@v6` + `cache: 'pip'` en vez de `setup-uv` es aceptable
  si el alumno justifica el cambio de stack (aunque el curso usa `uv`). El orden y el gate no cambian.
- Si el alumno añadió matriz/varios OS "porque sí" en el pipeline más simple, señálalo: complejidad sin
  riesgo que la justifique (eso es el ejercicio 2, con su trade-off explícito).
</content>
