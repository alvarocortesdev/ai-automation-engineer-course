---
ejercicio_id: fase-5/capstone-pipeline-produccion
fase: fase-5
sub_unidad: "5.P"
version: 1
---

# Rúbrica — Capstone Fase 5: Pipeline completo a producción

> Rúbrica **analítica** atada a los `objetivos` del contrato y al **Definition of Done único** (§B). El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar.
>
> **Es un capstone de infraestructura: NO hay una única respuesta correcta.** Evalúa si el deploy es **reproducible, seguro y observable** y si el alumno **defiende sus trade-offs** —no si eligió "el" proveedor. Un homelab con Cloudflare Tunnel bien hecho vale tanto como un VPS con Caddy o Vercel.
>
> **Antes de evaluar:** verifica que haya intento real (spec/ADRs + workflows + Dockerfile + evidencia de deploy). Si el alumno no intentó (carpeta con plantillas vacías), pide que primero lo trabaje (timebox por sesión 45 min) y detente. **Nunca entregues YAML/Dockerfile de la solución de referencia.**

## Objetivos evaluados
- **O1** — Producción reproducible: Docker multi-stage + config 12-factor + dominio/HTTPS.
- **O2** — Pipeline CI/CD con gates de seguridad/supply chain que bloquean en rojo.
- **O3** — Observabilidad instrumentada + ≥3 usuarios reales + cierre (spec/ADR/runbook/write-up).

## Criterios y niveles

### C1 — Reproducibilidad del empaquetado y deploy · mapea: O1 · (DoD 1 parcial)
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Sin Dockerfile o monolítico; usa `:latest`; el deploy es manual por SSH no documentado; sin config 12-factor (secretos/constantes en el código). |
| **en-progreso** | Dockerfile funciona pero sin multi-stage o corre como root; imagen no pinneada; config parcialmente en el entorno pero algún secreto o constante sigue en el código/repo. |
| **competente** | Multi-stage, base pinneada y slim, no-root, HEALTHCHECK; config 12-factor con `.env.example` completo y **cero secretos en el repo**; deploy referencia imagen por digest/tag inmutable; dominio propio con HTTPS. |
| **excelente** | Además: rollback determinista documentado y probado; imagen mínima justificada (tamaño/superficie); paridad dev/prod real vía Compose; smoke post-deploy contra `/health`. |

### C2 — Pipeline CI/CD y gates de seguridad/supply chain · mapea: O2 · (DoD 2, DoD 3)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay pipeline, o solo build/deploy sin tests; sin ningún gate de seguridad; `permissions: write-all`; actions a `@main`/`@vX`. |
| **en-progreso** | Pipeline con lint+test (gate de PR), pero **faltan gates** (solo uno de SCA/secret-scan/imagen/SBOM); algunas actions pinneadas, otras no; `permissions` no minimizados. |
| **competente** | lint → test (los de F3) → build con gate de PR que bloquea; **SCA + secret-scanning + escaneo de imagen + SBOM**; **todas** las actions a SHA; `permissions` mínimos por job; Dependabot configurado. El alumno explica **qué ataque previene cada gate**. |
| **excelente** | Además: gates fallan de verdad (demuestra un caso rojo); environment de prod con aprobación/auditoría; deploy de la **misma imagen** testeada; trade-off pin-SHA vs. Dependabot razonado en write-up/ADR. |

### C3 — Observabilidad y operación con usuarios reales · mapea: O3 · (DoD 4)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Observabilidad" = `print()`; sin correlation IDs; sin trazas; ningún usuario real (solo el autor). |
| **en-progreso** | Logs estructurados **o** trazas, pero no ambos; correlation ID inexistente o no propagado por el call-chain; usuarios reales ausentes o no documentados. |
| **competente** | Logs estructurados (JSON) + **correlation ID** propagado por el call-chain + **trazas OTel** funcionando en el deploy real; **≥3 usuarios reales** documentados (quiénes/qué). |
| **excelente** | Además: demuestra un diagnóstico real vía correlation ID/traza (la historia de falla); deja listo `OTLPSpanExporter` para prod explicando la promesa de OTel; nombra RED/USE o un SLO incipiente. |

### C4 — Comprensión demostrada y comunicación · mapea: O1-O3 · (DoD 1, DoD 8, DoD 9)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin SPEC/ADR; sin write-up; README inexistente o no en inglés; historial sin Conventional Commits; no hay demo viva. |
| **en-progreso** | SPEC o write-up presente pero superficial; un ADR sin alternativas; README en inglés parcial; commits mezclados. |
| **competente** | `SPEC.md` escrita antes del pipeline + ≥1 ADR con alternativas y consecuencias; `RUNBOOK.md` (deploy/rollback); `WRITE-UP.md` con trade-offs y **costo estimado**; README **en inglés**; **demo viva** (URL); Conventional Commits en todo el historial. |
| **excelente** | El write-up incluye la **falla con usuarios reales** y su post-mortem; los ADRs anticipan F6 (este pipeline desplegará el RAG); trade-offs defendibles sin notas. |

<!-- C5 (a11y) SOLO si despliega el frontend F4: -->
### C5 — a11y (condicional, solo si hay UI desplegada) · (DoD 7)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | UI desplegada sin gate de a11y ni estados. |
| **competente** | Se mantiene el gate WCAG 2.2 + cuatro estados de la Fase 4 en el deploy. |
| **excelente** | a11y verificada en la URL real (teclado/contraste), no solo en local. |

## Errores típicos a marcar
- Imagen `:latest` o no pinneada → irreproducible, sin rollback determinista.
- Secretos en el repo / en `compose.yaml` / escritos a un `.env` en claro dentro del runner.
- `permissions: write-all` o por defecto amplios; actions a `@main`/`@vX` en vez de SHA.
- "CI verde = seguro": tiene lint+test pero ningún gate de supply chain.
- Deploy manual por SSH (`git pull && up`) en vez de pipeline; o deploy de una imagen distinta a la testeada.
- Observabilidad agregada "para después": solo `print()`, sin correlation ID propagado ni trazas.
- HTTP plano / IP:puerto en vez de dominio + HTTPS.
- Sin usuarios reales (o tráfico sintético disfrazado).
- (transversales) persigue coverage% en vez de aserciones; falta un trade-off defendible; gate de cargo-cult que el alumno no sabe justificar; CORS `*`.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- YAML/Dockerfile sofisticado y correcto, pero el alumno **no sabe qué ataque previene cada gate** ni por qué pinea a SHA → pídele que explique un job concreto línea por línea.
- ADRs/write-up genéricos que no mencionan **su** topología, **su** costo ni **sus** usuarios reales → señal de texto generado sin operar nada real.
- "Tengo trazas" pero no puede mostrar un span ni buscar por un correlation ID → pídele que diagnostique en vivo un 500 inventado.
- **Verificación sugerida:** pídele que provoque una falla controlada (apagar la DB) y la diagnostique solo con sus trazas/logs, cronometrándose. Si instrumentó de verdad, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el YAML/Dockerfile de la solución. Primero pistas, luego preguntas, y solo tras intento real, dirección concreta.
- **Pista (nivel 1):** "Tu pipeline pasa lint y test, pero ¿qué le impide desplegar una dependencia con un CVE crítico hoy mismo? Mira qué gates de la 5.4 te faltan."
- **Pregunta socrática (nivel 2):** "Si comprometen el repo de una action que usas con `@v4`, ¿qué pasa en tu próximo deploy y con tus secretos? ¿Cómo lo evitarías sin congelarte para siempre en una versión?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a corregir es la **superficie de supply chain**: pinea cada `uses:` a un commit SHA (no a un tag), baja `permissions` a `contents: read` por job, y añade un job de SCA que falle el build ante un CVE conocido. No te doy el YAML: reescribe el workflow con esos tres cambios y verifica que un caso rojo lo bloquee."

## Conexión con el proyecto / capstone
- Esta es la **infraestructura reutilizable** del resto del curso: el mismo pipeline despliega el RAG de la [Fase 6](/fase-6-ai-engineering/) y el agente de la Fase 7; las trazas pasan a llevar tokens/latencia/costo del LLM. Los ≥3 usuarios reales son la **semilla directa** de la historia de falla en producción de Track-0.
