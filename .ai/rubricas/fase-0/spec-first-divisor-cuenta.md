---
ejercicio_id: fase-0/spec-first-divisor-cuenta
fase: fase-0
sub_unidad: "0.8"
version: 1
---

# Rúbrica — Spec-first: divisor de cuenta

> Rúbrica analítica para un ejercicio **mixto** (spec escrita + código + tests). Lo que más se evalúa
> no es que el código pase los tests —eso es el piso— sino que **la spec sea anterior al código** y que
> cada caso borde pensado se traduzca en un test o una validación. Un alumno puede tener los tests en
> verde y aun así fallar el objetivo central si codeó primero y "documentó" después.

## Objetivos evaluados
- **O1** — Escribir una mini-spec (entradas / salida / casos borde) **antes** de implementar.
- **O2** — Derivar tests y ramas de validación desde cada caso borde de la spec.
- **O3** — Implementar `dividir_cuenta` validando **antes** de dividir, con los tests en verde.

## Criterios y niveles

### C1 — La spec existe y es anterior al código · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `spec.md`, o sólo repite la firma de la función sin casos borde. |
| **en-progreso** | Hay spec pero parece escrita **después** del código: lista exactamente lo que el código hace, sin bordes que el código no maneje, o le faltan bordes del enunciado. |
| **competente** | `spec.md` con tabla entradas / salida y **al menos 4 casos borde** (negativo, cero, cero personas, división no exacta), plausible como diseño previo. |
| **excelente** | Además registra la **decisión de diseño** del redondeo como alternativa pensada, y anticipa el orden "validar antes de dividir" en la propia spec. |

### C2 — Cobertura: cada borde de la spec es test o validación · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Los bordes de la spec no aparecen ni como test ni como rama de código. |
| **en-progreso** | Algunos bordes cubiertos, otros declarados en la spec pero nunca verificados. |
| **competente** | Cada caso borde de la spec tiene su test o su `if` de validación; agregó **un test propio** real (un borde nuevo, no un duplicado). |
| **excelente** | El test propio cubre un borde genuino que los de base no tocaban (p. ej. `personas` no entero, `total` float con muchos decimales), con aserción precisa. |

### C3 — Corrección e ingeniería del código · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Tests en rojo, o `NotImplementedError` sin tocar. |
| **en-progreso** | Pasa algunos tests; divide **antes** de validar (cero personas lanza `ZeroDivisionError`, no `ValueError`), o trata `total == 0` como inválido. |
| **competente** | Los 7 tests en verde; valida `personas <= 0` y `total < 0` con `ValueError` **antes** de dividir; `total == 0` válido. |
| **excelente** | Código limpio y mínimo, mensajes de error claros, sin ramas muertas; la validación está separada del cálculo de forma legible. |

## Errores típicos a marcar
- **Spec escrita después del código** (o ausente): el objetivo central se incumple aunque los tests pasen.
- **Dividir antes de validar:** `dividir_cuenta(100, 0)` lanza `ZeroDivisionError` en vez de `ValueError`.
  Nota: el test igual lo detecta, porque `ZeroDivisionError` no es subclase de `ValueError`.
- **`total == 0` marcado como inválido:** confunde "cero" con "negativo"; rompe el test del cero.
- **Redondear sin declararlo en la spec:** rompe los tests de base y delata que no hubo contrato previo.
- **Test propio trivial:** repite un caso ya cubierto en vez de un borde nuevo de la spec.
- (transversal spec-driven) la spec no menciona ninguna decisión de diseño defendible (el redondeo).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `spec.md` y código con vocabulario o estructura por encima del nivel F0 que el alumno no puede defender.
- La spec calza **palabra por palabra** con el código y no contiene ningún borde que el código no maneje
  (señal de spec generada a partir del código ya hecho, no al revés).
- Solución impecable sin ningún rastro de iteración (ni un test que haya fallado, ni una nota de duda).
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué pasa con `dividir_cuenta(100, 0.0)`
  (float) o que añada el borde "`personas` debe ser entero" a la spec y lo defienda. Si diseñó de
  verdad, razona la decisión; si dependió de IA, improvisa.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Mira el orden dentro de tu función: ¿qué ocurre primero, validar o dividir?
  Prueba mentalmente `dividir_cuenta(100, 0)` y di qué excepción sale **exactamente**."
- **Pregunta socrática (nivel 2):** "¿Cada fila de 'borde' de tu `spec.md` tiene un test que la
  verifique? ¿Escribiste la spec antes o después del código? ¿Cómo lo notarías tú mismo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El patrón a corregir es **validar antes de
  operar**: pon las guardas de `personas <= 0` y `total < 0` (lanzando `ValueError`) **arriba**, antes
  de la división, y vuelve a correr el test del cero personas verificando que el tipo sea `ValueError`."

## Conexión con el proyecto / capstone
- La mini-spec es el primer paso literal del **Capstone F0 — CLI sin IA**: defines entradas/salidas/bordes
  del CLI antes de escribir una línea, y esa spec es a la vez tu mapa de construcción y tu lista de tests.
  Es también el embrión del hilo **spec-driven dev** que en la Fase 2 se formaliza con Spec Kit y ADRs.
