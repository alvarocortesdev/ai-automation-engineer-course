---
ejercicio_id: fase-3/plan-migracion-zero-downtime
fase: fase-3
sub_unidad: "3.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diseña un cambio de esquema zero-downtime

## 1. Por qué la propuesta del junior bota la app

- **Causa raíz — rolling deploy.** Durante el rollout conviven instancias con código **viejo** (que hace `SELECT correo`, `INSERT ... correo`) y código **nuevo** (que usa `email`). El `alter_column` rename elimina `correo` en el instante en que corre. A partir de ahí, cada request atendido por una instancia vieja consulta una columna inexistente y devuelve **5xx**. El error no es la sintaxis del rename: es que el cambio es **incompatible con el código que todavía está corriendo**. Incluso si el rename fuera instantáneo (metadata-only), rompería igual.
- **Segunda razón — el ALTER pesado.** Sobre 10M filas, según el motor/operación, un `ALTER TABLE` puede tomar un lock que bloquea lecturas/escrituras durante la operación, congelando la tabla. (Un rename puro suele ser barato en Postgres, pero el alumno que lo nota gana puntos; el argumento de compatibilidad es el central.)

## 2. Secuencia expand/contract

| # | Tipo | Qué hace | Columna que usa el código en ejecución | Por qué es seguro |
|---|---|---|---|---|
| 1 | **migración (expand)** | `op.add_column("clientes", sa.Column("email", sa.String(255), nullable=True))` | viejo: `correo` | Agregar una columna nullable no rompe a nadie; el código viejo ni la ve. |
| 2 | **migración (backfill)** | Copiar `correo` → `email` **por lotes** | viejo: `correo` | Los datos históricos quedan en `email`; el código sigue usando `correo`. |
| 3 | **deploy (código)** | Nuevo código: **escribe en AMBAS** (`correo` y `email`) y **lee de `email`** | transición: ambas | Doble escritura: mientras conviven viejo y nuevo, todo dato nuevo llega a las dos columnas. El viejo (que aún escribe solo `correo`) no queda atrás porque... (ver paso 4). |
| 4 | **migración / job (backfill de ventana)** | Re-copiar a `email` los `correo` escritos por instancias viejas durante el rollout (o esperar a que no queden instancias viejas y hacer un backfill final de huecos) | nuevo: doble escritura | Cierra la ventana en que el código viejo pudo escribir solo `correo`. |
| 5 | **deploy (código)** | Nuevo código: deja de tocar `correo`, usa solo `email` | nuevo: `email` | Ya ninguna instancia depende de `correo`. |
| 6 | **migración (contract)** | `op.drop_column("clientes", "correo")` | nuevo: `email` | Nadie usa `correo`; borrarla no rompe nada. **Paso destructivo y NO reversible** → backup antes. |

> El corazón del patrón: **nunca se elimina ni renombra algo que el código en ejecución todavía usa**, y **el cambio de esquema se separa en el tiempo del cambio de código**. La columna `email` aparece *antes* de que nadie la lea; `correo` desaparece *después* de que nadie la use.

## 3. Backfill de 10M filas sin congelar la tabla

Un `UPDATE clientes SET email = correo` único toma un lock amplio, crea una transacción gigantesca (WAL inflado, presión de replicación) y puede provocar timeouts. En su lugar, **por lotes**:

```sql
-- repetido en bloques, avanzando el rango de id, con pausas entre lotes
UPDATE clientes SET email = correo
WHERE id BETWEEN :lo AND :hi AND email IS NULL;
```

Bloques de unos miles de filas, commit por lote, breve pausa, y monitorear locks/latencia. Conecta con los locks vistos en `3.3`: lotes pequeños = locks cortos = la app sigue respondiendo.

## 4. Plan de rollback paso a paso

| Paso | Cómo revierto si falla | ¿Reversible sin pérdida? |
|---|---|---|
| 1 (add `email`) | `drop_column("clientes", "email")` | Sí (columna vacía). |
| 2 (backfill) | Idempotente: re-corro; o dejo `email` y revierto el código | Sí. |
| 3 (deploy doble escritura) | Deploy de vuelta al código viejo; `email` sigue ahí, sin daño | Sí (la doble escritura garantiza que `correo` nunca quedó atrás). |
| 5 (deploy solo-`email`) | Volver al deploy con doble escritura | Sí, **mientras `correo` siga existiendo**. |
| 6 (drop `correo`) | **No reversible**: los datos de `correo` se destruyen | **No.** Requiere snapshot/backup previo; recuperación = restore. |

La clave: los pasos *expand* y los deploys son reversibles baratos; **solo el contract destruye datos**, por eso va al final, detrás de un backup, cuando ya hay máxima confianza.

## 5. Observabilidad (nivel excelente)

Durante la migración, vigilar: tasa de errores 5xx por instancia, latencia p95/p99, locks activos en Postgres (`pg_locks` / `pg_stat_activity`), y lag de replicación. Un repunte de 5xx en instancias viejas tras un paso = abortar y revertir.

## Rango de soluciones aceptables

- Un alumno puede modelar el paso 4 como "esperar a que termine el rollout (no quedan instancias viejas) y hacer un único backfill final de huecos" en vez de un job continuo: **válido**, mientras cierre la ventana de la doble escritura.
- Puede usar un **trigger** de base de datos para mantener `email` sincronizada en lugar de doble escritura en el código: **válido y robusto**, nivel excelente si lo justifica (y nota que el trigger también hay que retirarlo).
- El número exacto de pasos puede variar (5–7) según cómo agrupe deploys y backfills; lo que **no** puede faltar: expand antes de leer, doble escritura durante la transición, contract al final con backup, backfill por lotes.
- **Variante de control para detectar dependencia-IA:** pedir que explique, sin el plan a la vista, qué cliente concreto pierde su email y en qué instante si se omite la doble escritura. Quien entendió describe la ventana de rollout; quien copió el patrón se traba.
