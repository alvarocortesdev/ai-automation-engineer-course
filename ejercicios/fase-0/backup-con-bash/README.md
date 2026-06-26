# Ejercicio 0.5 — Script de respaldo robusto

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.5` Terminal y Linux
**Ruta:** crítica · **Modalidad:** código (script bash) · **Timebox:** 40 min

## 🎯 Objetivo

Escribir un script bash **robusto** que automatice un respaldo: argumentos validados,
variable de entorno para configurar, separación de `stdout`/`stderr` y códigos de salida honestos.
Al terminar sabrás la diferencia entre "pegué tres comandos" y "escribí una herramienta".

## 📋 Contexto

Automatizar lo aburrido y repetible es la mitad del trabajo de un Automation Engineer. Un respaldo es
el "hola mundo" de la automatización seria: si tu script miente (dice que respaldó pero archivó una
carpeta vacía), es peor que no tenerlo. Aquí practicas el esqueleto (`set -euo pipefail`, validación,
exit codes) que reusarás en cada script del curso.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox.
2. Solo entonces consulta **documentación oficial** (`man tar`, `man date`, `man bash` sección de tests `[[ ]]`).
3. **Solo al final**, usa IA para que te *revise* — no para que lo *genere*. Pasa tu script por
   [ShellCheck](https://www.shellcheck.net/) antes de pedir corrección.
4. Mañana, **reescríbelo de memoria**.

## 🛠️ Instrucciones

Completa `backup.sh <directorio>` para que:

1. Empiece con `#!/usr/bin/env bash` y `set -euo pipefail`.
2. Cree un archivo `.tar.gz` con el **contenido** del directorio recibido, nombrado con timestamp
   (ej. `respaldo-20260625-103000.tar.gz`).
3. Lo deje dentro de la carpeta que indique la variable de entorno `BACKUP_DIR`
   (por defecto, la carpeta actual `.`).
4. Escriba **solo la ruta del archivo creado** en `stdout`; cualquier mensaje informativo va a `stderr`.
5. Maneje errores: sin argumento → uso a `stderr` y `exit 1`; directorio inexistente → error a `stderr` y `exit 1`.

Pruébalo y corre los tests:

```bash
BACKUP_DIR=/tmp bash backup.sh ./alguna-carpeta
uv run pytest        # o:  pytest
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Shebang + `set -euo pipefail` presentes.
- [ ] Sin argumento → mensaje de uso a `stderr` y `exit 1`. Directorio inexistente → `exit 1`.
- [ ] En éxito: crea el `.tar.gz` y escribe **solo su ruta** en `stdout`.
- [ ] Respeta `BACKUP_DIR` si está definida; usa `.` si no.
- [ ] Puedes **explicar sin notas** por qué los diagnósticos van a `stderr` y no a `stdout`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para archivar el **contenido** del directorio (sin arrastrar toda la ruta absoluta), usa
`tar -czf "$destino" -C "$origen" .`. El timestamp sale de `date +%Y%m%d-%H%M%S`. La carpeta de
destino con valor por defecto: `destino_dir="${BACKUP_DIR:-.}"`. Para validar el argumento:
`[[ -z "$1" ]]` (vacío) y `[[ -d "$origen" ]]` (es directorio). Recuerda: lo informativo con
`echo "..." >&2`, y la ruta limpia con un `echo "$destino"` final.

</details>

## 🤖 Cómo pedir la corrección

Entrega a tu IA: tu solución (este directorio), la **rúbrica**
`.ai/rubricas/fase-0/backup-con-bash.md` y `.ai/INSTRUCCIONES-CORRECTOR.md`. La **solución de
referencia** (`.ai/soluciones/fase-0/backup-con-bash.md`) no se mira antes de intentarlo de verdad.
