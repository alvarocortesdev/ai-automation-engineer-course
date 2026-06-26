---
ejercicio_id: fase-0/backup-con-bash
fase: fase-0
sub_unidad: "0.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` e `INSTRUCCIONES-CORRECTOR.md`).

# Solución de referencia — Script de respaldo robusto

## Solución canónica (`backup.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

origen="${1:-}"
if [[ -z "$origen" ]]; then
  echo "Error: falta el directorio a respaldar." >&2
  echo "Uso: backup.sh <directorio>" >&2
  exit 1
fi
if [[ ! -d "$origen" ]]; then
  echo "Error: '$origen' no es un directorio." >&2
  exit 1
fi

destino_dir="${BACKUP_DIR:-.}"
sello="$(date +%Y%m%d-%H%M%S)"
destino="$destino_dir/respaldo-$sello.tar.gz"

# -C "$origen" . archiva el CONTENIDO del directorio, no su ruta absoluta.
tar -czf "$destino" -C "$origen" .

n="$(find "$origen" -type f | wc -l | tr -d ' ')"
echo "Respaldo creado: $destino ($n archivos)" >&2  # diagnóstico -> stderr
echo "$destino"                                      # dato útil -> stdout
```

## Razonamiento paso a paso

1. `set -euo pipefail` — aborta ante fallos, variables no definidas o fallos en cualquier etapa de un pipe.
2. Validación: argumento ausente (`-z`) y "no es un directorio" (`! -d`) → mensaje a `stderr` y `exit 1`.
   Son **dos** errores distintos con mensajes distintos (eso es lo que sube de `competente` a `excelente`).
3. `destino_dir="${BACKUP_DIR:-.}"` — usa la variable de entorno si existe; si no, la carpeta actual.
4. `date +%Y%m%d-%H%M%S` — timestamp con segundos, evita colisiones entre respaldos cercanos.
5. `tar -czf "$destino" -C "$origen" .` — `-c` crea, `-z` comprime gzip, `-f` nombra el archivo;
   `-C "$origen" .` entra al directorio y archiva su contenido (no la ruta completa).
6. Separación de streams: la **ruta** del archivo va a `stdout` (para encadenar/capturar); el resumen
   informativo va a `stderr`. Por eso los tests capturan `stdout` para obtener la ruta limpia.

## Variantes aceptables
- Reportar o no el número de archivos (`find ... | wc -l`) es opcional; cuenta como `excelente`, no obligatorio.
- Usar `$(date +%s)` (epoch) en vez del formato legible — válido, mientras el nombre sea único y termine en `.tar.gz`.
- Un único `if` combinado con `elif` para los dos casos de error, en vez de dos `if` separados.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Comillas en TODAS las variables** (`"$origen"`, `"$destino"`). Sin ellas, rutas con espacios rompen `tar`.
2. **`-C "$origen" .`** vs `tar -czf "$destino" "$origen"`: lo segundo archiva la ruta completa (a veces
   absoluta), no el contenido. Los tests verifican que `a.txt`/`b.txt` estén dentro, así que ambos pasarían
   ese check — pero el `-C` es la forma correcta y la que evita sorpresas al restaurar.
3. **Diagnóstico en `stdout`** (en vez de `stderr`): ensucia la ruta y rompe la composición. Marcar.
4. **Olvidar `set -euo pipefail`:** el respaldo puede "tener éxito" con un tar incompleto.
