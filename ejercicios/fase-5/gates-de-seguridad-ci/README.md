# gates-de-seguridad-ci — Endurece el pipeline de la 5.3 con gates de supply chain

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.4` Gates de seguridad y supply chain en CI
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código (config YAML + test estructural)

## 🎯 Objetivo

Tomar el `ci.yml` de la 5.3 (solo lint → test) y convertirlo en un pipeline con
**gates de supply chain**: SCA (dependency scanning), secret-scanning, permisos
mínimos y **actions pineadas a SHA**; más un `dependabot.yml` que mantenga las
dependencias al día sin abrir 20 PRs.

## 📋 Contexto

Es el punto del **Definition of Done** del Capstone F5 que dice "secret-scanning +
dependency-scanning (SCA) en el pipeline". Aquí lo construyes en miniatura. El YAML lo
genera cualquiera; lo que se evalúa es que entiendas **qué ataque cierra cada gate** y
por qué `@v4` no basta tras el incidente de Trivy.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Reusa el esqueleto de la 5.3 y **añade** gates.
2. Solo entonces, consulta **documentación oficial** (`docs.github.com/code-security`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *escribir tu YAML*.
4. Mañana, **reescribe los gates de memoria** y explica qué ataque previene cada uno. Si no puedes, repasa.

## 🛠️ Instrucciones

1. Edita `.github/workflows/ci.yml` (tiene TODOs):
   - **TODO 1** — `permissions: contents: read` a nivel global (mínimo privilegio).
   - **TODO 2** — pinea **todas** las actions a un **SHA** de 40 hex (deja el tag en un comentario).
     No verifiques el SHA contra red; usa los de ejemplo del header del starter o cópialos de GitHub.
   - **TODO 3** — gate de **SCA**: un job con `uvx pip-audit`, **o** un job con `actions/dependency-review-action`.
   - **TODO 4** — gate de **secret-scan**: un job con `gitleaks/gitleaks-action` cuyo checkout use `fetch-depth: 0`.
2. Crea `.github/dependabot.yml`: `version: 2`, con entradas para **`github-actions`** y **`pip`**,
   usando `groups` (y, mejor, `cooldown`).
3. Valida la estructura:

   ```bash
   uv sync --frozen          # o: pip install pyyaml pytest
   uv run pytest test_seguridad.py
   ```

4. Itera hasta el verde. (`test_app.py` ya pasa; no edites `app.py`.)

> Versiones vigentes (jun 2026), por si las quieres reales: `actions/checkout@v5`,
> `astral-sh/setup-uv@v6`, `gitleaks/gitleaks-action@v3`, `actions/dependency-review-action@v4`,
> `github/codeql-action@v4`. **Pero el test exige el SHA, no el tag** — esa es la lección.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest test_seguridad.py` pasa (permisos mínimos, SHA en todas las actions, gate de SCA,
      gate de secret-scan con `fetch-depth: 0`, `dependabot.yml` válido con `groups`).
- [ ] Ninguna action usa `@main` ni un tag móvil; todas a SHA con el tag legible en un comentario.
- [ ] `dependabot.yml` agrupa actualizaciones en vez de un PR por dependencia.
- [ ] Puedes **explicar sin notas** qué ataque cierra cada gate (SCA, secret-scan) y por qué el pin a SHA importa.
- [ ] Puedes decir qué configuras **además del YAML** para que un PR con un CVE crítico no se pueda mergear
      (pista: *required status checks*, como en la 5.3).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Cada gate es **un job más** dentro de `jobs:` — no reescribas el workflow, **añade**. Para el SHA,
recuerda que el test solo exige 40 caracteres hex (no un tag): el formato es
`uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8  # v5.0.0`. El job de gitleaks
necesita `with: fetch-depth: 0` en su `checkout` o solo ve el último commit. Para `dependabot.yml`,
necesitas **dos** entradas bajo `updates:` (una `github-actions`, una `pip`), cada una con un bloque
`groups:`. Si un assert falla, su mensaje dice qué falta. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu IA:

- tu solución (este directorio, con tu `ci.yml` y tu `dependabot.yml`),
- la **rúbrica**: `.ai/rubricas/fase-5/gates-de-seguridad-ci.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/gates-de-seguridad-ci.md`
— no la mires antes de intentarlo de verdad.
