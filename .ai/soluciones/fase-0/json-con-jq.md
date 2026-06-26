---
ejercicio_id: fase-0/json-con-jq
fase: fase-0
sub_unidad: "0.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` e `INSTRUCCIONES-CORRECTOR.md`).

# Solución de referencia — Consulta JSON con jq

## Solución canónica (`consulta.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

archivo="${1:?Uso: consulta.sh <archivo.json>}"

jq -r '
  map(select(.activo and .logins > 5))
  | sort_by(.nombre)
  | .[].nombre
' "$archivo"
```

## Salida esperada (con el fixture `usuarios.json`)

```text
Ana
Carla
```

## Razonamiento paso a paso

1. `map(select(.activo and .logins > 5))` — recorre la lista y conserva solo los elementos que cumplen
   **ambas** condiciones a la vez: estar activo **y** tener más de 5 logins.
2. `sort_by(.nombre)` — ordena los objetos resultantes alfabéticamente por nombre.
3. `.[].nombre` — recorre la lista filtrada y extrae el campo `nombre` de cada objeto.
4. `jq -r` — modo *raw*: imprime los strings sin comillas, uno por línea, listo para encadenar.

Quién entra y quién no, con el fixture:
- **Ana** (activa, 42) ✓ · **Carla** (activa, 17) ✓
- **Beto** (inactiva) ✗ · **Diego** (activo, 0 logins) ✗
- **Eva** (activa, **5** logins) ✗ — borde clave: `> 5` es estricto, 5 no es "más de 5".

## Variantes aceptables
- `.[] | select(.activo and .logins > 5) | .nombre` antes de ordenar — equivalente si se ordena después
  (p. ej. canalizando a `sort` del shell). Aceptable mientras la salida final sea `Ana`/`Carla` en orden.
- Validar el argumento con un `if` explícito en vez de `${1:?}`.
- En producción el JSON vendría de `curl`: `curl -s URL | ./consulta.sh /dev/stdin`. Mencionarlo cuenta a favor.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`-r`.** Sin él la salida sale con comillas (`"Ana"`), inservible para encadenar. Error frecuente.
2. **Las dos condiciones juntas** dentro de un solo `select(... and ...)`. Filtrar por una sola incluye a quien no debe.
3. **`>` estricto.** Con `>=` se cuela Eva. Es la prueba de que entendió "más de 5".
4. **Ordenar.** `sort_by(.nombre)` (o `sort` del shell después): sin esto, el orden es el de aparición.
