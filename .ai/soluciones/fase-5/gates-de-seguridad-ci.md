---
ejercicio_id: fase-5/gates-de-seguridad-ci
fase: fase-5
sub_unidad: "5.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay grados de libertad en la
> forma del YAML; penaliza el **fondo** (tag en vez de SHA, secreto en claro, gate sin criterio),
> no las variantes válidas.

# Solución de referencia — Gates de supply chain en CI

## `ci.yml` de referencia (una versión correcta)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read           # mínimo privilegio global

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v5.0.0
      - uses: astral-sh/setup-uv@e92bafb6253dcd438e0484186d7669ea7a8ca1cc # v6.4.3
        with:
          enable-cache: true
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run pytest

  sca:                       # gate de SCA (escanea el árbol instalado contra CVEs)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v5.0.0
      - uses: astral-sh/setup-uv@e92bafb6253dcd438e0484186d7669ea7a8ca1cc # v6.4.3
      - run: uv sync --frozen
      - run: uvx pip-audit

  secret-scan:               # gate de secret-scanning (historial completo)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v5.0.0
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@ff98106e4c7b2bc287b24eaf42907196329070c7  # v3
```

Variante igualmente válida del gate de SCA en PRs (en vez de, o además de, `pip-audit`):

```yaml
  dependency-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v5.0.0
      - uses: actions/dependency-review-action@56339e523c0409420f6c2c9a2f4292bbb3c07dd3  # v4
        with:
          fail-on-severity: high
```

Extra `excelente` (job de SAST con permiso puntual):

```yaml
  sast:
    runs-on: ubuntu-latest
    permissions:
      security-events: write     # CodeQL escribe sus hallazgos; el resto sigue en contents: read
      contents: read
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v5.0.0
      - uses: github/codeql-action/init@4e94bd11f71e507f7f87df81788dff88d1dacbfb     # v4
        with:
          languages: python
      - uses: github/codeql-action/analyze@4e94bd11f71e507f7f87df81788dff88d1dacbfb  # v4
```

## `dependabot.yml` de referencia

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions:
        patterns: ["*"]

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    cooldown:
      default-days: 7        # no adoptar una versión hasta que tenga 7 días (defensa anti-malware reciente)
    groups:
      python-deps:
        patterns: ["*"]
```

## El razonamiento que el alumno debe poder defender

- **¿Qué ataque cierra cada gate?** SCA → CVEs conocidos en código de terceros que importas (A06 de OWASP web, automatizado). Secret-scanning → credenciales filtradas al repo. SAST → bugs de seguridad en *tu* código (inyección, etc.). Son **superficies distintas**; ninguna sustituye a otra.
- **¿Por qué SHA y no tag?** Un tag es **mutable**: lo movieron en el ataque a `aquasecurity/trivy-action` (marzo 2026, 76/77 tags reescritos a malware). El SHA del commit es la única referencia inmutable de git. `@v4` es mejor que `@main`, pero solo `@<sha>` inmuniza contra el tag hijacking. Dependabot mantiene el SHA al día.
- **¿Por qué `groups` + `cooldown`?** `groups` evita la fatiga de PRs (un PR revisable vs. 20 sueltos que se aprueban a ciegas). `cooldown` no adopta versiones recién publicadas, dándole tiempo a la comunidad a detectar un compromiso.
- **¿Qué falta además del YAML para que un PR rojo no se mergee?** El *required status check* en la **branch protection / ruleset** (igual que la 5.3): hay que marcar `sca`, `secret-scan`, etc. como obligatorios. El YAML reporta; la branch protection bloquea.

## Notas para el corrector

- **Variantes válidas:** orden de jobs distinto; `pip-audit` vs. `dependency-review` (cualquiera satisface el gate de SCA); `npm audit`/Trivy si el proyecto fuera Node; SHA distintos (el test solo exige 40 hex, no el SHA real de esa versión); `cooldown` ausente (es bonus, no obligatorio).
- **Gotcha YAML 1.1:** `on:` se parsea como `True`; no es error del alumno y el test no lo toca.
- **Penaliza el fondo, no la forma:** tag en vez de SHA, secreto en claro, `permissions: write-all`, gitleaks sin `fetch-depth: 0`, o no poder explicar qué ataque cierra cada gate.
- Si el YAML pasa pero el alumno no distingue SAST/SCA/secret-scanning al explicarlo, está en `en-progreso` de comprensión aunque el test esté verde: nómbralo.
