# Ejercicio 5.9 — Plan de despliegue de la app completa (decisión + trade-offs)

> **Modalidad: a mano (razonamiento/diseño, sin IA).** No despliegas nada: **decides** dónde
> vive cada pieza y **justificas** el porqué. El valor está en el criterio, no en ejecutar comandos.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.9` Despliegue
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Asignar cada pieza de la app (frontend, backend, base de datos) a una opción de despliegue (**Vercel / VPS+proxy / homelab+túnel / managed cloud**) y **justificar el trade-off** de cada elección.
- **O2** — Determinar la **fuente del certificado HTTPS** correcta por pieza (plataforma / Caddy+Let's Encrypt / edge de Cloudflare).
- **O3** — Diseñar las **variables por ambiente** (dev/staging/prod) distinguiendo **público** de **secreto**, y argumentar por restricciones por qué **no** necesitas Kubernetes.

## 📋 Contexto

Es el boceto de producción de tu capstone de la fase (app desplegada con dominio y ≥3 usuarios
reales). Tomar estas decisiones **antes** de escribir un Dockerfile es lo que separa al ingeniero
que dimensiona del que copia un tutorial de Kubernetes.

## 📏 Primero-Sin-IA (en este orden, timebox 40 min)

1. Decídelo **solo**, a mano, razonando cada elección por sus **restricciones** (tipo de app, exposición, costo, control).
2. Solo entonces, consulta la **documentación oficial** (sección 9 de la lección) para validar detalles.
3. **Solo al final**, usa IA para *revisar* tu plan —no para generarlo.
4. Mañana, reescribe de memoria el árbol de decisión. Si no sale, vuelve a la lección.

## El escenario (restricciones reales)

- **Frontend:** Next.js (capstone F4).
- **Backend:** FastAPI + PostgreSQL (capstone F3).
- **Usuarios:** ≥3 reales (tu pareja y dos amigos).
- **Presupuesto:** ~USD 0–10/mes.
- **Infra "gratis" disponible:** un servidor en tu casa **detrás de CGNAT (sin IP pública fija)**.
- Un compañero insiste: *"despliega todo con Kubernetes para que sea profesional"*.

## 🛠️ Qué entregar (deja estos archivos en esta carpeta)

1. **`plan.md`** — tabla: cada pieza (frontend, backend, base de datos) → opción de despliegue → **justificación en una frase** + **trade-off descartado**.
2. **`https.md`** — para cada pieza pública: **cómo obtiene HTTPS** y por qué esa estrategia en ese caso (incluye el caso del homelab por túnel: ¿dónde se termina el TLS?).
3. **`entornos.md`** — tabla de variables por ambiente (dev/staging/prod) con al menos `NEXT_PUBLIC_API_URL`, `DATABASE_URL` y una API key; marca **público vs. secreto** y **dónde vive** cada una; una línea explicando por qué `NEXT_PUBLIC_` no puede llevar un secreto.
4. **`no-kubernetes.md`** — un párrafo (respuesta de entrevista): qué resuelve k8s, qué restricciones lo justificarían, por qué tu caso no las tiene.

Acompaña las decisiones grandes con un **ADR de una línea** (decisión + alternativa descartada + por qué).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 4 archivos existen.
- [ ] `plan.md` cubre las 3 piezas con opción + justificación + trade-off descartado.
- [ ] `https.md` acierta la **fuente del certificado** por pieza (incluido que el túnel termina TLS en el edge).
- [ ] `entornos.md` clasifica bien público vs. secreto y explica el peligro de `NEXT_PUBLIC_`.
- [ ] `no-kubernetes.md` argumenta por **restricciones**, no por "es difícil".
- [ ] Puedes **defender cada elección sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por la restricción que más manda en cada pieza. Frontend: ¿hay una plataforma hecha para
ese framework? Backend: ¿tengo IP pública (VPS) o no (homelab/CGNAT)? La respuesta a "¿IP pública?"
decide entre **reverse proxy con TLS propio** y **túnel con TLS en el edge**. Para `no-kubernetes.md`,
piensa qué problemas resuelve k8s (orquestar *muchos* servicios, auto-escalar, self-healing) y
pregúntate si 3 usuarios crean alguno de esos problemas. Revisa las secciones 4.1, 4.6 y 5 de la
lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/plan-de-despliegue.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/plan-de-despliegue.md` — no la mires
antes de intentarlo de verdad.
