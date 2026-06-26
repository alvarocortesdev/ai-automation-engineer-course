# Ejercicio 0.6 — Construye el hook commit-msg (Conventional Commits)

> **Modalidad: código.** Implementas un hook real de Git que valida que cada mensaje de commit siga [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Es el primer hilo de *spec-driven development* del curso, forzado por una máquina y no por tu disciplina. Y lo construyes con **tests primero**: la suite ya define el contrato, tú lo haces pasar.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.6` Git y GitHub a fondo
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar un script `commit-msg` que **acepte** (exit `0`) mensajes válidos de Conventional Commits y **rechace** (exit ≠ `0`) los inválidos, dejando pasar los commits autogenerados de `Merge`/`Revert` y mostrando ayuda útil a `stderr`.

## 📋 Contexto

Git ejecuta el hook `commit-msg` justo después de que escribes el mensaje y le pasa **la ruta del archivo con el mensaje** como primer argumento (`$1`). Si el script sale con código distinto de `0`, **Git aborta el commit**. Aquí lo usamos para imponer un formato de mensaje. En el capstone de la fase, este hook vigilará todo tu historial.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox 45 min). Está bien que la regex te cueste.
2. Solo entonces consulta la [spec de Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) y `man grep` (sección de ERE).
3. **Solo al final**, usa IA para *revisar y explicar* tu regex — no para *generarla*.
4. Mañana, reescribe el hook de memoria. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `commit-msg` (es un script Bash con un esqueleto). La extracción de la cabecera ya está hecha; tú implementas la **validación** donde dicen los `TODO`.
2. Corre los tests, que definen el comportamiento esperado:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos pasen en verde**. Los tests invocan tu script con mensajes válidos e inválidos y verifican el código de salida.
4. Añade **un caso de prueba tuyo** en `tests/test_hook.py` (un mensaje borde: ¿qué pasa con un scope con guion? ¿con una descripción de 100 caracteres? ¿con un breaking change `feat(api)!:`?).
5. **Pruébalo de verdad** en un repo: copia `commit-msg` a `.githooks/`, hazlo ejecutable y enlázalo:

   ```bash
   mkdir -p .githooks && cp commit-msg .githooks/ && chmod +x .githooks/commit-msg
   git config core.hooksPath .githooks
   git commit -m "esto deberia fallar"        # ← el hook lo rechaza
   git commit -m "test: el hook funciona"     # ← lo acepta
   ```

## Contrato (lo que los tests verifican)

**Se aceptan** (exit `0`):

```text
feat: agrega comando de exportación
fix(parser): corrige off-by-one en el índice
docs: actualiza el README de instalación
refactor!: renombra el módulo de almacenamiento
chore(deps): sube pytest a 8.x
Merge branch 'feature'           # autogenerado por Git
```

**Se rechazan** (exit ≠ `0`):

```text
arregla el bug del login         # sin type
Feature: agrega algo             # type mal escrito / con mayúscula
feat agrega algo                 # faltan los dos puntos
feat:                            # sin descripción
actualizado                      # ni type ni ":"
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests de `tests/test_hook.py` pasan.
- [ ] Los mensajes válidos del contrato salen con `0`; los inválidos, con ≠ `0`.
- [ ] Los commits `Merge`/`Revert` autogenerados **no** se bloquean.
- [ ] Al rechazar, el hook imprime ayuda **a stderr** (no a stdout).
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar tu regex pieza por pieza, **sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`grep -E` usa expresiones regulares **extendidas** (ERE), donde los paréntesis de grupo son especiales y un paréntesis **literal** se escribe `\(`. Tu patrón, anclado con `^…$`, necesita: una alternancia de tipos `(feat|fix|...)`, un grupo **opcional** para el scope `(\(...\))?`, un `!` opcional `(!)?`, y luego `: ` seguido de al menos un carácter `.+`. Antes de validar el formato, deja pasar (exit `0`) cualquier cabecera que empiece con `Merge ` o `Revert `. No mires la solución de referencia hasta cerrar tu intento.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu solución (esta carpeta), la **rúbrica** (`.ai/rubricas/fase-0/commit-msg-hook.md`) y `.ai/INSTRUCCIONES-CORRECTOR.md`. La **solución de referencia** vive en `.ai/soluciones/fase-0/commit-msg-hook.md` — no la mires antes de intentarlo de verdad.
