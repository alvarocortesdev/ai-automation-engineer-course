---
ejercicio_id: fase-8/monolito-vs-microservicios-diseno
fase: fase-8
sub_unidad: "8.3"
version: 1
---

# Rúbrica — Diseña los módulos de un monolito modular

> Rúbrica **analítica** para un ejercicio de **diseño**. Se evalúa la calidad de los **límites** (ownership
> de datos + APIs de dominio), la **honestidad del ADR** (¿nombra lo que renuncia?) y el **razonamiento**
> de la primera costura. No hay un único mapa de módulos correcto; hay diseños bien y mal acoplados.

## Objetivos evaluados
- **O1** — Límites de módulo con ownership de datos y APIs de dominio.
- **O2** — ADR que defiende monolito modular nombrando una renuncia real.
- **O3** — Primera costura justificada por bajo acoplamiento transaccional + gatillo observable.

## Criterios y niveles

### C1 — Ownership de datos y límites · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No asigna datos a módulos, o varios módulos comparten/cruzan tablas sin dueño (big ball of mud disfrazado). |
| **en-progreso** | Asigna datos pero con solapamientos ambiguos (dos módulos "dueños" de la misma tabla) o sin declarar la regla de no-cruce. |
| **competente** | Cada tabla tiene **un** dueño; el diseño declara que nadie lee las tablas de otro; las cinco áreas (tickets, clasificación, KB, notificaciones, reportes) están cubiertas. |
| **excelente** | Además resuelve bien el caso difícil de **reportes** (que necesita datos de varios módulos): vía API/eventos/vista de solo-lectura, no leyendo tablas ajenas. |

### C2 — Calidad de las APIs internas · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay APIs, o son getters de tablas (`get_tickets_row`). |
| **en-progreso** | APIs presentes pero anémicas / con fuga de detalles de almacenamiento. |
| **competente** | Cada módulo expone funciones con **nombre de dominio** (`kb.sugerir_articulos(categoria)`, `notificaciones.enviar(...)`), no acceso a filas. |
| **excelente** | Las APIs están pensadas para sobrevivir a una extracción futura (la firma no cambiaría si el módulo pasara a servicio; solo la implementación). |

### C3 — Diagrama Mermaid · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay diagrama o no renderiza. |
| **en-progreso** | Renderiza pero mezcla flechas de "llamada a API" con "lee tabla de", o no distingue datos de llamadas. |
| **competente** | Renderiza; las flechas son llamadas entre APIs; cada módulo con sus propios datos. |
| **excelente** | El diagrama deja ver visualmente el módulo de bajo acoplamiento (pocas flechas entrantes/salientes) = la futura primera costura. |

### C4 — Honestidad del ADR · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay ADR, o solo vende ventajas ("monolito = simple, fin"). |
| **en-progreso** | ADR con contexto y decisión, pero sin renuncia explícita (trade-off ausente). |
| **competente** | ADR completo (contexto/decisión/alternativas/trade-off) que nombra **al menos una renuncia real** (escala independiente, aislamiento de fallas, o despliegue independiente). |
| **excelente** | Nombra cómo **mitiga** la renuncia (esquema por módulo, ownership, gatillo de extracción) y reconoce que la decisión es reversible/evolutiva. |

### C5 — Primera costura + gatillo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica costura, o elige el módulo del corazón transaccional (tickets) sin justificar. |
| **en-progreso** | Elige un módulo razonable pero el gatillo es vago ("cuando crezca"). |
| **competente** | Elige un módulo de **bajo acoplamiento transaccional** (notificaciones o reportes) y da un gatillo **observable**. |
| **excelente** | Justifica con el patrón fire-and-forget / lectura agregada, define gatillo medible y esboza una extracción incremental (Strangler Fig). |

## Errores típicos a marcar
- **Reportes leyendo tablas de todos los módulos:** el error de ownership más común. Debe consumir APIs,
  eventos, o una vista/réplica de solo lectura — no `SELECT` directo a tablas ajenas.
- **APIs que son getters de filas** (`obtener_ticket_row`) en vez de operaciones de dominio: filtran el
  esquema y rompen la extracción futura.
- **Elegir `tickets` como primera costura:** está en el centro transaccional (todo depende de él) → es el
  más difícil de extraer, no el más fácil.
- **ADR que solo lista ventajas:** sin una renuncia nombrada no es un trade-off, es marketing.
- **Gatillo no observable:** "cuando sea grande". Pedir métrica o evento (volumen de notificaciones, SLA
  de reportes, un equipo dedicado, etc.).
- (transversal, observabilidad) No mencionar que al extraer un servicio aparece la necesidad de trazas
  distribuidas / correlation IDs.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Mapa de módulos "de libro" y simétrico, pero con el módulo de reportes resuelto mágicamente sin decir de
  dónde saca los datos (la parte difícil esquivada).
- ADR pulido en forma pero sin una renuncia concreta y específica de **este** sistema/equipo.
- Diagrama elaborado que no concuerda con el ownership descrito en la Parte 1 (señal de partes generadas
  por separado sin integrarlas).
- **Verificación sugerida:** pídele que explique, sin notas, **cómo cambiaría la firma de una de sus APIs
  internas** si ese módulo se extrajera a servicio. Si diseñó pensando en la extracción, dice "no cambia,
  solo la implementación"; si no, improvisa.

## Feedback sugerido (graduado)
> Nunca dar el diseño completo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Empieza por el módulo de **reportes**: necesita datos de varios otros. Si lo
  resuelves leyendo sus tablas, rompiste el ownership. ¿Cómo se entera reportes sin tocar tablas ajenas?"
- **Pregunta socrática (nivel 2):** "De tus cinco módulos, ¿cuál tiene menos flechas que entran y salen?
  ¿Cuál participa en transacciones que abarcan a otros y cuál solo recibe avisos? Esa diferencia te dice
  cuál se extrae fácil."
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa que cada API tenga nombre de dominio,
  no de tabla, y que tu ADR diga explícitamente qué renuncias (escala/aislamiento/despliegue
  independiente). La primera costura es el módulo fire-and-forget (notificaciones) o el de solo-lectura
  agregada (reportes), nunca el corazón transaccional (tickets)."

## Conexión con el proyecto / capstone
- Este es el esqueleto de los diagramas del [capstone F8](/fase-8-system-design/proyecto/): mapa de
  módulos con ownership + ADR de la decisión de arquitectura. Diseñar la "primera costura" es justo el
  razonamiento que distingue un diagrama estático de uno que muestra **cómo evolucionaría** el sistema.
