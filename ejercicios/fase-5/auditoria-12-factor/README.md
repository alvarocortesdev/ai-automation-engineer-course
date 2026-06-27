# Ejercicio 5.2 — Auditoría 12-factor de un backend

> **Modalidad: razonamiento y diagnóstico (sin IA, sin código que correr).** Saber recitar los doce factores es fácil; detectarlos rotos en código real es la habilidad que se examina. Aquí auditas un backend sembrado de violaciones y explicas el síntoma de producción de cada una.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.2` 12-factor app
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Auditar `app.py` + `Dockerfile` + `compose.yaml`, identificar cada violación de 12-factor con el **factor** que incumple, el **síntoma observable en producción** que provoca y el **arreglo** accionable, y priorizar los arreglos en un ADR corto.

## 📋 Contexto

Antes de desplegar tu capstone de la Fase 5 vas a correr esta misma auditoría sobre tu propio `Dockerfile`/`compose.yaml`. Cada violación que caces aquí es un incidente de producción (sesión perdida, secreto filtrado, log que llena el disco) que no vas a tener allá. Es, además, material directo de un ADR de despliegue.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Lee los tres archivos con la lista de los doce factores al lado.
2. Solo entonces consulta **documentación oficial** (`12factor.net`).
3. **Solo al final**, usa IA para *revisar* tu auditoría — no para generarla.
4. Mañana, reescribe de memoria las seis violaciones y su síntoma.

## 🛠️ Instrucciones

1. Lee `app.py`, `Dockerfile` y `compose.yaml` (incluye los comentarios: algunos esconden pistas, como el gap dev/prod).
2. Completa `auditoria.md`: una entrada por violación (dónde, factor + número, síntoma en producción, arreglo).
3. Hay **al menos seis** violaciones reales. Encuentra todas las que puedas.
4. Cierra con el **ADR corto** (qué arreglo priorizas) y la **defensa**.
5. No hay tests: la entrega es tu razonamiento escrito.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Identificas al menos seis violaciones con el factor correcto (sin confundir, p. ej., III con IV).
- [ ] Cada síntoma es **observable** ("al reiniciar el contenedor los usuarios pierden la sesión"), no genérico ("es mala práctica").
- [ ] Cada arreglo es accionable y correcto (no "usa Kubernetes").
- [ ] El ADR prioriza con un criterio defendible (riesgo de seguridad vs operativo).
- [ ] Respondes, sin notas, por qué el secreto horneado es lo más grave y qué factor habilita el escalado horizontal.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Recorre los factores del corazón de la lección y busca cada uno en el código: ¿hay config/secretos en el código o en la imagen (III)? ¿estado en memoria del proceso (VI)? ¿logs a un archivo (XI)? ¿puerto fijo en el código (VII)? ¿deps sin pinear (II)? ¿el mismo backing service en dev y prod, o SQLite vs Postgres (X)? Para el síntoma, imagina dos cosas: que el contenedor **reinicia** y que corres **dos réplicas**. Repasa la sección 4 de la lección.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `auditoria.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/auditoria-12-factor.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/auditoria-12-factor.md` — no la mires antes de intentarlo.
