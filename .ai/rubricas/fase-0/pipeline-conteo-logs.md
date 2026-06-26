---
ejercicio_id: fase-0/pipeline-conteo-logs
fase: fase-0
sub_unidad: "0.5"
version: 1
---

# Rúbrica — Top 3 de IPs en un log

> Rúbrica analítica atada a los `objetivos` del contrato. Lo que se evalúa no es solo "los tests pasan",
> sino que el alumno **entienda el pipeline** y haya envuelto el script con criterio. Un alumno puede
> hacer pasar los tests con un comando copiado y seguir sin entender; la rúbrica distingue ese caso.

## Objetivos evaluados
- **O1** — Componer un pipeline (awk/sort/uniq/head) que agregue y rankee datos de texto.
- **O2** — Predecir la salida de cada etapa antes de ejecutar el todo.
- **O3** — Envolver el pipeline en un script bash que valide su argumento y use códigos de salida honestos.

> Salida correcta para `acceso.log`: `5 192.168.1.10` / `3 10.0.0.5` / `2 203.0.113.7`. (El corrector lo
> sabe; **no se lo dice al alumno** como atajo que evite construir el pipeline.)

## Criterios y niveles

### C1 — Corrección del pipeline · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El script no produce el top 3, o imprime las IPs sin contar/ordenar. |
| **en-progreso** | Cuenta pero falla en algo: `uniq -c` sin `sort` previo (conteos partidos), orden ascendente, o no recorta a 3. |
| **competente** | Imprime exactamente las 3 líneas esperadas en formato `CONTEO IP`, mayor a menor. |
| **excelente** | Además normaliza el formato (sin espacios de relleno de `uniq`), y puede explicar por qué `sort` va antes de `uniq` y por qué `sort -rn` y no `sort -r`. |

### C2 — Calidad del script (validación, errores, exit codes) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin shebang ni `set`; con un argumento ausente revienta con un error críptico o devuelve 0. |
| **en-progreso** | Funciona en el caso feliz, pero no valida el argumento o no controla el código de salida. |
| **competente** | Tiene `#!/usr/bin/env bash` + `set -euo pipefail`; sin argumento sale con código != 0 y un mensaje claro a `stderr`. |
| **excelente** | Mensaje de uso preciso, `stdout` limpio (solo el dato), y maneja con gracia un archivo inexistente o vacío. |

### C3 — Comprensión demostrada (el razonamiento calza con el código) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar qué hace cada etapa; "lo copié y funcionó". |
| **en-progreso** | Explica el todo a grandes rasgos pero no sabe qué entra/sale de una etapa concreta. |
| **competente** | Describe el flujo de datos etapa por etapa (qué recibe y qué emite cada comando). |
| **excelente** | Predice correctamente cómo cambiaría la salida si se altera una etapa (p. ej. quitar `sort`). |

## Errores típicos a marcar
- **`uniq -c` sin `sort` previo:** cuenta solo repeticiones adyacentes → conteos partidos. Es el error #1.
- **`sort -r` en vez de `sort -rn`:** ordena el conteo como **texto**, no como número (`9` antes que `42`).
- **No recortar a 3** (`head -3`) o recortar antes de ordenar por conteo.
- **`cat acceso.log | awk ...`:** "uso inútil de cat"; `awk` ya lee el archivo. Funciona pero delata nivel.
- **No validar el argumento:** sin `$1` el script debería fallar limpio, no con un error de `awk`.
- **Variable sin comillas** (`$1` en vez de `"$1"`): rutas con espacios lo rompen (hilo de seguridad/robustez).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Pipeline impecable pero **no puede explicar** por qué `sort` precede a `uniq` (lo pegó sin entender).
- Sofisticación impropia del nivel F0 (p. ej. un `awk` que cuenta con arrays asociativos) que el alumno no defiende.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga la salida de `awk '{print $1}' acceso.log | uniq -c` (sin el `sort`). Si trazó de verdad, anticipa los conteos partidos; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el pipeline completo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu conteo no cuadra con lo que ves en el log. ¿Qué necesita `uniq` para contar bien?"
- **Pregunta socrática (nivel 2):** "¿Las IPs iguales están juntas o repartidas en el archivo? ¿Cómo afecta eso a `uniq`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es: `uniq` solo colapsa líneas **adyacentes**. Inserta un `sort` antes de `uniq -c` y vuelve a predecir la salida antes de correr."

## Conexión con el proyecto / capstone
- Procesar texto con pipelines es el músculo que tu CLI del **Capstone F0** consumirá y producirá:
  una herramienta que escribe a `stdout` líneas limpias se vuelve componible con `sort`, `grep` y `jq`.
