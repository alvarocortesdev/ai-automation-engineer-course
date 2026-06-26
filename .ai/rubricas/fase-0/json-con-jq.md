---
ejercicio_id: fase-0/json-con-jq
fase: fase-0
sub_unidad: "0.5"
version: 1
---

# Rúbrica — Consulta JSON con jq

> Rúbrica analítica atada a los `objetivos`. Lo central es que el alumno componga un filtro `jq`
> entendiendo cada pieza (`select`, `and`, `sort_by`, `-r`), no que adivine un comando que pase los tests.

## Objetivos evaluados
- **O1** — Filtrar y transformar JSON con jq usando `select`, `and` y `sort_by`.
- **O2** — Producir salida en crudo (`jq -r`) apta para encadenar en un pipeline.

> Salida correcta para `usuarios.json`: `Ana` y `Carla` (en ese orden). Eva (5 logins) queda fuera por
> el `>` estricto: es el caso borde que revela si el alumno entendió "más de 5" vs "5 o más".

## Criterios y niveles

### C1 — Corrección del filtro · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No filtra (imprime todos), o el filtro es sintácticamente inválido (jq error). |
| **en-progreso** | Filtra por una sola condición (solo activos, o solo logins) — incluye a Eva o a Diego/Beto. |
| **competente** | Imprime exactamente `Ana` y `Carla`, ordenados alfabéticamente. |
| **excelente** | Maneja correctamente el borde (`> 5` estricto excluye a Eva) y puede explicar por qué. |

### C2 — Salida en crudo y componibilidad · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Imprime los objetos completos o JSON con comillas (`"Ana"`), no nombres en crudo. |
| **en-progreso** | Extrae los nombres pero deja comillas (olvidó `-r`) o los devuelve como un array JSON. |
| **competente** | `jq -r` produce un nombre por línea, sin comillas, listo para encadenar. |
| **excelente** | Demuestra que entiende la composición (p. ej. sabe que `curl ... \| ./consulta.sh /dev/stdin` funcionaría). |

## Errores típicos a marcar
- **Olvidar `-r`:** la salida sale entre comillas (`"Ana"`), inútil para encadenar con otros comandos.
- **Una sola condición:** filtrar por `.activo` pero no por `.logins` (o viceversa) → incluye a quien no debe.
- **`>=` en vez de `>`:** "más de 5" es estricto; con `>=` se cuela Eva (5 logins).
- **No ordenar:** salida correcta en contenido pero en orden de aparición, no alfabético.
- **Iterar mal:** usar `.nombre` sin recorrer la lista, o `.[]` sin extraer el campo.

## Señales de dependencia-IA
- Filtro `jq` con construcciones avanzadas (`reduce`, `to_entries`, `@csv`) que el alumno no sabe explicar.
- No distingue por qué Eva queda fuera (señal de que no razonó el borde, solo copió).
- **Verificación sugerida:** pedir que modifique el filtro para incluir también a quienes tengan **exactamente** 5 logins. Si entendió, cambia `>` por `>=` sin dudar.

## Feedback sugerido (graduado)
- **Pista (nivel 1):** "Tu salida trae comillas. ¿Qué bandera de jq devuelve strings 'en crudo'?"
- **Pregunta socrática (nivel 2):** "¿Cuántas condiciones tiene que cumplir un usuario para aparecer? ¿Tu `select` las exige todas a la vez?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Combina las dos condiciones dentro de un solo `select(... and ...)`, ordena con `sort_by(.nombre)` y extrae con `.[].nombre`. Usa `-r` para la salida cruda."

## Conexión con el proyecto / capstone
- Recortar JSON con `jq` es la base de consumir cualquier API o respuesta de LLM (Fases 3 y 6). El reflejo
  `curl ... | jq ...` aparece en casi todos los capstones; aquí lo entrenas sin red.
