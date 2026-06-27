---
ejercicio_id: fase-5/compose-app-postgres-redis
fase: fase-5
sub_unidad: "5.1"
version: 1
---

# Rúbrica — Compón el stack: app + Postgres + Redis con health gates

> Rúbrica **analítica** atada a los `objetivos` del contrato. El linter (`test_compose.py`) verifica la estructura; esta rúbrica mide la **comprensión** de los tres conceptos que el linter no puede ver: redes (descubrimiento por nombre), orden de arranque (la *race condition* que evita el health gate) y manejo de secretos. Un `compose.yaml` puede pasar el linter y el `notas.md` revelar que el alumno no entiende por qué `depends_on` corto falla.

## Objetivos evaluados
- **O1** — Componer un stack multi-servicio (app + Postgres + Redis) sin el campo `version` obsoleto.
- **O2** — Orquestar el orden de arranque con `depends_on` + `condition: service_healthy` apoyado en healthchecks reales.
- **O3** — Configurar red por nombre de servicio, named volume para persistencia y secretos por variable de entorno.

## Criterios y niveles

### C1 — Corrección: ¿el stack está bien compuesto? · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta algún servicio, hay campo `version:`, o `test_compose.py` falla en varios checks. |
| **en-progreso** | Los tres servicios existen pero el orquestado falla: `depends_on` en forma corta, healthchecks ausentes, o la DB sin volumen. |
| **competente** | Pasa el linter: sin `version`, imágenes pinneadas, healthchecks en db y cache, `depends_on: condition: service_healthy`, named volume, hostnames por nombre de servicio, contraseña por `${...}`. |
| **excelente** | Lo anterior + extras defendibles: `restart: unless-stopped`, `start_period` razonado, `.env` realmente en `.gitignore`, o uso de `secrets`/`env_file` en vez de `environment` para datos sensibles. |

### C2 — Orquestación y confiabilidad de arranque · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `depends_on: [db]` (forma corta) o sin `depends_on`; la api puede arrancar antes que Postgres acepte conexiones. |
| **en-progreso** | Usa `service_healthy` pero el healthcheck de la DB es débil (p. ej. `test: ["CMD", "true"]`) o sin `pg_isready`. |
| **competente** | Healthchecks reales (`pg_isready`, `redis-cli ping`) con intervalos sensatos, y la api espera a ambos sanos. |
| **excelente** | Explica la *race condition* concreta que evita y/o reconoce que un health gate de Compose no sustituye reintentos con backoff en la app (lo de [`3.14`/resiliencia](/fase-3-backend/)). |

### C3 — Red y descubrimiento de servicios · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | URLs con `localhost` o una IP hardcodeada para alcanzar la DB/cache. |
| **en-progreso** | Usa nombres de servicio pero no sabe explicar por qué funcionan (cree que es "magia" de Docker). |
| **competente** | `@db:5432` y `cache:6379`; explica que Compose crea una red por defecto y el nombre del servicio es el hostname (DNS interno). |
| **excelente** | Menciona que el puerto interno (5432/6379) no necesita publicarse al host para que los servicios se hablen; solo se publica lo que el exterior consume (la api). |

### C4 — Manejo de secretos y comprensión (el `notas.md` calza) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Contraseña en texto plano en `compose.yaml`, o sin `.env.example`, o sin `notas.md`. |
| **en-progreso** | Usa `${POSTGRES_PASSWORD}` pero el `notas.md` responde a medias o confunde por qué la forma corta de `depends_on` no basta. |
| **competente** | Secreto por variable de entorno + `.env.example` documentado; el `notas.md` explica con sus palabras la *race condition* y el DNS interno. |
| **excelente** | Razona la diferencia entre `environment` y `secrets`/`env_file`, o por qué `.env` no debe commitearse mientras `.env.example` sí. |

## Errores típicos a marcar
- **`depends_on: [db]` (forma corta)** creyendo que espera a que Postgres esté listo → solo espera a que el contenedor arranque; carrera de inicialización.
- **Dejar el campo `version:`** arriba → obsoleto; Compose lo ignora y advierte.
- **Contraseña en texto plano** en `compose.yaml` (que va al repo) en vez de `${POSTGRES_PASSWORD}` desde `.env`.
- **`localhost` o IP** para alcanzar la DB desde la api → en la red de Compose se usa el nombre de servicio.
- **Postgres sin named volume** → al recrear el contenedor se pierden los datos.
- **`image: postgres:latest` / `redis:latest`** → no reproducible.
- **Healthcheck trivial** (`true`) que pasa siempre y no comprueba nada.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `compose.yaml` perfecto pero `notas.md` que **no explica** por qué la forma corta de `depends_on` falla (el concepto central del ejercicio).
- Uso de funciones avanzadas (`secrets`, `configs`, `profiles`, healthchecks con dependencias) que el alumno no puede justificar al nivel de la fase.
- `notas.md` que describe un comportamiento que el archivo no tiene, o vocabulario fuera de nivel.
- **Verificación sugerida:** pedir que explique, sin notas, qué pasaría si quita el `healthcheck` de `db` pero deja `condition: service_healthy`. Si entiende, sabe que la dependencia nunca se daría por sana y la api no arrancaría.

## Feedback sugerido (graduado)
> Nunca dar el `compose.yaml` de referencia antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu `depends_on` espera a que el contenedor de Postgres exista. Pero, ¿existe el contenedor y está Postgres listo para una conexión son lo mismo? ¿Cuánto tarda Postgres en inicializar?"
- **Pregunta socrática (nivel 2):** "¿De dónde saca tu api la dirección de la base de datos? Si nunca configuraste una IP, ¿quién traduce `db` a una dirección dentro de la red?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Lo que falta es atar el arranque a la *salud* real: añade un `healthcheck` con `pg_isready` a `db` y cambia `depends_on` a la forma larga con `condition: service_healthy`. Vuelve a explicar qué carrera estás evitando."

## Conexión con el proyecto / capstone
- Junto con el `Dockerfile`, este `compose.yaml` es la primera entrega del **[Capstone F5](/fase-5-devops/proyecto/)**: el stack local reproducible que luego se despliega ([`5.9`](/fase-5-devops/5-9-despliegue/)) e instrumenta con observabilidad ([`5.10`](/fase-5-devops/5-10-observabilidad/)). Los health gates y la config por entorno son la base del principio 12-factor de la [`5.2`](/fase-5-devops/5-2-12-factor/).
