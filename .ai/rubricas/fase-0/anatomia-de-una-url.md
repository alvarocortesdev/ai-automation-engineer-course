---
ejercicio_id: fase-0/anatomia-de-una-url
fase: fase-0
sub_unidad: "0.4"
version: 1
---

# Rúbrica — Anatomía de una URL y su viaje

> Rúbrica analítica para un ejercicio **a-mano**. Se evalúa el **modelo mental**: el orden del viaje y el *porqué* de cada paso, no si el alumno memorizó una lista. Un recorrido con los pasos correctos pero sin justificar (p. ej. "TLS" puesto en cualquier lado) vale menos que uno que explica por qué TLS va **después** de TCP. El corrector evalúa contra los `objetivos` del contrato.

## Objetivos evaluados
- **O1** — Descomponer la URL en sus partes, con puerto efectivo justificado.
- **O2** — Predecir el recorrido (DNS → IP → TCP → TLS → HTTP → render) en orden, sin ejecutar.
- **O3** — Identificar qué parte de la URL no viaja al servidor y por qué.

## Criterios y niveles

### C1 — Descomposición de la URL · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan partes presentes en la URL, o confunde categorías (mete la query dentro de la ruta, o el host incluye el esquema). |
| **en-progreso** | Identifica las partes principales pero no justifica el **puerto efectivo** (lo deja en blanco o pone 80 para un `https`). |
| **competente** | Todas las partes presentes correctamente separadas; puerto efectivo correcto (443 para `https`, 80 para `http`) **con** la razón. |
| **excelente** | Además explica que la query es para el servidor y el fragmento para el navegador, y nota detalles (codificación de la query, múltiples pares `clave=valor`). |

### C2 — Recorrido y orden causal · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay recorrido, o salta del navegador al "se conecta a internet" sin nombrar piezas. |
| **en-progreso** | Nombra las piezas (DNS, TCP, TLS, HTTP) pero en **orden incorrecto** o sin dependencia causal (TLS antes de TCP, HTTP antes de resolver DNS). |
| **competente** | Orden correcto: parse → DNS → TCP → TLS → HTTP request → response → render. Cada paso nombra su pieza. |
| **excelente** | Justifica la **dependencia** ("no puedo cifrar sin canal TCP", "no hablo HTTP hasta tener TLS en `https`") y menciona caché DNS/TTL o que cada subrecurso repite el ciclo (latencia). |

### C3 — Qué no viaja al servidor (precisión conceptual) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No responde, o dice que "todo viaja". |
| **en-progreso** | Identifica el fragmento `#...` pero la razón es vaga ("no es importante"). |
| **competente** | El fragmento no se envía **porque** ubica una sección dentro de la página ya descargada; lo resuelve el navegador. |
| **excelente** | Además contrasta con la query (que **sí** viaja porque el servidor la necesita para decidir qué devolver) y nota que en `https` el resto de la URL viaja **cifrado**, no en claro. |

## Errores típicos a marcar
- **Puerto = parte del dominio:** tratar `:443` como parte del host en vez de selector de servicio.
- **Orden invertido TCP/TLS:** poner el cifrado antes del canal, o hablar HTTP antes de resolver DNS.
- **"DNS es el servidor web":** confundir el sistema de nombres con el servidor de la app.
- **El fragmento viaja:** afirmar que `#seccion` llega al servidor.
- **Recorrido sin causalidad:** lista de palabras correctas (DNS, TCP, TLS) sin explicar por qué ese orden — señal de memorización, no de modelo.
- (transversal costo/latencia) no notar que cada subrecurso repite request/response y que las idas y vueltas suman latencia.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Recorrido impecablemente fraseado pero que no calza con la URL concreta elegida (texto genérico copiado).
- Usa términos avanzados (handshake, MTU, OCSP) sin poder explicar los básicos cuando se le pregunta.
- La tabla de descomposición no corresponde a la URL pegada arriba (señal de plantilla rellenada por IA).
- **Verificación sugerida:** pedir que, sin notas, prediga qué cambia en el recorrido si la URL fuera `http://` en vez de `https://` (debe desaparecer el paso TLS) y por qué la cámara del navegador no funcionaría ahí.

## Feedback sugerido (graduado)
> Nunca dar el recorrido completo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Revisa el orden de tus pasos 2–4: ¿puedes cifrar un canal que todavía no abriste? ¿puedes abrir un canal a un nombre o necesitas un número?"
- **Pregunta socrática (nivel 2):** "¿Qué necesita *tener* el navegador antes de poder hacer cada paso? Si respondes eso, el orden se ordena solo. Y sobre el fragmento: ¿para qué sirve `#...` una vez que la página ya está cargada?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a fijar es la **cadena de dependencias**: nombre→IP (DNS), IP→canal (TCP), canal→cifrado (TLS, solo en https), cifrado→pregunta (HTTP). Reescribe el recorrido explicando en cada paso qué habilita el anterior."

## Conexión con el proyecto / capstone
- Este modelo es lo que permite que el **Capstone F0 — CLI sin IA** construya URLs correctas y elija bien el esquema/puerto al hablar con una API. Sin él, el CLI explota ante el primer redirect o el primer `https`.
