---
ejercicio_id: fase-8/comunicacion-rediseno-event-driven
fase: fase-8
sub_unidad: "8.4"
version: 1
---

# Rúbrica — Rediseña un flujo síncrono frágil a event-driven

> Rúbrica **analítica** para un ejercicio de **diseño**. Lo que se evalúa es el **criterio** (qué queda
> síncrono y qué pasa a evento, el trade-off de consistencia eventual en un ADR, y el blindaje de lo
> asíncrono), no una solución única. Caben variantes válidas (p. ej. un solo evento `UsuarioRegistrado` con
> cuatro consumidores, o eventos por capacidad) siempre que el razonamiento sea sólido.

## Objetivos evaluados
- **O1** — Separar el **corazón** (síncrono, consistente al instante) de los **reactores** (consumidores de
  un evento).
- **O2** — Articular el **trade-off** de la consistencia eventual en un ADR y **blindar** lo asíncrono
  (outbox contra dual write, idempotencia contra at-least-once).

## Criterios y niveles

### C1 — Corrección del rediseño (síncrono vs evento) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Deja todo síncrono, o mueve el **alta** a evento (rompe que la cuenta exista al responder), o no justifica por salto. |
| **en-progreso** | Mueve algunos reactores a evento pero deja uno acoplado sin razón (p. ej. CRM síncrono "por si acaso"), o no nombra la pregunta que manda. |
| **competente** | El alta queda síncrona; correo, CRM, cupón y analítica pasan a consumir un evento; cada decisión nombra la pregunta que manda. |
| **excelente** | Modela **un** evento `UsuarioRegistrado` con **fan-out** a consumidores independientes (no cuatro comandos acoplados al emisor), y nota que así un consumidor nuevo se suscribe sin tocar el registro. |

### C2 — Diagrama Mermaid · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay diagrama, o no renderiza, o no distingue síncrono de asíncrono. |
| **en-progreso** | Renderiza pero mezcla el alta con los reactores en una sola cadena (no se ve el desacoplamiento). |
| **competente** | Renderiza y muestra el salto síncrono (alta) separado del **fan-out por evento** a varios consumidores. |
| **excelente** | Muestra además el **broker/log** como intermediario y deja ver que los consumidores son independientes (la caída de uno no afecta a los otros ni al alta). |

### C3 — ADR y trade-off honesto · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay ADR, o solo vende ventajas ("event-driven es mejor") sin nombrar costo. |
| **en-progreso** | ADR con contexto y decisión, pero el trade-off es genérico ("es más complejo") sin nombrar qué se vuelve eventual ni qué riesgo se acepta. |
| **competente** | El ADR nombra al menos **una renuncia real** (correo/CRM/cupón dejan de ser inmediatos → consistencia eventual) **y** un **riesgo nuevo** (duplicado / orden / dual write). |
| **excelente** | Cuantifica la ventana ("convergen en ~segundos"), considera la UX honesta del retraso, y lista alternativas descartadas con su porqué. |

### C4 — Blindaje de lo asíncrono · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Publico el evento y ya"; no menciona dual write ni idempotencia. |
| **en-progreso** | Menciona idempotencia **o** outbox, pero no ambos, o sin explicar qué problema resuelve cada uno. |
| **competente** | Explica que el **dual write** (BD + publish no atómicos) se cubre con **outbox**, y que el **at-least-once** se cubre con **idempotencia** por `evento_id` en cada consumidor. |
| **excelente** | Añade el manejo de fallos del consumidor (reintentos + **DLQ**, de [7.2](/fase-7-automatizacion/7-2-integracion-confiabilidad/)) y/o el orden por clave si importa. |

## Errores típicos a marcar
- **Mover el alta a evento:** la cuenta debe existir cuando el registro responde; el alta es el corazón síncrono.
- **Cuatro comandos en vez de un evento:** modelar correo/CRM/cupón/analítica como comandos que el registro dispara uno a uno reacopla al emisor con cada consumidor; el punto del evento es que el emisor **no** los conozca.
- **ADR que solo vende:** sin nombrar la renuncia (consistencia eventual) ni el riesgo nuevo, no es un trade-off.
- **Ignorar el dual write:** asumir que "guardar en BD y publicar" es atómico; no lo es → outbox.
- **Olvidar idempotencia** pese a saber que la entrega es at-least-once → duplicados (correo doble, cupón doble).
- (transversal) **No instrumentar trazas:** sin correlation IDs, "¿dónde está mi evento?" es imposible de responder en producción.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diseño impecable con vocabulario avanzado (outbox, DLQ, KRaft) pero un ADR cuyo trade-off no calza con el diagrama (texto y dibujo no se hablan).
- ADR genérico que serviría para cualquier sistema (no menciona los pasos concretos: correo, CRM, cupón, analítica).
- **Verificación sugerida:** pídele que explique **qué pasa exactamente** si el evento se reentrega y el consumidor de cupón no fuera idempotente. Si entiende su propio diseño, describe el cupón duplicado; si no, generaliza.

## Feedback sugerido (graduado)
> Nunca dar la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Pregúntate, paso por paso: ¿qué debe ser verdad cuando el registro responde 200? Eso es el corazón síncrono. El resto, ¿alguien lo espera en línea?"
- **Pregunta socrática (nivel 2):** "Si el CRM se cae 10 minutos, ¿quieres que nadie pueda registrarse? Si la respuesta es no, ¿qué estilo de comunicación lo resuelve, y qué garantía cedes a cambio?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu ADR vende las ventajas; ahora nombra explícitamente qué deja de ser inmediato y un riesgo nuevo que aceptas. Y revisa: ¿cómo garantizas que el evento se publica si la BD ya hizo commit? (busca dual write / outbox)."

## Conexión con el proyecto / capstone
- Es el rediseño exacto que pide el [capstone F8](/fase-8-system-design/proyecto/): en la automatización de
  tickets con IA decides qué saltos son síncronos y cuáles eventos, y lo justificas en un ADR con su modelo
  de consistencia. Este ejercicio produce el ADR de muestra que reusarás allí.
