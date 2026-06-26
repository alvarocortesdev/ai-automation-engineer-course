---
ejercicio_id: fase-0/pipeline-conteo-logs
fase: fase-0
sub_unidad: "0.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` e `INSTRUCCIONES-CORRECTOR.md`).

# Solución de referencia — Top 3 de IPs en un log

## Solución canónica (`resolver.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

log="${1:?Uso: resolver.sh <archivo.log>}"

awk '{ print $1 }' "$log" \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -3 \
  | awk '{ print $1, $2 }'
```

## Salida esperada (con el fixture `acceso.log`)

```text
5 192.168.1.10
3 10.0.0.5
2 203.0.113.7
```

## Razonamiento paso a paso

1. `awk '{ print $1 }' "$log"` — aísla la primera columna (la IP) de cada línea.
2. `sort` — junta las IPs iguales en líneas adyacentes (requisito de `uniq`).
3. `uniq -c` — colapsa los grupos y antepone el conteo: `   5 192.168.1.10`.
4. `sort -rn` — ordena **numéricamente** (`-n`) y al revés (`-r`): mayor conteo primero.
5. `head -3` — toma las 3 primeras.
6. `awk '{ print $1, $2 }'` — normaliza el formato a `CONTEO IP` sin los espacios de relleno de `uniq -c`.

El `"${1:?...}"` hace que, sin argumento, bash imprima el mensaje a `stderr` y salga con código != 0,
cumpliendo el criterio de robustez sin un `if` explícito (aunque un `if` también es válido y más legible
para un principiante).

## Variantes aceptables
- Validar el argumento con un `if [[ -z "${1:-}" ]]; then echo "Uso: ..." >&2; exit 1; fi` en vez de `${1:?}`.
- Omitir el `awk` final si el corrector acepta la salida de `uniq -c` con espacios de relleno — **pero**
  los tests comparan contra `CONTEO IP` normalizado, así que sin esa normalización los tests fallan. La
  solución de referencia la incluye a propósito.
- Usar `awk '{c[$1]++} END{for (k in c) print c[k], k}' "$log" | sort -rn | head -3` (conteo con array
  asociativo). Es correcto y más eficiente (un solo paso), pero **por encima del nivel F0**: si el alumno
  lo entrega, pedirle que lo explique antes de calificarlo `excelente`.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`sort` antes de `uniq`.** Sin él, los conteos salen partidos. Error #1.
2. **`sort -rn` y no `sort -r`.** Con `-r` solo, `9` ordena después de `42` (comparación textual).
3. **Comillas en `"$log"`.** Una ruta con espacios sin comillas rompe el pipeline.
4. **`stdout` limpio.** El dato a `stdout`; cualquier diagnóstico a `stderr`.
