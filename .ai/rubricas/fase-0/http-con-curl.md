---
ejercicio_id: fase-0/http-con-curl
fase: fase-0
sub_unidad: "0.4"
version: 1
---

# Rúbrica — Inspecciona HTTP real con `curl`

> Rúbrica analítica para un ejercicio **mixto** (terminal + escritura). Se evalúa la **lectura e interpretación** de HTTP real, no si pegó salidas. Un informe lleno de outputs sin conclusión vale menos que uno con menos capturas pero diagnósticos correctos. El corrector evalúa contra los `objetivos` del contrato. Como las respuestas dependen de sitios vivos, **no** hay un status único esperado por caso: se evalúa que la **clasificación y el diagnóstico** sean coherentes con la salida pegada.

## Objetivos evaluados
- **O1** — Capturar respuestas reales y clasificar el status por familia.
- **O2** — Leer headers (content-type, location) y detectar TLS.
- **O3** — Diagnosticar cliente (`4xx`) vs servidor (`5xx`) con evidencia.

## Criterios y niveles

### C1 — Captura y clasificación de status · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan casos, o pega salidas sin identificar el status, o inventa códigos que no aparecen en su propia salida. |
| **en-progreso** | Captura los casos pero clasifica mal alguna familia (llama "error" a un `3xx`, o cree que `404` es del servidor). |
| **competente** | Los cuatro casos capturados; cada status correctamente ubicado en su familia con su significado. |
| **excelente** | Además **predijo** el status antes de correr (visible en el informe) y acertó/diagnosticó su error de predicción; usa los flags con criterio (`-I` vs `GET`, `--max-time`). |

### C2 — Lectura de headers y detección de TLS · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona headers, o no encuentra el `location` en la redirección, o no ubica el TLS. |
| **en-progreso** | Lee `content-type`/`content-length` pero no conecta el `location` con "a dónde redirige", o confunde el handshake TLS con otra cosa. |
| **competente** | Identifica `content-type`, el `location` de la redirección, y señala las líneas del handshake TLS en `-v`. |
| **excelente** | Explica **por qué** `-L` cambia el status final (sigue la cadena hasta un `2xx`) y articula qué garantiza TLS (canal cifrado, certificado de identidad). |

### C3 — Diagnóstico cliente vs servidor · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue `4xx` de `5xx`, o dice que `4xx` significa "servidor caído". |
| **en-progreso** | Da la regla (`4xx`=cliente, `5xx`=servidor) pero sin ejemplo o sin ligarla a la evidencia capturada. |
| **competente** | Distingue ambas familias con un ejemplo de cada una y lo conecta con lo que vería en `curl`. |
| **excelente** | Nota el matiz: un `5xx` puede venir de un **proxy** delante (`502/504`) aunque la app de atrás no respondió; un `404` es respuesta **exitosa** del servidor. (Observabilidad: leer la evidencia antes de concluir.) |

## Errores típicos a marcar
- **"`404` = servidor caído":** confundir error de cliente con caída del servicio. El servidor respondió.
- **Confundir `3xx` con error:** una redirección es comportamiento normal, no un fallo.
- **No encontrar `location`:** buscarlo en respuestas que no son `3xx`.
- **`https` "más seguro" sin saber qué cifra:** afirmar seguridad sin señalar el handshake ni qué protege (canal completo, no solo el login).
- **Pegar salida sin conclusión:** outputs crudos sin interpretarlos — no demuestra el objetivo.
- **No predecir antes de correr:** salta el "Primero" del Primero-Sin-IA; el valor está en predecir y contrastar.
- (transversal observabilidad) concluir sin evidencia: afirmar un diagnóstico que la salida pegada no respalda.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Interpretaciones perfectas de headers que **no aparecen** en la salida pegada (la IA describió un caso genérico, no el real).
- Predicciones ausentes o todas "correctas" sin un solo error — sospechoso en un primer intento real.
- Lenguaje de RFC (negociación de contenido, ALPN, OCSP stapling) sin poder explicar qué es un `404`.
- **Verificación sugerida:** pedir que, mirando una captura nueva (p. ej. un `301` con su `location`), diga **sin IA** qué hará el navegador y qué status final espera tras seguirla. Si interpretó de verdad, lo resuelve.

## Feedback sugerido (graduado)
> Nunca interpretar las capturas por el alumno antes de que cierre su intento.
- **Pista (nivel 1):** "Mira otra vez la primera línea de cada respuesta: el primer dígito te dice la familia. ¿Tu `404` y tu `503` están en la misma familia? ¿Qué significa cada primer dígito?"
- **Pregunta socrática (nivel 2):** "En tu caso de redirección, ¿qué header te dice **a dónde** ir? ¿Por qué crees que el status cambió cuando agregaste `-L`? ¿Quién decide seguir la redirección, tú o el navegador?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Fija la regla de familias: `2xx` ok, `3xx` 've a otro lado' (con `location`), `4xx` tú te equivocaste, `5xx` el servidor falló. Reescribe cada conclusión empezando por la familia y luego el matiz (p. ej. `404` = recurso ausente, pero el servidor está vivo)."

## Conexión con el proyecto / capstone
- Leer status y headers es exactamente lo que tu **Capstone F0 — CLI sin IA** debe hacer para no caerse ante un `4xx`/`5xx`. Es la primera práctica de **observabilidad** del curso: diagnosticar mirando la evidencia, no adivinando.
