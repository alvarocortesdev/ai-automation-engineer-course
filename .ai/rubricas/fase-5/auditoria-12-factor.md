---
ejercicio_id: fase-5/auditoria-12-factor
fase: fase-5
sub_unidad: "5.2"
version: 1
---

# Rúbrica — Auditoría 12-factor de un backend

> Rúbrica **analítica** atada a los `objetivos`. Es un ejercicio de **diagnóstico**:
> evalúa el razonamiento de `auditoria.md`, no una respuesta única (hay variantes válidas
> en la redacción del arreglo). Lo que importa es el factor correcto + un síntoma observable
> + un arreglo accionable, por violación.

## Objetivos evaluados
- **O1** — Diagnosticar las violaciones, nombrando el factor (número + nombre) de cada una.
- **O2** — Explicar el síntoma **observable en producción** de cada violación y un arreglo accionable.
- **O3** — Priorizar los arreglos por riesgo (seguridad vs operativo) en un ADR corto.

## Las violaciones sembradas (referencia del corrector)
> Hay seis claras (III aparece dos veces, en código y en la imagen). El alumno debería cazar al menos seis.
1. **Factor III** — `DATABASE_URL`/`STRIPE_API_KEY`/`PORT` hardcodeados en `app.py`.
2. **Factor III + seguridad** — `ENV STRIPE_API_KEY=...` horneado en la imagen (`Dockerfile`); visible con `docker history`.
3. **Factor VI** — estado en memoria del proceso (`SESSIONS`, `CARRITOS`) en `app.py`.
4. **Factor XI** — logs a un archivo (`/var/log/tienda/app.log`) en vez de stdout.
5. **Factor VII** — puerto fijo en el código (`port=PORT`) en vez de leído de config.
6. **Factor X** — paridad rota: SQLite en dev vs Postgres en prod (comentarios en `app`/`compose`).
7. **Factor II** — deps sin pinear ni lockfile (`pip install fastapi uvicorn ...`) en el `Dockerfile`. (bonus)
8. **Factor IV** — la URL de la base no es un recurso adjunto intercambiable (está en el código). (se solapa con III)

## Criterios y niveles

### C1 — Cobertura y precisión del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Encuentra dos o menos, o asigna factores equivocados (confunde III con II, o VI con IV sin matiz). |
| **en-progreso** | Encuentra 3–4 con el factor correcto, pero se le escapa el estado en memoria o el secreto de la imagen. |
| **competente** | Encuentra al menos 6 con el factor correcto, incluyendo el secreto en código y en imagen, el estado en memoria, los logs y el puerto. |
| **excelente** | Caza también la paridad dev/prod (X) y las deps sin pinear (II), y distingue con matiz III (config) de IV (recurso adjunto). |

### C2 — Calidad del síntoma y del arreglo · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Síntomas genéricos ("es mala práctica", "no es seguro") sin un efecto observable. |
| **en-progreso** | Algún síntoma concreto, pero varios arreglos vagos ("mejorar la config") o incorrectos ("usar Kubernetes"). |
| **competente** | Cada síntoma es observable (reinicio pierde sesión, secreto filtrado al repo/imagen, log que llena disco) y cada arreglo es accionable (vars de entorno, Redis/DB, stdout, `$APP_PORT`). |
| **excelente** | Liga el síntoma a un escenario de operación (dos réplicas tras balanceador, redeploy) y conecta el arreglo con el resto de la fase (secret-scanning de `5.4`, observabilidad de `5.10`). |

### C3 — Priorización y defensa (ADR) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin ADR, o prioriza sin criterio ("arreglar todo a la vez"). |
| **en-progreso** | Prioriza pero el criterio es débil o no justifica el porqué. |
| **competente** | Prioriza el secreto horneado primero por riesgo de seguridad y lo justifica; identifica el Factor VI como el que bloquea el escalado. |
| **excelente** | ADR con trade-off real (riesgo de filtración irreversible vs riesgo operativo recuperable) y orden defendible del resto. |

## Errores típicos a marcar
- **Síntoma genérico:** "es inseguro" no es un síntoma; "la clave queda en el historial de la imagen y cualquiera con la imagen la extrae" sí lo es.
- **Confundir III con IV:** III = la config (incluida la URL) vive en el entorno; IV = la base es un recurso adjunto intercambiable. Se solapan, pero el alumno debería notar el matiz.
- **Confundir VI con VIII:** VI es "procesos sin estado"; VIII es "escalar lanzando más procesos". VIII depende de VI; no son lo mismo.
- **Arreglo desproporcionado:** "migrar a Kubernetes/microservicios" para arreglar config o logs.
- **No ver el secreto de la imagen:** muchos cazan el del código pero olvidan el `ENV ...` del `Dockerfile`, que es igual de grave (queda en una capa).
- **Olvidar la paridad dev/prod:** la pista vive en los comentarios (SQLite vs Postgres); quien no lee los comentarios la pierde.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Lista de violaciones impecable pero síntomas genéricos: señal de que pidió "los factores que viola" sin razonar el efecto.
- Cita factores que **no** están violados aquí (p. ej. I codebase, IX disposability sin evidencia) para "rellenar".
- ADR genérico que no compromete una prioridad ("depende del contexto") sin tomar postura.
- **Verificación sugerida:** pídele que, sin notas, describa qué pasa exactamente con la sesión de un usuario cuando este backend corre en dos réplicas. Si no llega al "401 intermitente al saltar de réplica", no internalizó el Factor VI.

## Feedback sugerido (graduado)
> Nunca enumerar tú las violaciones que faltan antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Recorre los siete factores del corazón de la lección uno por uno y búscalos en los tres archivos. ¿Cuántos cazaste de siete?"
- **Pregunta socrática (nivel 2):** "Imagina que el contenedor reinicia a mitad de la tarde. ¿Qué pierden los usuarios? ¿Y si levantas una segunda réplica?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Te faltó el secreto horneado en el `Dockerfile` (Factor III en la imagen) y el estado en memoria (`SESSIONS`, Factor VI). Mira `docker history` mentalmente y el escenario de dos réplicas. Repasa 4.2 y 4.4."

## Conexión con el proyecto / capstone
- Es el ensayo de la auditoría que correrás sobre tu propio `Dockerfile`/`compose.yaml` antes del despliegue del capstone de la Fase 5. Cada violación cazada aquí es un incidente de producción evitado allá, y alimenta el ADR de despliegue que el Definition of Done espera.
