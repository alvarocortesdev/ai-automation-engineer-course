---
ejercicio_id: fase-2/patrones-adapter-notificaciones
fase: fase-2
sub_unidad: "2.5"
version: 1
---

# Rúbrica — Integra dos terceros con Adapter (y prueba Open/Closed)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa no es "¿pasó pytest?": es si el
> alumno entendió que **un Adapter traduce por composición** (el extraño se dobla a tu contrato, no al revés) y
> si su segundo adapter prueba **Open/Closed de verdad** (negocio intacto). Un alumno puede tener verde
> habiendo tocado el código de negocio; otro puede tener un diseño limpio sin entender por qué. La rúbrica los
> distingue.

## Objetivos evaluados
- **O1** — Implementar Adapter: hacer que una interfaz de terceros incompatible satisfaga el contrato `Notificador`, traduciendo por composición sin tocar el negocio.
- **O2** — Demostrar Open/Closed agregando un segundo proveedor como clase nueva, sin editar el adapter existente ni el negocio.
- **O3** — Reconocer el smell "interfaz incompatible" y justificar por qué el que se adapta es el extraño.

> Resultado esperado: con `SmsAdapter` + `EmailAdapter` correctos, `pytest` pasa los 2 tests de SMS dados + el
> test de email que el alumno agrega. El corrector lo sabe; **no se lo dice al alumno** como atajo que evite el razonamiento.

## Criterios y niveles

### C1 — Corrección: el Adapter traduce bien · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Los tests de SMS no pasan, o el alumno **modificó `enviar_alerta` / el contrato `Notificador`** (cambió el dominio en vez de adaptar el extraño). |
| **en-progreso** | Pasa, pero pierde o renombra datos en la traducción (p. ej. olvida `sender`, invierte argumentos), o el adapter **hereda** de la librería de terceros en vez de **componer** (guardarla en `__init__`). |
| **competente** | `SmsAdapter` cumple `enviar(destino, mensaje)` por fuera y llama `send_text(destino, mensaje, sender=...)` por dentro; los 2 tests de SMS pasan **sin tocar** negocio ni contrato. |
| **excelente** | Además razona/maneja la **falla del tercero** (qué pasa si `send_text` lanza): no propaga a ciegas la excepción del extraño (hilo seguridad/frontera). `Protocol` respetado; nombres limpios. |

### C2 — Open/Closed: extensión sin modificación · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó `EmailAdapter`, o para integrarlo **editó** `SmsAdapter` o `enviar_alerta`. |
| **en-progreso** | Agregó `EmailAdapter` pero con un payload incorrecto para `dispatch` (claves mal: no usa recipient/subject/html), o no agregó su test. |
| **competente** | `EmailAdapter` es una **clase nueva** que compone `ClienteEmailV2` y arma el payload correcto; su test verde demuestra que `enviar_alerta` funciona con él **sin que el negocio cambiara**. |
| **excelente** | Articula que esto **es** Open/Closed ("agregar un proveedor no reabrió código probado") y que migrar de proveedor es cambiar qué adapter se inyecta, no editar el dominio. |

### C3 — Comprensión demostrada (write-up / explicación) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar "quién se adapta a quién", o la explicación no calza con el código (p. ej. dice "adapté mi negocio"). |
| **en-progreso** | Explica "hice una clase que llama a la librería" sin conectar con el smell (interfaz incompatible) ni con el desacople del dominio. |
| **competente** | Explica con precisión que el extraño se dobla al contrato, que el dominio nunca importa la librería, y qué cambiaría para migrar de proveedor. |
| **excelente** | Conecta el Adapter con la frontera de validación (envolver un LLM en Fase 6: validar la salida antes de que entre al dominio) y/o con ports & adapters de Fase 3. |

## Errores típicos a marcar
- **Adaptar el dominio en vez del extraño:** cambiar `enviar_alerta` o el contrato `Notificador` para que "encaje" con la librería. Es exactamente al revés: el que se adapta es el tercero.
- **Herencia en vez de composición:** `class SmsAdapter(GatewaySmsLegacy)`. Un Adapter **contiene** al adaptado (lo recibe en `__init__`), no hereda de él —heredar acopla a su interfaz interna y rompe la traducción.
- **Perder datos en la traducción:** olvidar `sender`, mapear mal las claves del payload de email (no usar recipient/subject/html), invertir `destino`/`mensaje`.
- **El negocio importa la librería:** que `enviar_alerta` (o cualquier código de dominio) conozca `GatewaySmsLegacy`. El objetivo entero es que NO la conozca.
- **Propagar la falla del tercero a ciegas:** dejar que una excepción de `send_text` suba sin control desde la frontera (anótalo como mejora de seguridad/robustez, hilo transversal).
- (transversales) confiar en que "pasa pytest" sin revisar que el payload/orden de argumentos sea correcto; no agregar el test de email propio.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Adapter con manejo de errores sofisticado, reintentos o logging estructurado **impropio del enunciado** que el alumno no puede explicar línea a línea.
- El código está impecable pero el alumno no sabe decir **quién se adapta a quién** ni por qué el dominio no debe importar la librería.
- Usa el término "Adapter" correctamente pero no puede justificar por qué no se resuelve con herencia.
- **Verificación sugerida:** pedir que integre **en vivo** un tercer proveedor `ClientePushV3.notify(device_id, text)` y explique qué archivos toca y cuáles NO. Si entendió Adapter, escribe una clase nueva y no toca el negocio; si dependió de la IA, duda o edita el dominio.

## Feedback sugerido (graduado)
> Nunca pegar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Quién está cambiando para encajar: tu negocio o la librería de terceros? Si editaste `enviar_alerta`, vas en la dirección contraria —el que se adapta es el extraño."
- **Pregunta socrática (nivel 2):** "Tu `SmsAdapter`, ¿hereda de `GatewaySmsLegacy` o lo **contiene**? Si la librería cambiara un método interno mañana, ¿cuál de las dos opciones te rompería menos?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Guarda el gateway en `__init__` (composición) y en `enviar(destino, mensaje)` llama `self._gateway.send_text(destino, mensaje, sender=self._remitente)`: tradúce nombres y orden, no reimplementes el envío. Para email, arma el `dict` con las claves que `dispatch` espera. Vuelve a correr los tests sin tocar el negocio."

## Conexión con el proyecto / capstone
- Es el ensayo directo del **Capstone F2 — Refactor + suite de tests**: aislar una dependencia de terceros detrás de un contrato propio, con tests que prueban la traducción. Es además la forma exacta en que envolverás un cliente de LLM en la Fase 6 (la frontera donde validas su salida) y la semilla de ports & adapters de la Fase 3.
