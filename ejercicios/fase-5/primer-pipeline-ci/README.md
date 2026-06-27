# primer-pipeline-ci — Tu primer pipeline: lint → test en cada PR

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.3` CI/CD con GitHub Actions
**Ruta:** crítica · **Timebox:** 30–40 min · **Modalidad:** código (YAML)

## 🎯 Objetivo

Escribir **desde cero** el workflow de CI de un proyecto Python con `uv`: que en
cada `push` a `main` y en cada `pull_request` corra, sobre un runner limpio, el
pipeline **checkout → setup → install → lint → test**, con permisos mínimos y
actions pineadas a una versión.

## 📋 Contexto

Es el esqueleto de la Fase 5. El **Capstone F5 — Pipeline completo a producción**
crece exactamente desde este workflow: aquí montas el `lint → test`; en la **5.4**
(seguridad y supply chain) le sumas gates de seguridad, y el build/deploy vienen
después. Si entiendes esta forma, las próximas lecciones solo le agregan jobs.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que tengas que mirar la doc.
2. Solo entonces, consulta **documentación oficial** (`docs.github.com/actions`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el YAML.
4. Mañana, **reescribe el `ci.yml` de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. `app.py` y `test_app.py` ya están listos y pasan: **no los toques**. Son lo que
   tu pipeline debe lintear y testear.
2. Reescribe `.github/workflows/ci.yml` (hay un starter con TODOs) para que cumpla:
   - Se dispara en **`push` a `main`** y en **todo `pull_request`**.
   - Declara `permissions: { contents: read }` (mínimo privilegio).
   - Tiene un job `test` en `ubuntu-latest` cuyos steps, **en orden**, son:
     `actions/checkout` → `astral-sh/setup-uv` → `uv sync --frozen` →
     `uv run ruff check .` → `uv run pytest`.
   - Todas las actions pineadas a un **tag de versión** (`@v7`, `@v8`…), nunca `@main`.
3. Valida la **estructura** de tu YAML (no necesitas GitHub):

   ```bash
   uv add --dev pyyaml        # una sola vez (o: pip install pyyaml)
   uv run pytest test_workflow.py
   ```

4. Itera hasta que `test_workflow.py` esté **verde**. Cada assert te dice qué falta.

> Las versiones vigentes (jun 2026): `actions/checkout@v7`, `astral-sh/setup-uv@v8`.
> Verifícalas en el repo oficial de cada action; no las memorices.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest test_workflow.py` pasa (triggers, permisos, orden de steps, pins).
- [ ] El `checkout` es el **primer** step y `pytest` el último.
- [ ] Ninguna action usa `@main` ni una rama; todas usan un tag de versión.
- [ ] Puedes **explicar sin notas** qué hace cada step y por qué va en ese orden.
- [ ] Puedes decir qué tendrías que configurar **además del YAML** para que un PR
      con CI en rojo no se pueda mergear (pista: no vive en el `.yml`).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por las tres claves de nivel superior: `name:`, `on:`, `jobs:`. Bajo `on:`
necesitas **dos** triggers: `push` con `branches: [main]`, y `pull_request:` (sin
filtro, para que corra en todos los PRs). El runner arranca **vacío**: si el primer
step no es `checkout`, nada de lo que sigue encuentra tu código. Lee `test_workflow.py`:
es tu spec — cada función de test nombra una propiedad que tu YAML debe cumplir.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu IA:

- tu solución (este directorio, con tu `ci.yml`),
- la **rúbrica**: `.ai/rubricas/fase-5/primer-pipeline-ci.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/primer-pipeline-ci.md`
— no la mires antes de intentarlo de verdad.
</content>
