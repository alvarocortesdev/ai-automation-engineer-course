# 2.P — Capstone Fase 2: Refactor + suite de tests

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.P` Capstone (en el sitio: `/fase-2-ingenieria/proyecto/`)
**Ruta:** crítica · **Timebox:** 8–14 h repartidas en 1–2 semanas · **Modalidad:** código (proyecto)

> Este es el **capstone** de la fase: no un ejercicio de 40 minutos, sino el
> proyecto que ensambla todos los hábitos de la Fase 2 en una entrega coherente y
> que puedes fijar en tu GitHub. Lee la **lección del capstone** (`2.P`) antes de
> empezar.

## 🎯 Objetivo

Tomar un módulo que **funciona pero da vergüenza** y dejarlo en estado
*semi-senior*: SOLID aplicado donde un *code smell* lo justifica, una suite de
tests cuya calidad se mide por **mutation score** (no por coverage%), el diseño
documentado en `ARQUITECTURA.md` + ADRs, y un pipeline de CI que corre lint +
tests en cada push — todo con el comportamiento observable **intacto** (probado
por tests de caracterización).

## 📋 Contexto

Es, literalmente, el take-home más común de una entrevista semi-senior: "mejora
este módulo legado sin romperlo y convénceme de que no lo rompiste". El sujeto
puede ser:

- **Tu app de la Fase 1** (la mini-API de despensa en Python o TS), **o**
- el **`despensa.py`** provisto en esta carpeta, si tu app de la Fase 1 quedó
  demasiado simple para lucir un refactor.

`despensa.py` es una "versión junior" deliberada: una sola función que lee un
archivo, decide alertas de stock/vencimiento e imprime — con magic numbers,
nombres mudos y cero tests. Ya viene con una **red de caracterización** de partida
(`tests/test_caracterizacion.py`) en verde para que practiques el ciclo correcto.

## 📏 Primero-Sin-IA

1. Trabaja **solo** (timebox arriba). La IA entra **al final**, para *revisar y
   explicar* tu refactor y tus tests — nunca para *generarlos*.
2. Consulta **documentación oficial** (Fowler, pytest, mutmut, ruff) cuando la
   necesites.
3. El orden importa y casi siempre se hace al revés: **red de tests primero**,
   refactor después.
4. Reescribe de memoria, a la semana, el **ciclo de tres pasos**. Si no puedes, no
   lo aprendiste todavía.

## 🛠️ Instrucciones (en este orden)

### Paso 0 — Confirma el punto de partida

```bash
uv sync --all-extras --dev
uv run pytest -q                                  # la caracterización debe estar VERDE
uv run python despensa.py tests/datos/despensa-ejemplo.json
```

Si no está verde, arregla tu entorno antes de seguir (no el ejercicio).

### Paso 1 — Spec + red de caracterización

- Escribe `SPEC.md`: propósito, entradas, salidas, **casos borde** (¿qué pasa con
  `cantidad == 2`? ¿con un item vencido **hoy** exactamente?).
- Si usas tu propia app de Fase 1, escribe **tú** los tests de caracterización que
  fijan su comportamiento actual, igual que el provisto aquí. Confirma verde
  **antes** de cambiar una línea de producción.
- Commit: `test: red de caracterizacion`.

### Paso 2 — Refactor guiado por smells

- Recorre el catálogo de la lección `2.3` (Code smells + refactoring): **nombra**
  cada smell (god function, magic numbers, nombres mudos, condicional anidado,
  mezcla de I/O y lógica).
- Por cada smell, aplica su refactoring en un **commit pequeño** y confirma que la
  red sigue verde. Extrae al menos un **núcleo puro** sin I/O (SRP) e **inyecta**
  sus dependencias (DIP light), de modo que se pueda testear sin archivos ni `print`.
- Aplica SOLID **solo donde el smell lo justifique** (lee la advertencia sobre
  sobre-abstracción en la lección `2.4`, SOLID con crítica).

### Paso 3 — Tests unitarios + mutation

- Testea el núcleo puro: casos normales, **bordes exactos**, errores.
- Corre mutation testing y **mata a los sobrevivientes** con tests de borde:

  ```bash
  uv run mutmut run        # corre la suite contra cada mutante
  uv run mutmut results    # lista los mutantes y su estado
  uv run mutmut browse     # TUI para inspeccionar sobrevivientes ('q' para salir)
  ```

- Reporta el **mutation score de partida y final**. Si queda algún sobreviviente,
  justifícalo (p. ej. mutante **equivalente**: muestra qué entrada *debería*
  distinguirlo y por qué no existe).

### Paso 4 — Documentación

- `ARQUITECTURA.md` (en **inglés**) — usa `ARQUITECTURA.template.md`.
- **2–3 ADRs** en `docs/adr/` — usa `docs/adr/0001-record-architecture-decisions.md`
  como plantilla. Documenta las decisiones que **dudaste** (incluida una
  abstracción que decidiste **no** crear).

### Paso 5 — Pipeline de CI

- Copia `ci.example.yml` a `.github/workflows/ci.yml` de tu repo. Que corra lint +
  tests en cada push y quede **verde**.

## ✅ Criterios de "hecho" (mapeados al Definition of Done del curso)

- [ ] **DoD 1** — Existe `SPEC.md` y **2–3 ADRs** que defienden las decisiones de
      diseño (no "porque sí").
- [ ] **DoD 2** — CI verde con lint + tests; calidad reportada por **mutation
      score** (no por % de coverage); sobrevivientes restantes justificados.
- [ ] El **refactor es real**: el comportamiento observable no cambió (la
      caracterización sigue verde) y la estructura mejoró (SOLID donde el smell lo
      pedía, smells eliminados).
- [ ] **DoD 8** — La herramienta **ejecuta**; `ARQUITECTURA.md`/README en
      **inglés**; write-up de trade-offs (qué elegiste, qué mediste, qué te costó,
      qué decidiste **no** testear).
- [ ] **DoD 9** — **Conventional Commits** en todo el historial, en pasos pequeños
      que dejan la red verde.
- [ ] Puedes **defender** sin notas el ciclo de tres pasos y cada decisión (check
      de dominio de la lección).

> **Fuera de alcance esta fase** (llega después, mismo DoD): seguridad OWASP
> (no hay endpoint → Fase 3), observabilidad con trazas (Fase 5), eval harness
> (Fase 6), a11y WCAG (Fase 4). *Bonus* honesto: cambiar los `print` por **logging
> estructurado** (lección `2.12`, Debugging y código legado).

## 📦 Qué entregar

En el repo de tu proyecto (o en esta carpeta, si refactorizas `despensa.py`):

- `SPEC.md`, `ARQUITECTURA.md`, `docs/adr/*.md`
- El código refactorizado + la suite de tests (caracterización + unitarios)
- El reporte de mutation score (en `ARQUITECTURA.md` o un `MUTATION.md`)
- El workflow `.github/workflows/ci.yml` (en tu repo) y el historial de commits

## 💡 Pista (ábrela solo si no sabes por dónde partir)

<details>
<summary>Mostrar pista</summary>

No empieces por el código bonito; empieza por la **red**. Corre la herramienta,
copia su salida real y fíjala en un test de caracterización. Recién con ese test
verde tienes permiso de tocar producción. De ahí, el ciclo es siempre pequeño:
nombra **un** smell → aplícale su refactoring en **un** commit → confirma que la
red sigue verde → repite. Cuando exista el núcleo puro, mídete con `mutmut`: los
mutantes vivos te dicen **exactamente** qué borde no probaste (casi siempre un
`<=`/`<` en un umbral). Para los ADRs, escribe el que **dudaste**.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu proyecto (repo o esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-2/capstone-refactor-tests.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

> "Corrige mi capstone `ejercicios/fase-2/capstone-refactor-tests/` usando el
> framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."

La **solución de referencia** vive en
`.ai/soluciones/fase-2/capstone-refactor-tests.md` — no la mires antes de
intentarlo de verdad.
