# Ejercicio 3.4 — Diseña un cambio de esquema zero-downtime

> **Modalidad: diseño (a mano primero, sin IA).** No se evalúa código que compile, sino tu **plan**:
> que entiendas por qué un cambio "obvio" bota la app y sepas partirlo en pasos seguros. Es
> exactamente lo que te preguntan en una entrevista de backend senior: "¿cómo migras esto sin downtime?".

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.4` Migraciones de esquema
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Diseñar la secuencia **expand/contract** para renombrar una columna en una tabla enorme de una API en
producción **sin downtime**, justificando por qué la versión ingenua falla y cómo se revierte cada paso.

## 📋 Contexto (el caso, tal como te llega)

> Tienes una API en producción con **rolling deploys**: hay varias instancias y, durante el rollout de
> una versión nueva, el código **viejo** y el **nuevo** corren **al mismo tiempo** unos minutos. La tabla
> `clientes` tiene **10 millones de filas** y una columna `correo`. El negocio pide renombrarla a `email`.
>
> Un compañero junior abrió este PR: una sola migración con
> `op.alter_column("clientes", "correo", new_column_name="email")`, **junto** con el código nuevo que ya
> hace `SELECT email`. Le pides que pare antes de mergear, y te toca escribir el plan correcto.

## 📏 Primero-Sin-IA

1. Diséñalo **solo**, a mano (timebox 40 min). Razona el caso en papel antes de escribir el plan.
2. Solo entonces consulta documentación oficial (Alembic `alter_column`, PostgreSQL `ALTER TABLE` y locks).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar el plan*.
4. Mañana, **explícalo en voz alta** a alguien sin notas.

## 🛠️ Tu tarea

Completa `PLAN.md` (trae la estructura). Cubre, en este orden:

1. **Por qué la propuesta del junior bota la app.** Al menos **dos** razones concretas y distintas
   (piensa en el rolling deploy, y en qué hace un `ALTER` pesado sobre 10M filas).
2. **La secuencia expand/contract.** Lista cada **migración** y cada **deploy de código**, en orden.
   En cada paso indica explícitamente *qué columna usa el código que está corriendo* y por qué el paso
   es compatible hacia atrás.
3. **Backfill de 10M filas** sin congelar la tabla (¿por qué un `UPDATE` único es mala idea? ¿qué haces
   en su lugar?).
4. **Plan de rollback** en cada paso: si falla a mitad de camino, ¿qué haces? ¿Qué paso **no** es
   reversible y cómo te proteges de él?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Nombras el **rolling deploy** (viejo + nuevo conviven) como causa raíz del downtime, no solo "es riesgoso".
- [ ] Tu secuencia **nunca** elimina o renombra algo que el código en ejecución todavía usa.
- [ ] El backfill es **por lotes**, no un `UPDATE` de 10M filas en una transacción.
- [ ] El paso destructivo (borrar `correo`) ocurre **al final** y reconoces que **no es reversible** (de ahí el backup).
- [ ] Puedes **defender sin notas** por qué el esquema se migra en pasos separados del deploy de código.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa en términos de "¿qué columna lee/escribe cada versión del código mientras conviven?". El patrón
tiene tres fases: **expand** (agregas `email` y haces que el código nuevo escriba en `correo` Y `email`,
y backfilleas lo viejo), una transición (el código nuevo ya lee de `email`), y **contract** (cuando
ninguna instancia usa `correo`, recién ahí la borras). El rename de un golpe falla porque deja al código
viejo —que aún corre— consultando una columna que ya no existe. No mires la solución de referencia antes
de cerrar tu intento.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `PLAN.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/plan-migracion-zero-downtime.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/plan-migracion-zero-downtime.md` — no la
mires antes de intentarlo de verdad.
