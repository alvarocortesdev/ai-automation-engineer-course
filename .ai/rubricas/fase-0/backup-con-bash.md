---
ejercicio_id: fase-0/backup-con-bash
fase: fase-0
sub_unidad: "0.5"
version: 1
---

# Rúbrica — Script de respaldo robusto

> Rúbrica analítica atada a los `objetivos`. Aquí el "qué" (crear un tar.gz) es lo fácil; lo que separa
> a un script de juguete de uno profesional es el **cómo**: validación, separación stdout/stderr,
> códigos de salida y uso de una variable de entorno. Eso es lo que se evalúa.

## Objetivos evaluados
- **O1** — Script bash con shebang, `set -euo pipefail` y validación de argumentos.
- **O2** — Separar `stdout` (dato útil) de `stderr` (diagnóstico) y devolver códigos de salida honestos.
- **O3** — Usar la variable de entorno `BACKUP_DIR` para configurar sin tocar el código.

## Criterios y niveles

### C1 — Corrección (¿respalda de verdad?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No crea el `.tar.gz`, o el archivo está vacío / corrupto. |
| **en-progreso** | Crea un tar pero archiva la ruta absoluta completa, o no comprime (`.tar` sin `.gz`), o nombre sin timestamp. |
| **competente** | Crea `respaldo-<timestamp>.tar.gz` con el **contenido** del directorio; los tests verdes. |
| **excelente** | Además es idempotente en el sentido práctico (el timestamp evita colisiones) y reporta cuántos archivos respaldó. |

### C2 — Robustez: validación y exit codes · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `set -euo pipefail`; sin argumento explota con error de `tar` o devuelve 0. |
| **en-progreso** | Valida el argumento pero devuelve el código equivocado, o el mensaje de error va a `stdout`. |
| **competente** | Sin argumento → uso a `stderr` y `exit 1`; directorio inexistente → error a `stderr` y `exit 1`. |
| **excelente** | Mensajes precisos y accionables; distingue "falta argumento" de "no es directorio"; usa `exit` con códigos consistentes. |

### C3 — Higiene de streams y configuración · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Mezcla diagnóstico y dato en `stdout`; ignora `BACKUP_DIR`. |
| **en-progreso** | Respeta `BACKUP_DIR` **o** separa streams, pero no ambos. |
| **competente** | `stdout` solo trae la ruta del archivo; los mensajes informativos van a `stderr`; respeta `BACKUP_DIR` con default `.`. |
| **excelente** | `BACKUP_DIR` con `${BACKUP_DIR:-.}`, comillas en todas las variables, y el script pasa ShellCheck sin warnings. |

## Errores típicos a marcar
- **Olvidar `set -euo pipefail`:** un fallo intermedio pasa desapercibido y el respaldo "miente".
- **Variables sin comillas** (`tar -czf $destino $origen`): rutas con espacios rompen el comando.
- **Mandar la ruta a `stderr` y los logs a `stdout`** (al revés de lo correcto): rompe la composición con pipes.
- **Timestamp sin segundos:** dos respaldos en el mismo minuto se pisan.
- **Devolver `exit 0` tras un error de validación:** CI y otros scripts creerían que todo salió bien.
- **`tar -czf "$destino" "$origen"`** (sin `-C`): archiva la ruta completa en vez del contenido.

## Señales de dependencia-IA
- Script con `getopts`, `trap`, manejo de señales y opciones que el alumno **no puede explicar** (sobreingeniería impropia de F0).
- Comentarios genéricos tipo "robust error handling" sin que el código realmente lo haga.
- **Verificación sugerida:** pedir que explique línea por línea qué hace `set -u` y dé un ejemplo donde lo salve de un bug. Si lo copió, no sabrá.

## Feedback sugerido (graduado)
- **Pista (nivel 1):** "Corre tu script sin argumentos. ¿El mensaje y el código de salida son los que un humano (o CI) esperaría?"
- **Pregunta socrática (nivel 2):** "Si tu respaldo falla a la mitad, ¿cómo se enteraría quien lo corre? ¿Qué línea al inicio del script convierte un fallo silencioso en ruidoso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa los dos roles de la salida: la **ruta** del archivo a `stdout` (para encadenar), y todo lo informativo a `stderr` con `>&2`. Y empieza con `set -euo pipefail`."

## Conexión con el proyecto / capstone
- Este esqueleto (shebang + `set -euo pipefail` + validación + exit codes) es el molde del `run.sh`/`test.sh`
  del **Capstone F0 — CLI sin IA** y de toda automatización del curso (Fase 7). Es disciplina, no decoración.
