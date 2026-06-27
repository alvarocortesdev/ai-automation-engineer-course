# pipeline-matriz-gate — Diseña el pipeline completo: matriz, caché, gate y trade-offs

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.3` CI/CD con GitHub Actions
**Ruta:** crítica · **Timebox:** 40–45 min · **Modalidad:** mixto (YAML + write-up)

## 🎯 Objetivo

Escribir un workflow de release con **matriz** de versiones, **caché**, jobs
encadenados (`needs`) y un **deploy gated** (rama + environment + secret), **y**
justificar por escrito las decisiones: por qué `needs` y `if` son ortogonales, la
diferencia entre secret de repo y de environment, qué bloquea de verdad un merge, y
el trade-off de costo de la matriz.

## 📋 Contexto

Es el pipeline completo del **Capstone F5 — Pipeline a producción**: la columna
vertebral `lint → test → build → deploy` con la forma profesional. Aquí practicas las decisiones que separan un
"YAML de tutorial" de un pipeline que un equipo confiaría: gates, mínimo privilegio,
y costo consciente. La parte de razonamiento (write-up) es deliberadamente lo más
importante: el YAML lo genera cualquiera; el criterio, no.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). El write-up va **sin IA**: es tu criterio.
2. Solo entonces, consulta **documentación oficial** (`docs.github.com/actions`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *escribir tu razonamiento*.
4. Mañana, **reescribe el `release.yml` de memoria** y vuelve a responder (c). Si no puedes, repasa.

## 🛠️ Instrucciones

1. Reescribe `.github/workflows/release.yml` (hay un starter con TODOs) con tres jobs:
   - **`test`** — `strategy.matrix.python-version: ["3.11", "3.12", "3.13"]`, setup-uv con
     `enable-cache: true`, e instala con `uv sync --frozen` antes de lint + pytest.
   - **`build`** — `needs: test`; produce y sube un artefacto con `actions/upload-artifact`.
   - **`deploy`** — `needs: build`; `if:` que lo limite a **push a `main`**;
     `environment: production`; inyecta `DEPLOY_TOKEN` como `${{ secrets.DEPLOY_TOKEN }}`.
2. Valida la estructura:

   ```bash
   uv add --dev pyyaml        # una sola vez (o: pip install pyyaml)
   uv run pytest test_workflow.py
   ```

3. Completa `write-up.md` (los cuatro puntos a–d). **A mano, sin IA.**

> Versiones vigentes (jun 2026): `actions/checkout@v7`, `astral-sh/setup-uv@v8`,
> `actions/upload-artifact@v7`. Verifícalas en el repo oficial de cada action.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest test_workflow.py` pasa (matriz de 3, caché, `needs` correctos,
      deploy con `if:` de rama + `environment: production`, secret referenciado).
- [ ] El secret se referencia con `${{ secrets.DEPLOY_TOKEN }}`, **nunca** en texto plano.
- [ ] El write-up distingue lo que hace `if:`/`needs:` (dentro del workflow) de lo que
      hace la **branch protection** (gate de merge real) y la **nombra con precisión**.
- [ ] El write-up pesa **costo vs riesgo** en la matriz (no "más siempre es mejor").
- [ ] Puedes defender en voz alta cada respuesta del write-up sin notas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el YAML: `needs:` define **orden de ejecución** (build espera a test; deploy a
build); `if:` define **bajo qué condición** corre un job (solo push a main). Son cosas
distintas y se combinan. Para el write-up (c), la trampa es creer que el `if:` protege
`main` — no lo hace: el `if:` vive en el workflow, que solo *reporta*; el bloqueo del
merge vive en **Settings → Rules** del repo (required status checks). Para (d),
pregúntate: ¿hay usuarios reales corriendo este código en esas tres versiones?

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu IA:

- tu solución (este directorio, con tu `release.yml` y tu `write-up.md`),
- la **rúbrica**: `.ai/rubricas/fase-5/pipeline-matriz-gate.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/pipeline-matriz-gate.md`
— no la mires antes de intentarlo de verdad.
</content>
