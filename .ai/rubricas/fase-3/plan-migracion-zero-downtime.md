---
ejercicio_id: fase-3/plan-migracion-zero-downtime
fase: fase-3
sub_unidad: "3.4"
version: 1
---

# Rúbrica — Diseña un cambio de esquema zero-downtime

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es un ejercicio de **diseño**: no hay
> tests. Lo que se evalúa es el **razonamiento** — que el plan sea correcto y, sobre todo, **defendible**.
> Un plan que llega al patrón correcto pero no sabe explicar por qué el rolling deploy lo obliga no es
> "competente": es una receta copiada.

## Objetivos evaluados
- **O1** — Explicar por qué el rename de un golpe causa downtime bajo rolling deploy.
- **O2** — Diseñar la secuencia expand/contract con pasos compatibles hacia atrás.
- **O3** — Planificar backfill por lotes y rollback seguro, identificando lo no reversible.

## Criterios y niveles

### C1 — Diagnóstico de la causa raíz (¿por qué falla lo ingenuo?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Dice "es arriesgado" o "puede fallar" sin mecanismo; o cree que el problema es solo la sintaxis del rename. |
| **en-progreso** | Identifica una causa (p. ej. el lock sobre 10M filas) pero **no** el problema del rolling deploy. |
| **competente** | Nombra explícitamente que durante el rollout conviven código viejo y nuevo: el viejo consulta `correo` (que el rename eliminó) y tira 5xx → downtime. Añade una segunda razón (lock/tiempo del ALTER pesado). |
| **excelente** | Distingue el rename "metadata-only" (rápido en algunos motores) del problema real, que es de **compatibilidad de código**, no de velocidad del DDL; menciona que incluso un ALTER instantáneo rompería al código viejo. |

### C2 — Diseño de la secuencia expand/contract · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No separa esquema de código; o borra/renombra `correo` antes de retirar el código que la usa. |
| **en-progreso** | Llega a "agrego `email` y después borro `correo`" pero se salta la fase de **doble escritura** (el código nuevo debe escribir en ambas mientras conviven) o el orden de deploys queda ambiguo. |
| **competente** | Secuencia ordenada: (1) migración expand agrega `email` nullable, (2) backfill, (3) deploy de código que escribe en `correo` Y `email` y lee de `email`, (4) deploy que deja de usar `correo`, (5) migración contract borra `correo`. Cada paso es compatible con el código en ejecución. |
| **excelente** | Justifica la doble escritura (las filas que entran *durante* la transición por código viejo deben replicarse a `email`), ubica un segundo backfill de "lo que entró durante la ventana" si hace falta, y separa claramente "migrar esquema" de "deployar código" en el tiempo. |

### C3 — Backfill por lotes y costo/latencia · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Propone un `UPDATE clientes SET email = correo` único, o no menciona el backfill. |
| **en-progreso** | Sabe que el UPDATE único es malo pero no propone una alternativa concreta. |
| **competente** | Backfill por lotes (`WHERE id BETWEEN ...` en bloques de unos miles, con commits/pausas) para no tomar un lock largo ni inflar el WAL; lo conecta con los locks de 3.3. |
| **excelente** | Cuantifica el riesgo (lock de tabla, transacción gigante, replicación) y propone monitorear locks/latencia mientras corre (observabilidad). |

### C4 — Rollback y lo irreversible · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay plan de rollback, o asume que todo se puede deshacer. |
| **en-progreso** | Da rollback genérico ("vuelvo a la versión anterior") sin distinguir pasos. |
| **competente** | Para cada paso dice cómo revierte; identifica que **borrar `correo` (contract) no es reversible** sin backup y por eso va al final y con respaldo. |
| **excelente** | Nota que los pasos *expand* son reversibles baratos (drop de `email`), que la doble escritura permite revertir el deploy de código sin perder datos, y que el contract exige snapshot/backup previo. |

## Errores típicos a marcar
- **Olvidar que viejo y nuevo conviven** en el rollout: es la causa raíz; sin esto el plan no tiene sentido.
- **Borrar/renombrar `correo` antes** de retirar el código que la usa → reintroduce el downtime.
- **Saltarse la doble escritura**: los datos escritos por código viejo durante la transición se perderían en `email`.
- **`UPDATE` único de 10M filas**: lock largo, transacción gigante, riesgo de timeouts.
- **Creer que el rename es "reversible"** trivialmente: el contract destruye datos; necesita backup.
- (transversales) plan correcto pero indefendible; no separa "migrar esquema" de "deployar código" en el tiempo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Plan que recita "expand/contract" con vocabulario impecable pero no puede explicar **por qué** la doble escritura es necesaria, ni qué fila concreta se perdería sin ella.
- Pasos en orden correcto pero sin atar cada uno a "qué columna usa el código corriendo" (el corazón del razonamiento).
- **Verificación sugerida:** pregunta "si saltas la fase de doble escritura, ¿qué cliente concreto pierde su email y en qué momento exacto?". Quien diseñó entendiendo describe la ventana; quien copió se traba.

## Feedback sugerido (graduado)
> Nunca dar el plan completo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Durante el deploy, ¿una sola versión del código está corriendo, o dos a la vez? Si son dos, ¿qué columna espera cada una?"
- **Pregunta socrática (nivel 2):** "Si agregas `email` y haces que el código nuevo lea de ahí, pero un request lo atiende todavía una instancia vieja que escribe en `correo`, ¿dónde queda ese dato? ¿Cómo te aseguras de que también llegue a `email`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es: expand (agregar `email` + backfill) → deploy con **doble escritura** y lectura de `email` → cuando ninguna instancia vieja queda viva, deploy que deja de tocar `correo` → contract (borrar `correo`, con backup). El borrado siempre al final."

## Conexión con el proyecto / capstone
- El **Capstone F3 — API de producción** declara en su Definition of Done "demo que CORRE" y operabilidad. Cuando el capstone evolucione su esquema, este plan es el que evita el downtime; saber diseñarlo es lo que separa una API "de portafolio" de una operable por un equipo.
