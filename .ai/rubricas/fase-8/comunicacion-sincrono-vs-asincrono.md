---
ejercicio_id: fase-8/comunicacion-sincrono-vs-asincrono
fase: fase-8
sub_unidad: "8.4"
version: 1
---

# Rúbrica — Decisor: ¿llamada síncrona o evento asíncrono?

> Rúbrica **analítica** para un ejercicio de **razonamiento**. Lo que se evalúa es el **criterio de
> decisión** (la pregunta que manda, comando vs evento, el modelo de consistencia y el trade-off), no si el
> alumno coincidió con una respuesta única. Los saltos 1–5 tienen una respuesta claramente mejor; el
> **salto 6 admite ambas** decisiones si están bien defendidas. Un alumno puede acertar "por moda" y seguir
> sin entender; otro puede defender la opción menos común con un trade-off impecable. La rúbrica distingue
> ambos casos.

## Objetivos evaluados
- **O1** — Decidir síncrono vs asíncrono por salto nombrando la **pregunta que manda**.
- **O2** — Clasificar asíncronos como **comando/evento**, nombrar **consistencia eventual** y una **anomalía**
  a mitigar.

## Criterios y niveles

### C1 — Corrección de las decisiones 1–5 · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan saltos, o las decisiones contradicen la pregunta que manda (p. ej. fraude o precio por evento asíncrono "porque desacopla", cuando el flujo necesita la respuesta para continuar). |
| **en-progreso** | Acierta 2–3, pero justifica con motivos genéricos ("más moderno", "más rápido", "escala mejor") en vez de "¿necesita la respuesta para continuar?". |
| **competente** | Acierta los cinco (1→síncrono, 2→evento, 3→asíncrono, 4→síncrono, 5→evento) y nombra la pregunta que manda en cada uno. |
| **excelente** | Además nota que 1 y 4 comparten "el flujo necesita el dato ahora" (consulta → síncrono) y que 2, 3 y 5 comparten "nadie lo espera en línea / aislar fallas" (reactores → asíncrono). |

### C2 — Comando vs evento + consistencia/anomalía · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No clasifica comando/evento, o no nombra consistencia ni anomalías; las decisiones son afirmaciones sin consecuencia. |
| **en-progreso** | Clasifica algunos comando/evento pero confunde casos (p. ej. "usuario registrado" como comando), o nombra anomalías vagas ("puede fallar"). |
| **competente** | Distingue comando (un destinatario que ejecuta, p. ej. "generar factura") de evento (hecho que varios observan, p. ej. "usuario registrado"), nombra **consistencia eventual** en los asíncronos y **una anomalía concreta** (duplicado/orden/read-your-writes) con mitigación. |
| **excelente** | Liga el **at-least-once** a la necesidad de **idempotencia**, y reconoce que el fan-out del salto 5 es el caso canónico de evento (varios consumidores sin que el emisor los conozca). |

### C3 — Calidad del trade-off en el caso 6 (juicio) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Esquiva el caso 6, o decide sin defender contra la alternativa. |
| **en-progreso** | Decide y da una fuerza a favor, pero no nombra qué renuncia / qué riesgo acepta. |
| **competente** | Decide, da una fuerza a favor **y** una en contra, y nombra el desempate (¿la consistencia inmediata es un requisito real del usuario o un lujo? ¿la compensación posterior es aceptable para el negocio?). |
| **excelente** | Reconoce que la opción síncrona da certeza inmediata de stock pero acopla el checkout a `Inventario`; la opción evento + compensación desacopla pero introduce una ventana donde un pedido "confirmado" puede cancelarse después (UX honesta). Cualquiera de las dos, con el trade-off nombrado, es excelente. |

## Errores típicos a marcar
- **"Asíncrono = más rápido"** como justificación: asíncrono mueve el trabajo fuera del camino crítico, no lo acelera; baja la latencia *del que llama*, no el cómputo total.
- **Confundir comando con evento:** "usuario registrado" es un hecho (evento, broadcast); "generar factura" tiene un responsable (comando). Modelar un evento como comando a un solo destino mata el desacoplamiento.
- **Hacer asíncrono lo que el flujo necesita ya** (fraude, precio): el checkout no puede continuar sin el veredicto; la página no puede mostrar sin el precio.
- **No nombrar la consistencia eventual ni una anomalía** en los asíncronos: señal de que no vio el costo del desacoplamiento.
- **Decidir el caso 6 por reflejo** sin nombrar qué renuncia (no es trade-off, es preferencia).
- (transversal) **Olvidar idempotencia** pese a mencionar at-least-once.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Seis decisiones "correctas" con justificaciones genéricas idénticas en estructura, sin la pregunta que manda específica de cada caso (texto plausible pero intercambiable).
- El caso 6 resuelto con una respuesta tajante y sin trade-off, como si tuviera respuesta única.
- Vocabulario (saga, outbox, at-least-once) usado sin poder explicarlo si se le pregunta.
- **Verificación sugerida:** pídele que invente un **séptimo salto** propio donde la decisión correcta sea la menos intuitiva, y que lo defienda. Si razonó de verdad, lo construye; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar las respuestas antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada salto, hazte la única pregunta de la sección 4.5: ¿el que llama **necesita** la respuesta para continuar su propia operación? Marca sí/no antes de decidir nada más."
- **Pregunta socrática (nivel 2):** "En el salto 5, ¿el que registra al usuario **conoce** a todos los que deben reaccionar, o solo sabe que 'pasó un registro'? ¿Qué te dice eso sobre comando vs evento?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa que cada salto asíncrono nombre la consistencia eventual **y** una anomalía concreta con mitigación. Y en el caso 6, nombra qué renuncias con la opción que elegiste: sin eso no es trade-off."

## Conexión con el proyecto / capstone
- Es el músculo exacto del [capstone F8](/fase-8-system-design/proyecto/): en la automatización de tickets
  con IA y en el pipeline de datos, cada salto de comunicación debe decidirse síncrono vs evento y quedar
  justificado en un ADR con su modelo de consistencia. Este ejercicio entrena esa decisión en frío.
