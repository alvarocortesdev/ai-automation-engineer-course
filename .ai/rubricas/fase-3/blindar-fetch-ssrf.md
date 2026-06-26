---
ejercicio_id: fase-3/blindar-fetch-ssrf
fase: fase-3
sub_unidad: "3.13"
version: 1
---

# Rúbrica — Blinda un fetch saliente contra SSRF

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `guardia_ssrf.py` + `bitacora.md`
> con `test_guardia_ssrf.py` en verde. El test cubre esquemas, IPs literales peligrosas,
> host público y DNS rebinding. La bitácora prueba que el alumno entiende por qué una
> lista negra de strings no basta.

## Objetivos evaluados
- **O1** — Guardia anti-SSRF que valida esquema, resuelve DNS y rechaza rangos privados/loopback/link-local.
- **O2** — Revisar todas las IPs resueltas (DNS rebinding) y explicar por qué la lista negra de strings falla.
- **O3** — Explicar por qué SSRF es crítico en un agente de IA que hace fetch.

## Criterios y niveles

### C1 — Corrección del guardia · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `validar_destino` sin implementar o solo cubre algún caso; varios tests en rojo. |
| **en-progreso** | Bloquea esquemas e IPs literales, pero no resuelve el DNS (deja pasar un host que resuelve a privada) o solo mira la primera IP (falla el rebinding). |
| **competente** | Los tests en **verde**: bloquea file/ftp/sin-host, loopback, metadatos, privada, unspecified y rebinding; acepta el host público. |
| **excelente** | Verde + maneja `socket.gaierror` como bloqueo, mensajes de error claros por causa, y nota en la bitácora las defensas extra (redirects, timeouts, conectar a la IP validada). |

### C2 — Defensa real, no cosmética · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Compara el string del host contra `"localhost"`/`"127.0.0.1"` (lista negra de texto). |
| **en-progreso** | Resuelve pero valida solo `infos[0]`, dejando la puerta al rebinding. |
| **competente** | Itera todas las entradas de `getaddrinfo` y bloquea si alguna IP es peligrosa. |
| **excelente** | Explica por qué resolver-y-validar-todas cierra el rebinding y por qué `169.254.169.254` (link-local) es el objetivo clásico (metadatos de la nube). |

### C3 — Comprensión + conexión con IA (bitácora) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay bitácora o no explica el riesgo en agentes de IA. |
| **en-progreso** | Explica SSRF en general pero no lo aterriza en una herramienta `leer_url` de un agente. |
| **competente** | Responde las tres preguntas: por qué la lista negra de strings falla, por qué revisar todas las IPs, y el riesgo en un agente que navega. |
| **excelente** | Conecta con prompt injection (Fase 6): una URL envenenada por el LLM dispara el fetch interno; el guardia va ANTES del fetch, no después. |

## Errores típicos a marcar
- **Lista negra de strings** (`if "localhost" in url`): se evade con `127.0.0.1`, `0.0.0.0`, forma decimal, o un dominio que resuelve a privada. Hay que resolver y validar la IP.
- **Validar solo la primera IP resuelta**: deja pasar DNS rebinding. El test lo caza.
- **No bloquear `file://`/`ftp://`**: la lista blanca de esquemas es la primera línea.
- **"Sanitizar" la respuesta después del fetch** en vez de validar el destino antes: la petición interna ya se hizo.
- **Confiar en que el LLM no pedirá URLs peligrosas**: eso es prompt injection esperando a ocurrir.
- (transversal costo/latencia) no mencionar timeouts/límite de tamaño: un fetch sin techo es también un riesgo de consumo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución que importa una librería externa de "anti-SSRF" sin entender qué valida: no demuestra el razonamiento del rango de IP.
- Código correcto pero `bitacora.md` que no explica por qué la lista negra de strings falla.
- No sabe decir qué es `169.254.169.254` ni por qué importa.
- **Verificación sugerida:** pídele que prediga qué pasa con `http://interno.miempresa.cl` que resuelve a `10.0.0.5` (debe bloquear) y por qué; y qué evade una lista negra de `"localhost"`.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de `validar_destino` antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Corre `test_host_que_resuelve_a_privada_bloqueado`. Si pasa un host que resuelve a `10.0.0.5`, ¿estás mirando el string del host o la IP a la que resuelve?"
- **Pregunta socrática (nivel 2):** "Si un atacante controla el DNS y hace que su dominio devuelva dos IPs (una pública y una privada), ¿cuántas IPs tienes que revisar para estar seguro?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Orden: parsea, chequea esquema, saca host, `resolver(host, port or 80)`, itera `info[4][0]` y bloquea si `_es_ip_peligrosa`. Envuelve la resolución en try/except `socket.gaierror`. Repasa 4.4."

## Conexión con el proyecto / capstone
- En el capstone, cualquier fetch saliente pasa por este guardia. Se vuelve obligatorio en la Fase 6/7 cuando un agente de IA recibe URLs: el guardia va antes de cada llamada de la herramienta, parte del least-privilege y la validación de I/O del Definition of Done.
