# Capstone Fase 5 — Pipeline completo a producción

> **Modalidad: proyecto (Primero-Sin-IA para las decisiones de arquitectura).** Timebox sugerido: **20–30 h repartidas en 2–3 semanas**. No es un ejercicio con tests pre-escritos: tú decides la topología, la config, dónde corre y cómo lo observas —y luego lo defiendes. La IA puede ayudarte a *teclear* YAML, pero las **decisiones** (qué gates, dónde corre, cómo haces rollback, qué instrumentas) las razonas tú: son justo lo que un live coding / system design de entrevista examina.

Lleva a **producción real** el sistema que ya construiste:

- **Obligatorio:** tu [API de la Fase 3](../../../src/content/docs/fase-3-backend/proyecto.mdx) (FastAPI + Postgres).
- **Recomendado:** tu frontend de la Fase 4 (Next.js).

"Producción real" significa que **otra persona, que no eres tú, lo usa** —con dominio propio, HTTPS, un pipeline que lo despliega solo, y observabilidad que te deja diagnosticar una falla.

---

## Objetivos

- **O1** — Llevar el servicio a producción de forma **reproducible**: imagen Docker multi-stage, config 12-factor, deploy con dominio propio y HTTPS.
- **O2** — Construir un **pipeline CI/CD** (GitHub Actions) con **gates de seguridad y supply chain** que bloquean el merge/deploy cuando algo está rojo.
- **O3** — Instrumentar **observabilidad** (logs estructurados + correlation IDs + trazas OTel) y operar con **≥3 usuarios reales**, cerrando con spec/ADRs/runbook/write-up.

---

## Tu tarea (en este orden — la spec antes que el servidor)

Sigue el orden de la sección 4 de la lección. **No empieces por el servidor.**

1. **Config 12-factor + spec.** Llena `.env.example` con todas las claves (sin valores). Escribe `docs/SPEC.md`: qué despliegas, dónde corre, cómo se promueve un cambio, cómo haces rollback. Escribe al menos un ADR en `docs/adr/` (usa la plantilla).
2. **Empaqueta.** Completa el `Dockerfile` multi-stage (base pinneada y slim, no-root, HEALTHCHECK). Reusa el del ejercicio `dockerizar-fastapi` y endurécelo.
3. **Pipeline base.** Completa `.github/workflows/ci.yml`: lint → test (los de tu F3) → build. El gate de PR bloquea si está rojo.
4. **Gates de seguridad/supply chain.** Sobre el CI, añade SCA, secret-scanning, SBOM y escaneo de imagen. Pinea todas las actions a un **commit SHA**, aplica `permissions` mínimos por job, y configura `.github/dependabot.yml`.
5. **Observabilidad.** Instrumenta tu API con OTel (trazas + correlation ID) y logs estructurados. **Antes** de exponer.
6. **Deploy con dominio + HTTPS.** Completa `.github/workflows/deploy.yml` y despliega (VPS+Caddy, homelab+Cloudflare Tunnel, o Vercel para el frontend). Documenta el rollback en `docs/RUNBOOK.md`.
7. **Usuarios reales.** Invita a ≥3 personas. Obsérvalas con tus trazas. Anota quiénes y qué hicieron en `WRITE-UP.md`.
8. **Cierra.** `RUNBOOK.md`, `WRITE-UP.md` (trade-offs + costo estimado + qué falló), README en inglés, Conventional Commits.

---

## Criterios de "hecho" (mapeados al Definition of Done único del curso)

Está **hecho** solo si cumple **todo** lo que aplica (DoD 5 y 6 NO aplican: aún no hay IA):

- [ ] **(DoD 1)** `docs/SPEC.md` escrita **antes** del pipeline + ≥1 **ADR** real (dónde corre / rollback / contrato de config).
- [ ] **(DoD 2)** **Tests verdes + lint en CI**: los tests de tu F3 corren en el pipeline; el gate de PR bloquea si fallan. Calidad por aserciones, no coverage%.
- [ ] **(DoD 3)** **Seguridad y supply chain:** OWASP web de F3 en pie + **SCA + secret-scanning + escaneo de imagen + SBOM** en el pipeline + actions pinneadas a **SHA** + `permissions` mínimos por job + Dependabot.
- [ ] **(DoD 4)** **Observabilidad instrumentada:** logs estructurados (JSON) + **correlation ID** por request en el call-chain + **trazas OTel**, funcionando en el deploy real.
- [ ] **Empaquetado reproducible:** Dockerfile multi-stage, base pinneada (nada de `:latest`), no-root, HEALTHCHECK. El deploy referencia una imagen por **digest o tag inmutable**.
- [ ] **Config 12-factor:** toda la config en el entorno; `.env.example` completo; **cero secretos en el repo**.
- [ ] **Dominio + HTTPS:** el servicio responde en un dominio propio con HTTPS (HTTP plano no cuenta).
- [ ] **≥3 usuarios reales** usándolo (no tú; no tráfico sintético). Documentados.
- [ ] **Costo:** estimación del costo mensual del deploy (aunque sea ≈0 en homelab).
- [ ] **(DoD 7, si despliegas el frontend F4)** a11y WCAG 2.2 + cuatro estados, como en la Fase 4.
- [ ] **(DoD 8)** **Demo que corre** (la URL viva) + **README en inglés** + **`WRITE-UP.md`** de trade-offs (incluida la falla con usuarios reales, si la hubo).
- [ ] **(DoD 9)** **Conventional Commits** en todo el historial.

---

## Qué entregar (deja estos archivos en esta carpeta)

- `Dockerfile`, `compose.yaml`, `.dockerignore`, `.env.example` — empaquetado y config.
- `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `.github/dependabot.yml` — pipeline.
- `app/` — tu API de la F3, instrumentada con OTel.
- `docs/SPEC.md`, `docs/adr/*.md`, `docs/RUNBOOK.md` — spec, decisiones, operación.
- `WRITE-UP.md` — trade-offs, costo estimado, usuarios reales, qué falló.
- `README.md` (en inglés) — cómo correrlo + la URL viva de la demo.

> Las plantillas (`SPEC.md`, ADR, `RUNBOOK.md`, `WRITE-UP.md`) y los esqueletos de workflow ya están en esta carpeta con TODOs. Bórralos/llénalos a medida que avanzas.

---

## Pedir corrección

Cuando termines (o si te trabas tras intentarlo de verdad), pídele a tu IA:

> "Corrige `ejercicios/fase-5/capstone-pipeline-produccion/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **infraestructura y tus decisiones** (reproducibilidad, gates, observabilidad, defensa de trade-offs), no si elegiste "el" proveedor correcto. No existe una única respuesta.
