---
ejercicio_id: fase-5/exponer-homelab-cloudflare-tunnel
fase: fase-5
sub_unidad: "5.9"
version: 1
---

# Rúbrica — Expón tu API del homelab con Cloudflare Tunnel

> Rúbrica **analítica** para un ejercicio de **código** (un `docker-compose.yml`). Los tests (`test_despliegue.py`) son un piso objetivo: si pasan, las decisiones de seguridad están. Pero la rúbrica mira más allá del verde —¿entiende **por qué** cada decisión, o solo acertó a que el lint pasara?

## Objetivos evaluados
- **O1** — Exponer el servicio con Cloudflare Tunnel sin abrir puertos del router.
- **O2** — Mantener el backend con exposición mínima (`expose`, no `ports`).
- **O3** — Inyectar el token del túnel desde el entorno, sin hardcodearlo ni commitearlo.

> El corrector puede correr `pytest` para el piso objetivo; la solución de referencia está en `.ai/soluciones/fase-5/exponer-homelab-cloudflare-tunnel.md`. **No se la muestra al alumno.**

## Criterios y niveles

### C1 — Corrección (¿el Compose hace lo que el objetivo pide?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan servicios, o el Compose no corre `cloudflared tunnel ... run`; tests en rojo masivo. |
| **en-progreso** | Define ambos servicios y el túnel corre, pero publica el puerto del backend al host (`ports`) o le falta `expose`. |
| **competente** | `pytest` en verde: `api` con `expose`, `cloudflared` corriendo el túnel por token, ningún puerto publicado al host. |
| **excelente** | Además, comentarios que explican *por qué* (no qué) por servicio; nombra que el túnel es saliente y que el TLS se termina en el edge. |

### C2 — Seguridad (mínima exposición + gestión de secretos) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Token hardcodeado en el archivo, o `.env` sin ignorar, o backend publicado a internet. |
| **en-progreso** | Token por entorno pero deja un `ports:` innecesario, o no incluye `.env.example`/`.gitignore`. |
| **competente** | Token vía `${CF_TUNNEL_TOKEN}`; `.env` ignorado; `.env.example` documenta la clave; cero puertos al host. |
| **excelente** | Articula la defensa en profundidad: conexión saliente (sin puertos de entrada) + secreto fuera del repo + backend solo interno; compara con abrir el 443 del router. |

### C3 — Comprensión demostrada (el porqué calza con el Compose) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin comentarios, o comentarios que solo repiten el comando. |
| **en-progreso** | Comentarios de "qué" pero no de "por qué" (no explica `expose` vs `ports`, ni por qué el túnel no abre puertos). |
| **competente** | Un comentario de *por qué* por servicio; explica `expose` vs `ports` y la conexión saliente. |
| **excelente** | Puede defender, sin notas, por qué el túnel es más seguro que abrir el router y dónde se termina el TLS. |

## Errores típicos a marcar
- **Publicar el backend al host** (`ports: - "8000:8000"`): lo expone directo a internet; en este diseño el único que debe llegarle es el túnel (`expose`).
- **Token hardcodeado** en el `command`: un secreto en el repo está comprometido para siempre, aunque luego se borre.
- **Commitear el `.env`** o no incluir `.env.example`/`.gitignore`.
- **Abrir un `ports:` en `cloudflared`**: el túnel es saliente, no necesita puertos de entrada.
- **Olvidar `restart: unless-stopped`**: el homelab se reinicia y la app no vuelve sola.
- (transversales) confiar en que "pasa el lint" sin entender el porqué; no registrar la decisión (ADR/comentario); ignorar el costo (el túnel + homelab es la opción de ~$0).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Compose impecable con flags exóticos (healthchecks, redes nombradas, labels de más) que el alumno no puede explicar: sofisticación impropia del ejercicio.
- Comentarios genéricos copiados ("runs the cloudflare tunnel") que no mencionan `expose`/saliente/edge.
- Pasa los tests pero no puede decir **por qué** `expose` y no `ports`.
- **Verificación sugerida:** pídele que explique qué cambiaría si tuviera que exponer **dos** servicios (api + un panel) por el mismo túnel, o por qué el `command` no lleva el token literal. Si razonó, responde; si copió, se traba.

## Feedback sugerido (graduado)
> Nunca pegar el `docker-compose.yml` de referencia antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Mira los tests en rojo de a uno: cada uno apunta a una decisión (imagen, comando del túnel, token, `expose`, `restart`). Empieza por el del token."
- **Pregunta socrática (nivel 2):** "¿Cuál es la diferencia entre `expose` y `ports`? Si el túnel es una conexión **saliente**, ¿qué puerto de entrada necesitas abrir? ¿Dónde debería vivir el token para no terminar en el repo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El backend va con `expose` (solo red interna); ningún servicio lleva `ports:` (el túnel es saliente). El conector corre `tunnel --no-autoupdate run --token ${CF_TUNNEL_TOKEN}` con el token del `.env`. Revisa la sección 4.4 y ajusta."

## Conexión con el proyecto / capstone
- Es una de las dos rutas concretas para poner el backend del [Capstone F5](/fase-5-devops/proyecto/) online con dominio y ≥3 usuarios **sin pagar cloud ni exponer la red de casa** — y el entregable de seguridad "ni un puerto de más, ni un secreto en el repo" del Definition of Done de la fase.
