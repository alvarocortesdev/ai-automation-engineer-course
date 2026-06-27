---
ejercicio_id: fase-5/dockerizar-fastapi
fase: fase-5
sub_unidad: "5.1"
version: 1
---

# Rúbrica — Dockeriza el backend FastAPI (multi-stage, seguro y mínimo)

> Rúbrica **analítica** atada a los `objetivos` del contrato. El linter (`test_dockerfile.py`) verifica los patrones mecánicos; esta rúbrica mide lo que el linter no ve: si el alumno **entiende por qué** cada decisión está ahí. Un `Dockerfile` puede pasar el linter y aun así revelar, en el `notas.md`, que no se comprende la caché de capas o el doble beneficio del multi-stage. La rúbrica distingue "pasó el linter" de "lo domina".

## Objetivos evaluados
- **O1** — Implementar un Dockerfile multi-stage que produce una imagen mínima copiando solo lo necesario al runtime.
- **O2** — Ordenar las instrucciones para aprovechar la caché de capas (manifiesto antes que el código).
- **O3** — Aplicar seguridad de imagen: base pinneada y slim, usuario no-root, HEALTHCHECK y `.dockerignore` que excluye secretos.

## Criterios y niveles

### C1 — Corrección: ¿el Dockerfile cumple el objetivo? · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No es multi-stage (un solo `FROM`), o no construye, o `test_dockerfile.py` falla en varios checks. |
| **en-progreso** | Multi-stage presente pero con fallas: copia todo el toolchain al runtime, o el orden de capas no aprovecha la caché, o corre como root. |
| **competente** | Pasa el linter: multi-stage real (`COPY --from`), base slim pinneada, orden de capas correcto, no-root, HEALTHCHECK sin curl, `.dockerignore` que excluye `.env`. |
| **excelente** | Lo anterior + decisiones extra defendibles: `--no-cache` en el instalador, `start-period` ajustado al arranque real, comentarios que explican el porqué, o medición real del tamaño de imagen en `notas.md`. |

### C2 — Calidad de ingeniería (imagen mínima y reproducible) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Imagen basada en `python:3.x` completo (no slim) y/o `:latest`; arrastra build tools a producción. |
| **en-progreso** | Slim pero sin separar build de runtime, o sin venv/artefacto limpio que copiar; la imagen final aún carga `uv`/compiladores. |
| **competente** | El runtime solo recibe el venv/artefacto construido; nada del toolchain de build llega a la imagen final. Tags fijos. |
| **excelente** | Justifica el tamaño con un número (antes/después) o explica el trade-off slim vs distroless; deja el `CMD` en *exec form* (lista JSON), no *shell form*. |

### C3 — Seguridad de imagen (supply chain básico) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Corre como root, o hornea un secreto (`ENV PASSWORD=...`), o no hay `.dockerignore` (riesgo de filtrar `.env`/`.git`). |
| **en-progreso** | No-root presente pero `.dockerignore` incompleto, o entiende a medias por qué el secreto en build es permanente. |
| **competente** | Usuario sin privilegios, sin secretos en build, `.dockerignore` que excluye `.env`/`.git`/`__pycache__`; explica que un secreto en una capa queda visible con `docker history`. |
| **excelente** | Conecta con OWASP / la [`5.4`](/fase-5-devops/5-4-seguridad-supply-chain-ci/): menciona reducción de superficie de ataque, pin por digest (`@sha256`) o escaneo de la imagen. |

### C4 — Comprensión demostrada (el `notas.md` calza con el Dockerfile) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `notas.md`, o repite definiciones sin responder las dos preguntas. |
| **en-progreso** | Responde una pregunta bien y la otra de forma vaga o incorrecta (p. ej. confunde qué capa se invalida). |
| **competente** | Explica con sus palabras el doble beneficio del multi-stage (tamaño + seguridad) y acierta qué capa se invalida al tocar `app/main.py` y cuál no. |
| **excelente** | Razona el *por qué* a nivel de modelo mental (capas como diffs apilados; la caché se invalida en cascada hacia abajo) y lo liga al costo de CI. |

## Errores típicos a marcar
- **`COPY . .` antes de instalar** → invalida la caché de dependencias en cada cambio de código y arrastra archivos no deseados (`.git`, `.env`).
- **Olvidar el `.dockerignore`** o no excluir `.env` → riesgo de hornear secretos y engordar la imagen.
- **Multi-stage "de adorno":** dos `FROM` pero sin `COPY --from`, o copiando todo el builder al runtime (no reduce nada).
- **`curl` en el HEALTHCHECK** sobre una imagen slim que no lo trae → el healthcheck falla siempre o obliga a instalar curl (más peso).
- **Quedarse como root** "porque funciona igual" → ignora defensa en profundidad.
- **`CMD` en *shell form*** (`CMD fastapi run ...`) en vez de *exec form* (lista JSON): rompe el manejo de señales (el proceso no recibe SIGTERM limpio).
- (transversales) confiar en `:latest`; no medir/justificar el tamaño; no conectar imagen mínima con menor superficie de ataque.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Dockerfile impecable y "de libro" pero `notas.md` que **no sabe explicar** qué capa se invalida al cambiar el código (la pregunta central de la caché).
- Flags o patrones sofisticados (`--mount=type=cache`, BuildKit secrets) que el alumno no puede justificar al nivel de la fase.
- `notas.md` con vocabulario que no calza con el resto del trabajo, o que describe un Dockerfile distinto del entregado.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué pasa con el tiempo de build si mueve `COPY ./app ./app` *encima* del `RUN install`. Si trazó de verdad el modelo de capas, responde al instante.

## Feedback sugerido (graduado)
> Nunca dar el Dockerfile de referencia antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Mira el orden de tus instrucciones: ¿qué tiene que rehacer Docker si cambias una línea de `main.py`? Ubica la frontera entre 'lo que cambia poco' y 'lo que cambia mucho'."
- **Pregunta socrática (nivel 2):** "Si el runtime hereda del builder con `COPY --from`, ¿qué cosas del builder NO estás copiando, y por qué eso es bueno para el tamaño *y* para la seguridad a la vez?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El patrón a corregir es el orden de capas: copia e instala el manifiesto (`requirements.txt`) **antes** de copiar `./app`. Reescribe esas tres líneas y vuelve a razonar qué capa reusa la caché."

## Conexión con el proyecto / capstone
- Esta imagen es la primera entrega del **[Capstone F5 — Pipeline a producción](/fase-5-devops/proyecto/)**: el CI/CD ([`5.3`](/fase-5-devops/5-3-cicd-github-actions/)) la construye y los gates de seguridad ([`5.4`](/fase-5-devops/5-4-seguridad-supply-chain-ci/)) la escanean. Una imagen mínima, pinneada y no-root reduce costo de build y hallazgos de seguridad aguas abajo.
