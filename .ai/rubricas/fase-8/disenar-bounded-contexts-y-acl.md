---
ejercicio_id: fase-8/disenar-bounded-contexts-y-acl
fase: fase-8
sub_unidad: "8.2"
version: 1
---

# Rúbrica — Diseñar bounded contexts + un anti-corruption layer

> Rúbrica **analítica** atada a los `objetivos`. **No hay respuesta correcta única.** Se evalúa
> si el alumno **trazó fronteras defendibles**, **diseñó una aduana que traduce Y valida**, y
> **defendió dónde DDD paga y dónde no** —no si coincidió con un diseño concreto. Este ejercicio
> **no se implementa**: si el alumno entregó código de la traducción, se desvió del objetivo.

## Objetivos evaluados
- **O1** — Context map con 2-3 bounded contexts y la **relación** entre ellos nombrada (no solo cajas).
- **O2** — ACL que **traduce** el modelo sucio del ERP al dominio propio y **valida** el input no confiable (frontera de seguridad).
- **O3** — ADR que pesa **ACL vs conformist** y un juicio defendible de **dónde DDD táctico paga vs over-engineering**.

## Criterios y niveles

### C1 — Calidad del context map · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Un solo "sistema" sin fronteras; o cajas conectadas sin nombrar la relación; sin Mermaid. |
| **en-progreso** | Identifica contexts pero no nombra la **relación** (upstream/downstream, customer-supplier, conformist, ACL), o la frontera con el ERP no se distingue de las internas. |
| **competente** | 2-3 contexts con fronteras claras en Mermaid; la relación con el ERP marcada como **upstream/downstream con ACL**; argumenta por qué (modelo ajeno + ya cambió). |
| **excelente** | Justifica una decisión no obvia (Clasificación-IA como context propio vs servicio dentro de Soporte) con criterio de "lenguaje ubicuo distinto"; nombra qué término significa cosas distintas en cada context. |

### C2 — Calidad del ACL: traduce Y valida · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Solo un mapper" que renombra campos; deja entrar el modelo sucio (string `bal`, `pay_st` numérico) al dominio; sin validación. |
| **en-progreso** | Traduce campos pero no define el **modelo limpio** con tipos propios (value objects), o no dice **qué rechaza** (el `pay_st: 4` mágico, `bal` no numérico). |
| **competente** | Modelo sucio → modelo limpio con value objects (`Dinero`, enum legible); traducción campo a campo; **valida y rechaza** lo desconocido; nombra que es frontera de **confianza/seguridad** (input externo no confiable). |
| **excelente** | Conecta con OWASP (validar en la frontera) y con Fase 7/IA (la salida del LLM y el dato externo son input no confiable que la aduana valida antes de actuar); explica que cambiar de ERP solo toca el ACL. |

### C3 — ADR + juicio DDD-sí / DDD-no · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin ADR, o con **una sola opción** (no hay decisión, hay capricho); no discute over-engineering. |
| **en-progreso** | ADR con estructura pero sin pro/contra reales de "conformist"; o el juicio dice "todo DDD" / "nada DDD" sin matiz. |
| **competente** | ADR con **≥2 opciones** (ACL vs conformist) con pro/contra, decisión atada al contexto y **gatillo**; el juicio nombra **una parte que merece DDD y una que no**, con razón. |
| **excelente** | El gatillo es concreto y medible (p. ej. "si el ERP se vuelve estable y propio, reconsiderar conformist"); el juicio distingue invariantes reales (estado de pago / regla de moroso) de CRUD plano (categorías de tickets) con criterio transferible. |

## Errores típicos a marcar
- **ACL tratado como "solo un mapper"**: renombra campos pero no valida ni define tipos de dominio; el modelo sucio se cuela igual.
- **Dejar entrar tipos crudos**: `bal` como string, `pay_st` como int al dominio → no se tradujo, se conformó.
- **No rechazar lo desconocido**: ignorar que `pay_st` puede venir `4`/`7` (el escenario lo advierte) es el agujero de seguridad y de robustez.
- **Context map de cajas sin relaciones**: dibujar Soporte/ERP/IA conectados sin decir quién es upstream/downstream ni por qué hay ACL.
- **ADR con una sola opción** o sin gatillo: no hubo trade-off.
- **"Todo DDD por consistencia"**: aplicar aggregates al CRUD de categorías es el over-engineering que el ejercicio pide detectar.
- (transversal seguridad) no reconocer que el input externo / salida de LLM es no confiable hasta validarlo en la aduana.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Mapa y ADR pulidísimos con jerga DDD (context mapping patterns completos) pero el alumno no puede defender **por qué** eligió ACL sobre conformist *en este caso*: la forma vino de fuera.
- El "juicio DDD-sí/DDD-no" repite la lección palabra por palabra pero no aplica el criterio a una parte concreta de *este* sistema.
- Diseño que ignora pistas específicas del escenario (los `pay_st` mágicos, el cambio histórico del proveedor): señal de respuesta genérica no leída.

## Feedback sugerido (graduado)
- **Pista (nivel 1):** "¿Tu aduana solo renombra, o también decide qué entra? ¿Qué pasa si el ERP manda `pay_st: 4`?"
- **Pregunta socrática (nivel 2):** "Si el proveedor cambia mañana sus códigos (ya lo hizo antes), ¿cuántos archivos de tu sistema tocas? Si la respuesta no es 'uno', ¿dónde se filtró su modelo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** señala el punto donde el modelo sucio entra al dominio sin traducir, o la relación del mapa sin nombrar, sin rediseñar por el alumno.

## Conexión con el proyecto / capstone
- Es exactamente lo que pide el capstone F8 (diseña 3 sistemas en papel): bounded contexts en Mermaid + dónde van los ACL (la automatización de tickets integra sistemas externos y LLMs) + ADRs que justifican el modelado.
