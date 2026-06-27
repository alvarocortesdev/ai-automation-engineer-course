---
ejercicio_id: fase-5/capstone-pipeline-produccion
fase: fase-5
sub_unidad: "5.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es un **deploy ejemplar**, no "la" respuesta: un capstone de infraestructura admite muchas topologías válidas. Úsala como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Capstone Fase 5: Pipeline completo a producción

## Respuesta canónica (forma de un deploy ejemplar)

Un capstone **competente** tiene, como mínimo:

1. **Empaquetado reproducible.** Dockerfile multi-stage (builder instala desde el lockfile; runtime parte de `python:3.13-slim` pinneada), corre como usuario no-root, `HEALTHCHECK` a `/health`, imagen sin toolchain de build. El deploy referencia la imagen por **digest `sha256:...` o tag de versión inmutable**, jamás `:latest`.
2. **Config 12-factor.** Toda la config en el entorno; `.env.example` con todas las claves sin valores; **cero secretos en el repo** (verificable porque el secret-scan pasa limpio); secretos de CI en GitHub Actions secrets, secretos de runtime en el secrets-manager del destino.
3. **Pipeline CI con gate de PR.** `ci.yml`: lint → test (los de la API F3) → build, que **bloquea el merge** si está rojo. Más los gates de supply chain: **SCA** (pip-audit/npm audit), **secret-scanning** (gitleaks), **escaneo de imagen** (Trivy), **SBOM** (CycloneDX) como artefacto. Todas las actions **pinneadas a SHA**, `permissions: contents: read` por defecto y subido solo donde hace falta. Dependabot configurado.
4. **Deploy.** `deploy.yml` en push a `main`, gateado por un Environment `production`, que construye/publica la imagen inmutable y la despliega a un destino real (VPS+Caddy / homelab+Cloudflare Tunnel / Vercel para el frontend), con smoke post-deploy a `/health`. Rollback documentado.
5. **Observabilidad.** Logs estructurados (JSON), **correlation ID** generado por request y propagado por todo el call-chain (en logs y como atributo de span), **trazas OTel** con `ConsoleSpanExporter` en dev y `OTLPSpanExporter` listo para prod.
6. **Dominio + HTTPS.** Responde en un dominio propio con TLS (Caddy/Let's Encrypt o Cloudflare Tunnel terminando TLS). HTTP plano no califica.
7. **≥3 usuarios reales** documentados, observados con la telemetría.
8. **Cierre.** `SPEC.md` (antes del pipeline), ≥1 ADR con alternativas/consecuencias, `RUNBOOK.md`, `WRITE-UP.md` (trade-offs + costo + falla), README en inglés, demo viva, Conventional Commits.

## Razonamiento paso a paso (el porqué, para explicar — no para dictar)

- **Por qué imagen inmutable y no `:latest`:** producción exige saber *exactamente* qué corre y poder volver atrás con certeza. `:latest` es un puntero móvil; el digest es un contrato. Sin esto no hay rollback determinista ni auditoría.
- **Por qué los gates van separados de lint/test:** lint/test verifican *correctitud funcional*; los gates de supply chain verifican que sea *seguro desplegar*. Un CVE crítico o un secreto filtrado pasan el test verde. Cada gate previene un ataque concreto: SCA → dependencia vulnerable conocida; secret-scan → fuga de credenciales; escaneo de imagen → CVEs en capas base/OS; SBOM → trazabilidad de qué hay dentro (responder rápido al próximo Log4Shell); pin a SHA → supply-chain attack si comprometen un tag/rama mutable de una action; `permissions` mínimos → contener el blast radius si un step es comprometido.
- **Por qué observabilidad ANTES de exponer:** la telemetría solo sirve si captura el momento de la falla. Instrumentar "cuando haya un problema" significa no tener datos del primer problema. El correlation ID es lo que convierte "un usuario tuvo un 500" en "el request `req-8f3a` falló en el span `query_postgres` por timeout".
- **Por qué la promesa de OTel importa:** cambiar `ConsoleSpanExporter` → `OTLPSpanExporter` no toca el código de instrumentación. El alumno gana visibilidad en dev y portabilidad a cualquier backend (Grafana/Datadog/etc.) en prod con una línea.
- **Por qué ≥3 usuarios reales:** el tráfico sintético no produce las fallas que producen los humanos (sesiones que expiran a mitad de flujo, concurrencia, navegadores raros). Es la condición que genera la **historia de falla en producción** —la narrativa de semi-senior de Track-0.

## Puntos resbalosos (donde el corrector debe mirar)

1. **`:latest` "disimulado":** a veces el CI taggea por SHA pero el `deploy`/`compose` sigue apuntando a `:latest` o a una tag móvil. Verifica que el deploy use la **misma** referencia inmutable que se testeó.
2. **Secreto "fuera del repo" pero escrito en claro en el runner** (`echo SECRET > .env` dentro del job): sigue siendo una fuga (queda en logs/artefactos). Debe inyectarse vía `secrets.` en el entorno del step, no materializarse en disco.
3. **Gate decorativo:** el job existe pero está en `continue-on-error: true` o no falla nunca. Un gate que no bloquea no es un gate.
4. **`permissions` amplio "temporal":** `write-all` o el default amplio del workflow sin minimizar por job.
5. **Correlation ID que no se propaga:** se genera pero no viaja al call-chain (no aparece en los spans hijos ni en los logs de las funciones internas). Sin propagación no reconstruye el recorrido.
6. **Deploy manual disfrazado:** el "pipeline" solo hace SSH `git pull && up` —no construye ni despliega la imagen verificada.
7. **HTTPS ausente o mal terminado:** responde en `http://IP:puerto`, o el cert está auto-firmado/expirado.

## Rango de soluciones aceptables (NO penalizar caminos válidos distintos)

- **Destino de deploy:** VPS + Caddy, homelab + Cloudflare Tunnel, o Vercel/Fly/Render para el frontend/servicio son **todos válidos**. Lo que se evalúa es reproducibilidad + HTTPS + config por ambiente, no el proveedor.
- **Stack:** API en Python (FastAPI, el troncal del curso) o el frontend en Node/Next; los gates concretos cambian (pip-audit vs. npm audit) pero el patrón es el mismo.
- **Registry:** GHCR, Docker Hub, o el del proveedor cloud —indistinto si la referencia es inmutable.
- **Herramientas de gate:** pip-audit/osv-scanner/Snyk para SCA; gitleaks/trufflehog para secret-scan; Trivy/Grype para imagen; CycloneDX/Syft para SBOM. Cualquier combinación coherente que cubra las cuatro superficies cuenta como competente.
- **Backend de telemetría:** Console en dev + cualquier colector OTLP (Grafana Tempo, Jaeger, Datadog, Langfuse más adelante) en prod.
- **Costo ≈ 0** (homelab) es perfectamente aceptable; lo evaluado es que el alumno **conozca y declare** su costo, no que gaste dinero.
- **Sin frontend desplegado** es aceptable (el frontend F4 es recomendado, no obligatorio): en ese caso C5/DoD-7 no aplica y no se penaliza su ausencia.
- **"La falla" puede ser provocada:** si con usuarios reales no se rompió nada todavía, un alumno excelente provoca una falla controlada (apaga la DB, mete un timeout) y demuestra el diagnóstico vía traza + el rollback. Eso cuenta como historia de falla.
