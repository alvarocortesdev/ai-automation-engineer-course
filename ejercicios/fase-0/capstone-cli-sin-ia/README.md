# Capstone Fase 0 — CLI sin IA

> **Modalidad: capstone (mixto — código + spec/ADR/README).** Es el proyecto final de la Fase 0:
> una herramienta de línea de comandos **útil para ti**, diseñada desde una mini-spec y escrita
> **100% sin IA**. No es un ejercicio con tests que ya están escritos: aquí decides el problema,
> el diseño y cada línea. Es tu prueba de que recuperaste la autonomía de ingeniería.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.P` Capstone — CLI sin IA
**Ruta:** crítica · **Timebox:** proyecto · 6–10 h repartidas en ~1 semana

## 🎯 Objetivo

Diseñar y construir un CLI pequeño y real, **partiendo de una mini-spec** y un **ADR**, con manejo de
casos borde, **demo que corre**, **README** usable e historial de **Conventional Commits** —todo **sin
delegar el pensamiento a una IA**. Al terminar, puedes explicar cada decisión y cada línea sin notas.

## 📋 Contexto

Las siete sub-unidades de la Fase 0 fueron piezas: trazar a mano, terminal, Git, funciones que validan
su entrada. Este capstone las ensambla en una herramienta que **usarás de verdad**. El CLI es el formato
nativo del oficio de AI/Automation Engineer (scripts que mueven datos, llaman APIs, orquestan pipelines):
empezar a construirlos con disciplina ahora es el hábito que repetirás cien veces. Además, un repo con
spec + commits limpios + README es lo primero que mira un reclutador —antes que el código.

## 📏 Primero-Sin-IA (el corazón de este capstone)

1. **Piensa tú el diseño.** La spec, la estructura, la lógica y los casos borde los razonas a mano, sin IA.
2. Consulta **documentación oficial** (`argparse`, `pathlib`, Conventional Commits) cuando lo necesites.
3. **Solo al final**, si quieres, usa IA para *revisar y explicar* lo que ya construiste —nunca para *generarlo*.
4. **Mañana**, reescribe tu `SPEC.md` de memoria. Si no puedes, no internalizaste tu propio diseño.

> "100% sin IA" = no le pides a un modelo que razone por ti (diseño, estructura, código). Usar `man`,
> docs oficiales y el autocompletado básico del editor está bien. Si quitarte el chat de IA te deja en
> blanco, ese vacío es justo lo que el capstone vino a llenar.

## 🛠️ Instrucciones

Construye tu proyecto **en este orden** (la disciplina *es* el orden):

1. **Elige tu problema** (5 min). Una herramienta que **sí vas a usar esta semana**. Ideas:
   - **Bitácora de estudio:** registra sesiones (`add "tema" --min 40`) en JSON; `resumen` suma por semana.
   - **Gestor de notas / vault:** busca, lista o crea notas markdown por título o tag.
   - **Organizador de archivos:** mueve archivos a subcarpetas por extensión (con dry-run).
   - **Divisor de gastos:** registra gastos compartidos y calcula quién le debe a quién.
   - **Renombrador por lotes:** renombra según un patrón, con dry-run.
2. **Crea el repo + instala el hook.** `git init`, copia `plantillas/commit-msg` a `.githooks/`, hazlo
   ejecutable y enlázalo. Primer commit. (El hook debe vigilar **desde el commit #1**.)

   ```bash
   mkdir -p .githooks && cp plantillas/commit-msg .githooks/ && chmod +x .githooks/commit-msg
   git config core.hooksPath .githooks
   ```

3. **Escribe la `SPEC.md`** (copia `plantillas/SPEC.md`). Entradas, salidas, casos borde —**antes** de codear.
   Commit: `docs: agrega SPEC inicial`.
4. **Escribe un ADR** (copia `plantillas/ADR-0001-eleccion-de-herramienta.md` a `docs/`). Justifica tu
   decisión técnica principal. Commit: `docs: agrega ADR-0001`.
5. **Implementa el camino feliz** (puedes partir de `plantillas/cli_esqueleto.py`) y **pruébalo en la
   terminal**. Commit `feat:`.
6. **Implementa los casos borde de la spec, uno por uno.** Cada uno un commit `feat:`/`fix:`.
7. **Escribe el `README.md`** con instalación, uso y una **sesión de terminal pegada** (la demo que corre).
8. **Cierra con un write-up de trade-offs** (3–5 líneas: qué elegí, qué dejé fuera, qué fue lo más difícil).
   Va en el README o en `docs/`.

> El error #1 es empezar por el paso 5 (codear) y dejar spec/ADR/README "para después" (que no llega).
> La disciplina es hacer 3 y 4 **antes** de la primera función.

## ✅ Criterios de "hecho" (Definition of Done — Fase 0)

Este capstone se mide contra el **Definition of Done único** del curso. En la Fase 0 aplican estos puntos
(los demás se siembran ahora y se exigen en fases posteriores):

- [ ] **(DoD 1)** `SPEC.md` existe y se escribió **antes** que el código (su commit precede a la primera función).
- [ ] **(DoD 1)** Hay al menos un **ADR** que justifica una decisión técnica real (contexto / decisión / consecuencias).
- [ ] **(DoD 8)** El CLI **corre** y hace lo que el README promete (**demo pegada** que lo prueba).
- [ ] Maneja sus **casos borde**: argumento faltante, entrada inválida y un caso "vacío" → mensajes claros a
  `stderr` y **exit codes honestos** (0 en éxito, ≠0 en error).
- [ ] **(DoD 8)** El **README** permite a un desconocido instalar y usar la herramienta sin preguntarte nada.
- [ ] **(DoD 9)** Todo el historial usa **Conventional Commits** (validados por tu hook).
- [ ] **(Gate F0)** Escrito **100% sin IA** para razonar; puedes explicar **cada línea sin notas**.
- [ ] **(DoD 8)** Escribiste el **write-up de trade-offs**.

## 📂 Estructura sugerida del entregable

```text
mi-cli/                      (o esta carpeta del repo)
├── SPEC.md                  ← la mini-spec, escrita primero
├── README.md                ← qué es, instalación, uso, demo que corre
├── mi_cli.py                ← el código (un solo archivo está perfecto)
├── docs/
│   └── ADR-0001-*.md        ← tu decisión técnica justificada
└── .githooks/
    └── commit-msg           ← el hook que valida tus commits
```

## 💡 Pista (ábrela solo si te trabas)

<details>
<summary>Mostrar pista</summary>

Si te paralizas frente a la página en blanco, casi siempre saltaste la spec. Vuelve atrás: escribe en
texto plano *"el comando `X` recibe `Y` y produce `Z`; si pasa `W`, falla con mensaje `M`"*. Con 3–4 de
esas líneas ya tienes la estructura: **una función por verbo, una rama por caso borde**. Para la demo,
arranca por el camino feliz más chico posible (un comando, sin opciones) y hazlo correr **antes** de
agregar nada. Un CLI que hace una cosa bien supera a uno que intenta cinco y no arranca. Esto es una
pista del *proceso*; el diseño lo haces tú.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu proyecto completo (este directorio o tu repo), la
**rúbrica** (`.ai/rubricas/fase-0/capstone-cli-sin-ia.md`) y `.ai/INSTRUCCIONES-CORRECTOR.md`. Pídele:

> "Corrige mi capstone `ejercicios/fase-0/capstone-cli-sin-ia/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."

La **solución de referencia** (un proyecto ejemplar) vive en `.ai/soluciones/fase-0/capstone-cli-sin-ia.md`
— es material del corrector; no la mires antes de cerrar tu intento. Recuerda: en un capstone de diseño
**no hay una única respuesta correcta**; el corrector evalúa tu spec, tu disciplina y si puedes defender
tus decisiones, no si elegiste "el" proyecto.
