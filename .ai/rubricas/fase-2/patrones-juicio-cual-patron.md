---
ejercicio_id: fase-2/patrones-juicio-cual-patron
fase: fase-2
sub_unidad: "2.5"
version: 1
---

# Rúbrica — El juicio: ¿qué patrón, o ninguno?

> Rúbrica **analítica** atada a los `objetivos` del contrato. Este ejercicio **no tiene "respuesta correcta"
> única**: se evalúa la **calidad del razonamiento**, no el bando. Un alumno que decide "no abstraer" con un
> trade-off explícito y un gatillo observable puntúa **más alto** que uno que aplica el patrón "porque es la
> buena práctica". El antipatrón a cazar es la pattern-itis (abstraer sin smell) y su espejo (no nombrar nunca
> el smell que SÍ justifica abstraer).

## Objetivos evaluados
- **O1** — Reconocer qué patrón convoca un smell dado, o si ninguno aplica (YAGNI).
- **O2** — Justificar cada decisión con smell presente/ausente + fuerza a favor + argumento en contra.
- **O3** — Distinguir un eje de variación real y presente de uno especulado; definir el gatillo observable.

## Criterios y niveles

### C1 — Reconocimiento del patrón / no-patrón · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Decisiones sin nombrar patrón, o nombres mal usados (llama "Factory" a un Adapter), o no contempla nunca "ninguno". |
| **en-progreso** | Acierta el patrón en los escenarios obvios pero no reconoce los "ninguno" (1, 3) —tiende a abstraer siempre (pattern-itis). |
| **competente** | Reconoce el patrón pertinente donde aplica (2→Adapter, 4→Repository) y **defiende "ninguno"** donde corresponde (1, 3) en vez de abstraer por reflejo. |
| **excelente** | Además distingue capas (p. ej. en 1 nombra que serían Strategy *y* Factory si llegara el 2º formato) y matiza que reconocer el patrón ≠ aplicarlo ya. |

### C2 — Calidad del trade-off · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Decisiones sin justificación, o solo a favor (sin contra), o sin mencionar smell. |
| **en-progreso** | Menciona un smell pero el argumento en contra es genérico ("podría ser complejo") sin nombrar YAGNI / Rule of Three / costo de indirección / control de flujo invisible. |
| **competente** | Cada decisión nombra el smell **presente o ausente**, una fuerza a favor y un argumento en contra **concreto y pertinente** al escenario. |
| **excelente** | Conecta el argumento en contra con el costo específico del patrón (Observer→control de flujo invisible; Repository passthrough→indirección sin beneficio) y reconoce la tensión con DRY/YAGNI. |

### C3 — Eje de variación real vs especulado + gatillo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Trata "quizás algún día" (1) igual que "migración el próximo trimestre + testabilidad hoy" (2); decisiones de "no" sin gatillo. |
| **en-progreso** | Intuye la diferencia pero no la nombra; los gatillos son vagos ("si se complica"). |
| **competente** | Distingue explícitamente la **fuerza especulativa** (1, 3) de las **dos fuerzas reales y presentes** (2, 4) y da gatillos **observables** ("si entra un 2º formato", "si llega una 3ª reacción de otro equipo"). |
| **excelente** | Articula la regla general: dos fuerzas presentes (testabilidad *hoy* + cambio *probable*) inclinan a abstraer; una sola fuerza especulativa, no. Lo aplica consistentemente a los cuatro. |

## Errores típicos a marcar
- **Pattern-itis:** aplicar un patrón en 1 o 3 "porque es buena práctica" sin un smell que crezca. El escenario 1 tiene un solo formato; el 3, dos reacciones fijas —abstraer ahí es speculative generality.
- **No reconocer las dos fuerzas:** tratar el escenario 2 (Adapter) como especulativo cuando hay **testabilidad presente** (testear sin gastar tokens) *además* de la migración probable. Igual en 4 (Repository): duplicación presente + testabilidad + más queries.
- **Confundir patrones:** llamar Factory a lo que es Adapter, o Strategy a lo que es Observer. El smell distingue: interfaz incompatible→Adapter; reacciones que crecen→Observer; comportamiento que varía por tipo→Strategy.
- **Decisión sin gatillo:** decir "no abstraigo" sin definir qué evento observable lo cambiaría —deja la decisión sin fecha de revisión.
- **Observer para 2 reacciones fijas (escenario 3):** ignorar que el costo (control de flujo invisible) no se paga cuando las reacciones no crecen ni pertenecen a actores distintos.
- (transversales) no registrar la decisión como digna de un ADR; no defender un solo trade-off.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Las cuatro decisiones "suenan" perfectas y completas pero el alumno no puede **defender una en voz alta** ni responder "¿y si el PM insiste en 1?".
- Usa vocabulario de patrones impecable (speculative generality, control de flujo invisible) sin poder dar un ejemplo propio de cuándo lo vivió.
- Todas las decisiones van hacia abstraer (o todas hacia no), sin sensibilidad al contexto de cada escenario —respuesta de plantilla, no de juicio.
- **Verificación sugerida:** pedir que **cambie una variable** de un escenario en vivo (p. ej. "en el 3, ahora son 4 reacciones de 3 equipos distintos: ¿cambia tu decisión?") y vea si el razonamiento se mueve con coherencia.

## Feedback sugerido (graduado)
> Nunca dar la "respuesta": guiar el razonamiento.
- **Pista (nivel 1):** "Cuenta las fuerzas que empujan a abstraer en cada escenario. ¿Cuántas son reales y presentes hoy, y cuántas son 'quizás algún día'? Esa cuenta casi decide sola."
- **Pregunta socrática (nivel 2):** "En el escenario 3, si el Observer desacopla, ¿qué pierdes al leer `confirmar_pedido`? ¿Vale ese costo cuando solo hay dos reacciones que no crecen?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu decisión de 'no abstraer' necesita un **gatillo observable**: no 'si se complica', sino 'si entra un segundo formato' o 'si una tercera reacción la pide otro equipo'. Reescribe cada 'no' con su gatillo concreto y verás cuáles decisiones eran sólidas y cuáles eran miedo a abstraer (o ganas de abstraer)."

## Conexión con el proyecto / capstone
- Es el músculo que el **Capstone F2** exige documentar: en el `ARQUITECTURA.md` / ADR justificarás dónde aplicaste un patrón **y dónde decidiste NO hacerlo**. Esta segunda mitad —la crítica a la pattern-itis— es lo que separa tu capstone del de un junior que metió un Factory en cada constructor.
