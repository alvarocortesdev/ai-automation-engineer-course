---
name: extender-curso
description: Añade o modifica una lección/sub-unidad del curso AI/Automation Engineer respetando la ANATOMÍA DE LECCIÓN estándar (11 partes), los hilos transversales (testing, evals, seguridad, observabilidad, spec-driven, costo/latencia, inglés, empleabilidad, active recall) y el Definition of Done de los capstones. Úsala cuando quieras crear, expandir, reordenar o corregir contenido del curso a futuro con IA. Incluye el CONTRATO DE LECCIÓN como template copiable y el mapa exacto de rutas (src/content/docs, ejercicios/, .ai/rubricas, .ai/soluciones, progreso.md).
---

# Extender el curso (autor de contenido)

> Skill de RE-ITERACIÓN. Sirve para **mantener y crecer** el curso después del build inicial: añadir una sub-unidad nueva, expandir una corta, reordenar, marcar opcional o corregir un dato. Toda lección que entra al curso pasa por aquí.

## 0. Insumos de contrato (leer antes de escribir)

- `ROADMAP.md` — columna vertebral; ids y títulos oficiales de las sub-unidades.
- `CURRICULUM-REVIEW.md` (si está en el repo) — secciones **E** (anatomía + rúbrica), **B** (hilos transversales + DoD), **D** (build list con marcas ruta-crítica/opcional). Es la fuente de verdad pedagógica.
- `.ai/INSTRUCCIONES-CORRECTOR.md` — cómo se corregirán los ejercicios que generes (debe poder corregirse con lo que escribas).

No inventes ids ni títulos: cópialos del build list (§D). Cada sub-unidad tiene una marca **[ruta-crítica]** o **[opcional/profundización]** — respétala; las opcionales **nunca se eliminan** (por diseño del curso), solo se marcan.

## 1. Convención de identidad de una sub-unidad

| Campo | Regla | Ejemplos |
|---|---|---|
| `id` | El del build list, literal | `0.1`, `1.10`, `6.0b`, `7.5a`, `N.P` (capstone), `T0.4` |
| `fase` | `fase-0` … `fase-8`; track paralelo = `track-0` | `fase-6`, `track-0` |
| `slug` | `<id>-<kebab-corto-en-español>` | `6.0b-puente-ml-dl`, `0.1-mentalidad`, `7.P-capstone-agentico` |
| `ruta` | `critica` u `opcional` (de la marca del build list) | `critica` |

El `slug` es la llave que comparten lección, ejercicios, rúbrica y solución. Si renombras, renombra los cuatro.

## 2. Mapa de archivos (dónde va cada cosa)

> `fase-N` = `fase-0`…`fase-8` o `track-0`. `<slug>` como en §1.

| Artefacto | Ruta | Visibilidad |
|---|---|---|
| **Lección publicable** (Astro Starlight) | `src/content/docs/fase-N/<slug>.md` | Pública (la lee el alumno) |
| **Ejercicios** (enunciados + andamiaje) | `ejercicios/fase-N/<slug>/` | Pública |
| **Rúbrica** (criterios de corrección) | `.ai/rubricas/fase-N/<slug>.md` | Privada (corrector) |
| **Solución de referencia** anotada | `.ai/soluciones/fase-N/<slug>/` | Privada (corrector) |
| **Dashboard de avance** | `progreso.md` | Pública |

Reglas duras:
- **Nada de `.ai/` se referencia ni se enlaza desde la lección pública.** La solución completa vive solo en `.ai/soluciones/`. Lo que el alumno ve para autocorregirse es un bloque "solución de referencia" *dentro* de la lección, revelable **después** del intento (collapsible), más breve que la de `.ai/`.
- No toques `src/` config ni `package.json` desde esta skill — solo creas/editas archivos de contenido `.md` y de ejercicios.
- Carpetas técnicas y nombres de archivo en inglés cuando son infraestructura; el contenido y los slugs en español.

## 3. Anatomía de lección estándar (las 11 partes, obligatorias)

Toda sub-unidad (las ~121) se escribe con esta estructura (§E.1). El orden importa: convierte "temario" en "enseñanza".

1. **Objetivos observables (1–3)** — verbos de Bloom (`implementar`, `explicar el trade-off`, `depurar`, `diseñar`). Lo que sabrás *hacer*, no "conocer".
2. **Hook / por qué importa** — reusa el "💰" de la fase en el ROADMAP; relevancia de mercado.
3. **Activación de conocimiento previo** — retrieval de lo anterior (prerequisite-check).
4. **Ejemplo resuelto modelado (worked example)** — think-aloud: el experto razona en voz alta, no solo muestra el resultado. Para contenido genuinamente nuevo, el worked example **bate** al "resuélvelo solo" (Sweller).
5. **Non-examples + misconceptions explícitas** — "podrías pensar X; aquí por qué está mal".
6. **Práctica con andamiaje que se desvanece (faded)** — completar (Parsons/faded) → independiente. Aquí entra el Primero-Sin-IA escalado por novedad (§5).
7. **Ejercicios Primero-Sin-IA con timebox (25–45 min)** — cada uno con **solución de referencia + errores comunes** para autocorrección honesta. Los enunciados viven en `ejercicios/fase-N/<slug>/`.
8. **Check de dominio (active recall)** — quiz de bajo riesgo / "explícalo de vuelta" / predecir salida.
9. **Recursos** — documentación oficial primero; lista viva en `articulos.md` de la carpeta de ejercicios.
10. **Conexión con el proyecto** — cómo alimenta el capstone de la fase (constructive alignment).
11. **Prompt de reflexión + gancho de spaced repetition** — qué repasar y cuándo.

> **F0–F1 específicamente:** usa **PRIMM** (Predict–Run–Investigate–Modify–Make) y **Parsons problems** (reordenar líneas). Baja carga cognitiva, encaja con Primero-Sin-IA (predecir = pensar primero).

## 4. Hilos transversales (tejer, no enseñar una vez)

El curso encapsula como *hábitos diarios* lo que un roadmap encapsularía como fases. En **cada** lección revisa qué hilos tocan y téjelos en el worked example y los ejercicios — no los pospongas a una fase "de calidad":

- **Testing / TDD** — red-green-refactor como método por defecto del Primero-Sin-IA; mutation/behavior coverage, **nunca coverage %** como meta.
- **Evals de IA** — eval harness *antes* de optimizar; "los unit tests de la IA"; ship-gate de todo proyecto con LLM.
- **Seguridad** — OWASP web desde el primer endpoint; OWASP LLM Top 10 + Agentic en cada feature de IA.
- **Observabilidad** — logs estructurados + correlation IDs + trazas (OTel); para IA, traza del call-chain con tokens/latencia/costo.
- **Spec-driven + ADRs + Conventional Commits** — mini-spec al arrancar; decisiones en ADRs; `commit-msg` hook desde el commit #1.
- **Costo / latencia** — token budgeting + USD/request medido en vivo; prompt + semantic caching; ruteo de modelos.
- **Inglés técnico** — READMEs/ADRs en inglés en fases tardías; explicar arquitectura en voz alta.
- **Empleabilidad** — conectar con portafolio/entrevista cuando aplique (track-0).
- **Active recall + spaced repetition + interleaving** — el check de dominio (#8) y el gancho de repaso (#11) no son opcionales.

## 5. Escalar Primero-Sin-IA por novedad (matiz crítico)

- **Concepto nuevo:** worked example → problema de completar (faded) → Primero-Sin-IA.
- **Repaso/consolidación (o lo que el alumno ya sabe):** Primero-Sin-IA de entrada.
- **Todo** ejercicio Primero-Sin-IA trae **solución de referencia + errores comunes**. Sin esto, el floundering fija misconceptions.
- La experiencia previa del autor entra como **recuadro opcional** ("Si ya lo tocaste, valida y salta"), **nunca como prerrequisito**.

## 6. Capstones (las sub-unidades `N.P`)

Un capstone declara su **"hecho significa…"** mapeado a los objetivos de la fase + la rúbrica + el **Definition of Done único**. No uses ">80% coverage" como criterio jamás. El capstone está **terminado** solo si cumple todo lo aplicable:

1. **Spec** inicial + **ADRs** de decisiones clave.
2. **Tests verdes** + lint en CI; calidad por mutation/behavior coverage o aserciones reales.
3. **Seguridad aplicada:** OWASP web (si hay endpoint) + OWASP LLM/Agentic (si hay IA); secret + dependency scanning (SCA).
4. **Observabilidad instrumentada:** logs + correlation IDs + trazas (OTel); para IA, call-chain con tokens/latencia/costo por paso.
5. **(Si toca IA) eval harness versionado** + número + gate de regresión + budget de costo/latencia.
6. **(Si toca agente que ejecuta acciones)** validación de salida antes de ejecutar + least-privilege de tools + HITL para acciones sensibles + techo de costo.
7. **a11y mínima (WCAG 2.2)** si hay UI; estados completos (empty/loading/error/success).
8. **Demo en vivo que CORRE** + **README en inglés** + write-up público de trade-offs.
9. **Conventional Commits** en todo el historial.

## 7. CONTRATO DE LECCIÓN (template copiable)

Copia este bloque a `src/content/docs/fase-N/<slug>.md` y rellénalo. Frontmatter compatible con Astro Starlight + campos del curso.

````markdown
---
title: "<Título humano de la sub-unidad>"
description: "<1 línea — qué sabrás hacer al terminar>"
# --- metadata del curso (no romper estos nombres) ---
id: "<id-del-build-list>"          # p.ej. 6.0b
fase: "fase-N"                      # fase-0…fase-8 | track-0
slug: "<id>-<kebab-corto>"
ruta: "critica"                    # critica | opcional
objetivos:
  - "<verbo de Bloom> ..."
hilos: [testing, evals, seguridad, observabilidad, spec-driven, costo-latencia, ingles, active-recall]  # solo los que aplican
prerequisitos: ["<slug-de-leccion-previa>"]
capstone: false                    # true solo en las N.P
---

## 🎯 Objetivos
<!-- 1–3, observables, verbos de Bloom. Lo que sabrás HACER. -->

## 💰 Por qué importa
<!-- Hook: reusa el "💰" de la fase. Relevancia de mercado, 2–4 líneas. -->

## 🔁 Antes de empezar (lo que ya deberías poder hacer)
<!-- Activación de conocimiento previo / prerequisite-check. 2–3 preguntas de recuperación. -->

> [!note] Si ya lo tocaste
> <!-- Recuadro OPCIONAL para el oxidado-con-experiencia: cómo validar y saltar. Nunca prerrequisito. -->

## 🧠 Ejemplo resuelto (think-aloud)
<!-- El experto razona en voz alta: decisiones, dudas, por qué este camino y no otro. NO solo el resultado. -->

## 🚫 Errores y falsas intuiciones
<!-- Non-examples + misconceptions: "podrías pensar X; aquí por qué está mal". -->

## 🪜 Práctica guiada (andamiaje que se desvanece)
<!-- Parsons / faded → independiente. En F0–F1 usa PRIMM. -->

## ✍️ Ejercicios Primero-Sin-IA
<!-- Enunciados completos en ejercicios/fase-N/<slug>/. Cada uno con timebox 25–45 min. -->
- **E1** (timebox 30 min) — <enunciado corto>. Enunciado: `ejercicios/fase-N/<slug>/e1/`.

<details>
<summary>Solución de referencia (ábrela SOLO después de intentar)</summary>

<!-- Versión breve para autocorrección honesta + "errores comunes". La versión anotada completa vive en .ai/soluciones/ y NO se enlaza aquí. -->

</details>

## ✅ Check de dominio (active recall)
<!-- 3–5 preguntas de bajo riesgo / "explícalo de vuelta" / predecir la salida. -->

## 🔌 Hilos transversales aplicados
<!-- Cómo esta lección teje testing/evals/seguridad/observabilidad/etc. Borra los que no apliquen. -->

## 🛠️ Conexión con el capstone de la fase
<!-- Qué pieza del proyecto de la fase habilita esta sub-unidad. -->

## 🪞 Reflexión + repaso espaciado
<!-- Prompt de reflexión + qué reescribir de memoria mañana + cuándo repasar (gancho de spaced repetition). -->

## 📚 Recursos
<!-- Documentación oficial primero. Lista viva en ejercicios/fase-N/<slug>/articulos.md. -->
````

## 8. Crear los artefactos privados (.ai/)

Por cada sub-unidad con ejercicios, crea también:

- `.ai/rubricas/fase-N/<slug>.md` — **rúbrica analítica** atada a los objetivos observables. Criterios: (a) corrección, (b) calidad de ingeniería (aserciones reales, no coverage%; clean code; manejo de errores), (c) seguridad (OWASP web/LLM según aplique), (d) comprensión demostrada (el write-up calza con el código), (e) observabilidad/eval (si toca IA: eval harness + número), (f) comunicación (README/ADR claros, inglés en fases tardías). Niveles: **Novato** (no cumple objetivo) · **Competente** (cumple, calidad aceptable) · **Proficiente** (cumple + teje los hilos transversales sin que se lo pidan). Lista los **errores típicos a marcar** específicos de la sub-unidad.
- `.ai/soluciones/fase-N/<slug>/` — solución(es) de referencia **anotada(s)**: por qué cada decisión, qué trade-off, qué se evaluará. Es lo que el corrector consulta para graduar **sin** pegarla. Más completa que la del `<details>` de la lección.

> El estándar de rúbrica vive en la skill `corregir-ejercicio` y en §E.4 de CURRICULUM-REVIEW. Mantén ambos consistentes: la rúbrica que escribes aquí es exactamente la que el corrector aplicará.

## 9. Actualizar `progreso.md`

Tras crear/modificar una sub-unidad, refleja el cambio en el dashboard:

- Marca de estado: `- [ ]` pendiente · `- [~]` en progreso · `- [x]` completado.
- Una línea por sub-unidad bajo su fase, con `id`, título, marca **[ruta-crítica]/[opcional]** y enlace relativo a `src/content/docs/fase-N/<slug>.md`.
- Mantén el orden del build list (§D). Si añades una sub-unidad nueva fuera del build list, anótala como tal y avisa que toca actualizar `ROADMAP.md`/`CURRICULUM-REVIEW.md`.

## 10. Checklist de calidad (antes de declarar "hecha" una lección)

- [ ] `id`, `fase`, `slug`, `ruta` correctos y coherentes con el build list.
- [ ] Las **11 partes** de la anatomía presentes (o justificación explícita si una no aplica).
- [ ] Objetivos **observables** con verbos de Bloom (no "conocer/entender").
- [ ] Worked example es **think-aloud**, no solo resultado.
- [ ] Hay **non-examples/misconceptions** explícitas.
- [ ] Cada ejercicio Primero-Sin-IA tiene **timebox + solución de referencia + errores comunes**.
- [ ] Andamiaje **se desvanece** (faded); en F0–F1, PRIMM/Parsons.
- [ ] Hilos transversales que aplican están **tejidos** (no pospuestos).
- [ ] Si es capstone: declara "hecho significa…" mapeado al **DoD único**; nada de coverage% como meta.
- [ ] `.ai/rubricas/fase-N/<slug>.md` y `.ai/soluciones/fase-N/<slug>/` creados y consistentes con la lección.
- [ ] **Nada de `.ai/` enlazado** desde la lección pública.
- [ ] `progreso.md` actualizado.
- [ ] Español con términos técnicos en inglés; **sin voseo argentino**; sin trailer de Claude en commits.

## 11. Reglas de lenguaje y estilo

- Prosa en **español latino estándar (tuteo)** o chileno natural; términos técnicos en **inglés** (testing, embeddings, rate limiting…).
- **Prohibido el voseo argentino** y sus modismos (`podés`, `tenés`, `revisá`, `che`, `laburo`…). Usa `puedes`, `tienes`, `revisa`.
- Sin trailers de co-autoría de Claude en ningún commit. No hagas commit desde esta skill salvo que te lo pidan.
- No edites `src/` de configuración ni `package.json`: esta skill solo produce contenido `.md`, ejercicios y artefactos `.ai/`.
