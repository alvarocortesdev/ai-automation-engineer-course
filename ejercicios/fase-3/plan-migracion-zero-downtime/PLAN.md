# Plan de migración zero-downtime: `clientes.correo` → `clientes.email`

> Completa cada sección con tu razonamiento. Borra estas citas guía al terminar.
> Escríbelo como si fuera el plan que pegarías en el PR para que el equipo lo revise.

## 1. Por qué la propuesta del junior bota la app

> Al menos dos razones concretas y distintas. Una debe ser sobre el rolling deploy.

- Razón 1 (rolling deploy):
- Razón 2 (tabla de 10M filas / locks):

## 2. Secuencia expand/contract

> Numera cada paso. Marca si es **migración** (cambio de esquema/datos) o **deploy** (cambio de código).
> En cada paso, di qué columna usa el código que está corriendo y por qué es compatible hacia atrás.

| # | Tipo (migración / deploy) | Qué hace | Columna que usa el código en ejecución | ¿Por qué es seguro? |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |

## 3. Backfill de 10M filas sin congelar la tabla

> ¿Por qué un `UPDATE` único es mala idea? ¿Qué haces en su lugar?

## 4. Plan de rollback paso a paso

> Si falla a mitad, ¿qué haces en cada paso? ¿Cuál paso NO es reversible y cómo te proteges?

| Paso | Cómo revierto si falla | ¿Reversible sin pérdida? |
|---|---|---|
| 1 |  |  |
| ... |  |  |

## 5. (Opcional) Observabilidad

> ¿Qué mirarías durante la migración para saber que va bien (locks, errores 5xx, latencia)?
