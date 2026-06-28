# Capstone Fase 7 ★ — Automatización end-to-end agéntica

> **El proyecto estrella de tu portafolio.** Un sistema que recibe un input real (webhook / cola / documento), deja que la IA lo **clasifique y extraiga** (salida estructurada validada), **decida** la acción con un plano de control determinista, y la **ejecute en un sistema externo** con todas las garantías de producción. No es una demo de video: es software que sostienes.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.P` Capstone
**Ruta:** crítica · **Modalidad:** proyecto multi-sesión (Fases A–D)
**Timebox:** el diseño Primero-Sin-IA es 30–45 min; cada milestone (A/B/C/D) tiene su propio ritmo. No hay timebox único: es un capstone.

La lección con el brief completo, el ejemplo resuelto y la anatomía está en `/fase-7-automatizacion/proyecto/`. Este README es el contrato operativo del entregable.

## 🎯 Objetivo

Diseñar, implementar y **sostener** una automatización agéntica end-to-end de producción que cumpla el **Definition of Done único completo (los 9 puntos)**, y comunicarla como ingeniero senior (demo que corre, README en inglés, write-up de trade-offs, historia de falla en producción).

## 📋 Contexto

Es el capstone que te diferencia del 80% de portafolios (el RAG genérico). Ensambla todo el curso: salida estructurada + agent loop + evals + seguridad LLM + costo/latencia (Fase 6); idempotencia + DLQ + integración confiable + ejecución durable + data contracts (Fase 7); observabilidad + CI/CD (Fase 5). La columna vertebral conceptual es la sub-unidad `7.7`.

Dominio sugerido (usa este o uno tuyo equivalente): **tickets de soporte que pueden gatillar un reembolso**. El mismo patrón sirve para facturas, onboarding o correos. La acción externa puede ser real (una API tuya/de prueba) o un sistema simulado idempotente —lo que importa es que el manejo de fallas sea real.

## 📏 Primero-Sin-IA (el diseño, antes que el código)

Antes de escribir una línea, crea `DISENO.md` en tu repo y, **a mano y sin IA** (30–45 min):

1. **Diagrama de arquitectura** (Mermaid o foto de papel) marcando dónde vive cada uno de los **9 puntos del Definition of Done**.
2. **Tabla de decisión del plano de control**: para cada combinación relevante de `(ya_procesado, schema_valido, costo_acumulado, accion_sensible, confianza)`, cuál es la ruta (`AUTO` / `HITL` / `RECHAZO` / `DUPLICADO`) y por qué. Incluye **al menos un caso que dispare dos barreras a la vez** (p. ej. duplicado + acción sensible) e indica cuál gana.
3. **ADR** corto: por qué **Temporal** (ejecución durable) y no un cron + cola para este caso.

Solo después codeas. Si no puedes dibujar el flujo de un duplicado-que-además-es-sensible sin ejecutar nada, todavía no lo entiendes.

## 🛠️ Plan de construcción (vertical slices, andamiaje que se desvanece)

- **Fase A — Slice mínimo que corre.** Webhook FastAPI → `clasificar_y_extraer` (llamada directa al LLM, sin Temporal aún) → `decidir()` → imprime la ruta. **Hecho:** un `curl` con un ticket devuelve la ruta correcta.
- **Fase B — Confiabilidad de entrada.** HMAC + anti-replay; idempotency key por `message_id`; DLQ para schema inválido / poison messages. **Hecho:** un replay del mismo webhook NO re-ejecuta; firma mala se rechaza.
- **Fase C — Durabilidad + HITL.** Orquestación en un workflow Temporal con actividades; espera durable de la señal de aprobación para acciones sensibles. **Hecho:** matas el worker a mitad de una espera HITL, lo reinicias, y el workflow retoma sin perder estado.
- **Fase D — Producción.** Trazas OTel (`message_id` como correlation id; tokens/latencia/costo por paso); eval gate del agente sobre un golden set en CI con baseline versionado; techo de costo; CI/CD; **3 usuarios reales**. Luego **rompe algo a propósito**, obsérvalo en las trazas, reconcilia, y escribe el post-mortem.

> El plano de control determinista es la pieza más examinable y la base de todo: hazlo pasar los tests del `starter/` en verde antes de construir la infraestructura alrededor.

## ✅ Criterios de "hecho" (Definition of Done único — los 9 puntos)

- [ ] **1. Spec + ADRs** — `DISENO.md` (diagrama + tabla de decisión + ADR de Temporal).
- [ ] **2. Tests verdes + lint en CI** — `control_plane.py` pasa los tests del starter; aserciones reales sobre las rutas; no persigues coverage%.
- [ ] **3. Seguridad** — HMAC + anti-replay del webhook (OWASP web); guardrail de schema + least-privilege de tools + HITL (OWASP LLM01/05/06); secret-scanning (gitleaks) + SCA en el pipeline.
- [ ] **4. Observabilidad** — structured logs + correlation id (`message_id`) + trazas OTel; span por paso con tokens/latencia/costo.
- [ ] **5. Eval gate del agente** — harness versionado + número + gate de regresión que bloquea el deploy + budget de costo/latencia, como entregables de primera clase.
- [ ] **6. Plano de control** — validación de salida antes de ejecutar + least-privilege + HITL para acciones sensibles + techo de costo (el `control_plane.py` completo).
- [ ] **7. a11y (si hay UI)** — si construyes una UI/consola para el HITL (recomendado), WCAG 2.2 mínima + estados empty/loading/error/success.
- [ ] **8. Demo que corre + README en inglés + write-up** — `docker compose up` (o equivalente) + demo script; `README.md` en inglés; `WRITE-UP.md` con trade-offs, número del eval y costo/latencia medidos.
- [ ] **9. Conventional Commits** en todo el historial.
- [ ] **(Track-0) Historia de falla en producción** — `POST-MORTEM.md`: qué rompiste, cómo se vio en las trazas, cómo reconciliaste sin perder ni duplicar, qué cambiaste.
- [ ] Puedes **explicar tu arquitectura completa sin notas, en inglés, en menos de 5 minutos** (check de dominio).

## 📦 Entregables mínimos

- Repo con el sistema que **corre** + demo script/curl que procesa un caso end-to-end.
- `README.md` **en inglés** (qué hace, cómo correrlo, arquitectura).
- `DISENO.md` (diagrama + tabla de decisión + ADR de Temporal).
- `WRITE-UP.md` (trade-offs: qué elegí, qué medí, qué falló; número del eval gate + baseline; costo/latencia).
- `POST-MORTEM.md` (la historia de falla en producción).

## 🧰 Scaffold inicial

En `starter/` tienes:

- `schemas.py` — el modelo pydantic de la propuesta del LLM (el "cerebro" llena esto).
- `control_plane.py` — el plano de control determinista con `decidir(...)` **a completar** (TODOs). Es puro, sin red: testeable exhaustivamente.
- `test_control_plane.py` — los tests que **gatean** tu plano de control. Corre `uv run pytest` (o `pytest`) en `starter/`.
- `.env.example` — variables de entorno (no commitees secretos reales).
- `starter/README.md` — cómo usar el scaffold y la estructura de repo sugerida.

Copia el scaffold a tu repo del proyecto y construye alrededor de él.

## 🤖 Cómo pedir la corrección

Cuando termines (o quieras feedback de un milestone), entrega a tu IA:

- tu repo del proyecto (con `DISENO.md`, `WRITE-UP.md`, `POST-MORTEM.md` y el código),
- la **rúbrica**: `.ai/rubricas/fase-7/capstone-automatizacion-agentica.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

> "Corrige mi capstone `ejercicios/fase-7/capstone-automatizacion-agentica/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-7/capstone-automatizacion-agentica/` — no la mires antes de intentarlo de verdad. El corrector evalúa tu **sistema y tu razonamiento** contra el Definition of Done completo, no solo si los tests del plano de control pasan.
