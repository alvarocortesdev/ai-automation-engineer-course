---
ejercicio_id: fase-0/descomponer-problema-cotidiano
fase: fase-0
sub_unidad: "0.2"
version: 1
---

# Rúbrica — Descompón un problema cotidiano con las 4 herramientas

> Rúbrica analítica para un ejercicio **a-mano** de razonamiento. No hay "respuesta única": el problema es abierto. Lo que se evalúa es la **calidad del pensamiento**: ¿las dependencias son reales?, ¿la abstracción es consciente o es olvido disfrazado?, ¿los casos borde son los que de verdad rompen? Un write-up bonito con dependencias inventadas vale menos que uno feo con razonamiento sólido.

## Objetivos evaluados
- **O1** — Descomponer en subproblemas y nombrar dependencias.
- **O2** — Identificar un patrón y abstraer detalle irrelevante de forma justificada.
- **O3** — Diseñar un algoritmo sin ambigüedad con casos borde.

## Criterios y niveles

### C1 — Descomposición y dependencias · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No parte el problema, o lista pasos sueltos sin estructura; no hay dependencias. |
| **en-progreso** | Parte en subproblemas razonables pero no marca dependencias, o las que marca son triviales/decorativas ("primero pienso, luego hago"). |
| **competente** | 4–7 subproblemas coherentes y **al menos una dependencia real y justificada** (B necesita un producto de A). |
| **excelente** | Dependencias precisas (incluso detecta una no obvia, p. ej. que el chequeo de "falta algo" debe ir *después* de cierto paso), y subproblemas genuinamente independientes entre sí donde corresponde. |

### C2 — Patrón + abstracción · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica patrón, o "abstrae" sin justificar (lista detalles ignorados al azar). |
| **en-progreso** | Nombra un patrón superficial, o ignora detalles pero la justificación es débil ("no importa" sin explicar por qué). |
| **competente** | Un patrón claro ("hago lo mismo para cada invitado/caja/día") **y** 3+ detalles ignorados con un *porqué* defendible. |
| **excelente** | Conecta el patrón con su forma computacional ("esto sería un bucle"), y la abstracción muestra criterio: ignora lo irrelevante **sin** caer en sobre-abstracción (no inventa requisitos futuros). |

### C3 — Algoritmo y casos borde · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay pasos numerados, o son tan vagos que dos personas los ejecutarían distinto ("organiza bien las cosas"). |
| **en-progreso** | Pasos numerados pero con ambigüedad en alguno, o falta uno de los dos casos borde, o los casos borde son inventados/irrelevantes. |
| **competente** | Pasos sin ambigüedad que resuelven el problema **y** dos casos borde que de verdad podrían ocurrir, con qué hace el algoritmo en cada uno. |
| **excelente** | Algoritmo limpio cuyos pasos respetan las dependencias de C1, y casos borde *no obvios* (no solo "y si no hay nada", sino "y si un invitado responde tarde / una caja excede el peso"). |

## Errores típicos a marcar
- **Dependencias decorativas:** marcar "todo depende de todo" o dependencias triviales que no aportan. Una dependencia útil restringe el orden.
- **Abstracción = olvido:** ignorar detalles porque no se le ocurrieron, no porque decidió que no importan. Señal: no hay *porqué* junto a cada detalle ignorado.
- **Sobre-abstracción:** preparar el algoritmo para casos que nadie pidió ("¿y si algún día son 500 invitados en otro país?"). Es el error opuesto y también cuenta como inmaduro.
- **Pasos ambiguos:** "ordena las cajas correctamente" no es un paso; es un deseo. Un paso se ejecuta igual sin importar quién lo lea.
- **Casos borde de adorno:** poner un caso borde imposible o irrelevante para llenar el casillero, en vez de el que realmente rompería el plan.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Texto pulido y exhaustivo pero **sin una sola dependencia concreta** ni casos borde realistas (la IA tiende a producir listas completas y genéricas, sin el criterio del que vivió el problema).
- Vocabulario de ingeniería ("acoplamiento", "idempotencia") en un ejercicio cotidiano de F0, sin poder explicarlo.
- Abstracción que enumera detalles "irrelevantes" que en realidad **sí** importan para el problema elegido (señal de plantilla genérica, no de pensar este caso).
- **Verificación sugerida:** pídele que, en voz alta y sin notas, descomponga *otro* de los tres problemas en 2 minutos. Si pensó de verdad, fluye; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca rehacer el ejercicio por el alumno. Empujarlo a ver su propio hueco.
- **Pista (nivel 1):** "Tu descomposición está bien, pero, ¿podrías ejecutar el paso 4 sin haber terminado el 2? Si no, eso es una dependencia que falta nombrar."
- **Pregunta socrática (nivel 2):** "De los detalles que dijiste ignorar, ¿alguno cambiaría el resultado si fuera distinto? Si la respuesta es sí en alguno, no era ignorable. ¿Y los que ignoraste por buena razón: cuál es esa razón en una frase?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu algoritmo asume que todo sale bien. Recorre tus pasos preguntando en cada uno '¿y si esto falla?': ahí viven tus casos borde reales. Añade los dos que más probablemente ocurran y di qué hace el algoritmo en cada uno."

## Conexión con el proyecto / capstone
- Es el ensayo en seco del **Capstone F0 — CLI sin IA**: antes de teclear, descompondrás la CLI, abstraerás lo irrelevante y diseñarás su algoritmo. Quien no sabe descomponer un problema cotidiano tampoco sabrá descomponer su propia herramienta —y se notará en la demo.
