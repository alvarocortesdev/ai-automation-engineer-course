---
ejercicio_id: fase-2/solid-juicio-sobre-abstraccion
fase: fase-2
sub_unidad: "2.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). **Importante:** este ejercicio **no tiene
> respuesta correcta única**. Esta solución es una *orientación de qué razonamiento es defendible*, no una
> plantilla a la que el alumno deba converger. Califica el trade-off, no el bando.

# Solución de referencia — El juicio: ¿abstraer o no?

## Cómo usar esta solución

El alumno entrega `decisiones.md` con tres decisiones. Para cada una, contrasta su **(a) decisión, (b) smell,
(c) trade-off, (d) gatillo** contra la dirección defendible de abajo. Lo que mide la rúbrica es si **pesó las
fuerzas**, no si coincidió contigo. Una decisión contraria con un trade-off explícito y honesto es `competente`
o `excelente`.

## Escenario 1 — El reporte que solo exporta a PDF

**Dirección defendible: NO abstraer todavía (dejar la función concreta).**

- **Smell:** **ausente**. Hay **un** formato real (PDF). El "quizás algún día Excel, no sé" es especulación, no
  un requisito. Abstraer ahora sería **speculative generality**.
- **Trade-off:** a favor de abstraer está OCP/DIP ("preparado para más formatos"); en contra está
  **YAGNI + Rule of Three**: con un solo caso no conoces el eje de variación (¿el segundo formato compartirá la
  misma interfaz que imaginas hoy?), y casi siempre la abstracción especulada no calza con el segundo caso real.
- **Gatillo:** "cuando exista un **segundo formato confirmado** (no un 'quizás'), extraigo una abstracción
  `Exportador` —y ahí ya tengo dos casos para diseñar bien la interfaz."
- **Por qué es la dirección fuerte:** el costo de refactorizar de 1 función concreta a 2 implementaciones cuando
  Excel sea real es **bajo**; el costo de una abstracción equivocada hecha hoy es **alto**. Esperar gana.
- *Decisión contraria aceptable:* abstraer ya, **si** el alumno argumenta que el formato es un punto de
  extensión conocido del dominio del producto (un generador de reportes cuyo negocio ES exportar a muchos
  formatos). Debe nombrar esa evidencia, no el "quizás".

## Escenario 2 — El cliente de pagos (Stripe instanciado por dentro)

**Dirección defendible: SÍ invertir la dependencia (DIP).**

- **Smell:** **presente y doble.** (1) Acoplamiento que **impide testear hoy**: no puedes probar el checkout sin
  cobrar tarjetas reales (dolor concreto, ya). (2) Un **segundo proveedor probable** el próximo trimestre (eje de
  variación con evidencia, no especulación).
- **Trade-off:** a favor, DIP (testabilidad inmediata + flexibilidad de proveedor); en contra, el costo de
  indirección (un `Protocol` + inyección). Aquí el costo se paga **hoy** con un beneficio que también es **hoy**
  (poder testear), así que el cálculo se inclina claro a abstraer.
- **Gatillo:** no aplica un gatillo de "esperar" —el smell ya está. Lo que sí: empezar por la **mínima**
  abstracción (un `Protocol` `PasarelaPago` + un `FakePago` para tests), no un framework de DI completo.
- **Por qué es la dirección fuerte:** a diferencia del escenario 1, aquí hay **dos fuerzas reales y presentes**.
  La testabilidad rota es un smell *de hoy*; no es especulación. Esa es la diferencia que el ejercicio quiere que
  el alumno detecte.
- *Decisión contraria aceptable:* difícil de defender bien. Si el alumno deja Stripe concreto, debería al menos
  reconocer que sacrifica testabilidad inmediata —y eso ya es un costo difícil de justificar.

## Escenario 3 — La clase `Usuario` (¿separar la validación?)

**Dirección defendible: NO separar (mantener la cohesión).**

- **Smell:** **ausente**. `validar_email()` y `nombre_completo()` no cambian por **razones distintas**: ambos son
  parte de "qué es y cómo se comporta un usuario". No hay *divergent change*. La propuesta del colega es **SRP
  dogmático**: confunde "una clase = una sola cosa" con "una clase = una sola razón de cambio".
- **Trade-off:** a favor de separar, una lectura literal de SRP; en contra, **cohesión** + el riesgo de crear
  fragmentos **anémicos** y **shotgun surgery** (un cambio en "usuario" que ahora obliga a tocar dos clases).
- **Gatillo:** "si la validación de email crece a reglas complejas con su propio ciclo de cambio (políticas,
  dominios permitidos, integración externa), *ahí* la extraigo a un `ValidadorEmail` —cuando tenga su propia
  razón de cambio."
- **Por qué es la dirección fuerte:** SRP es "una razón para cambiar", no "un método por clase". Trocear por
  trocear empeora el diseño. Detectar que **no hay smell** es una respuesta de ingeniería válida, no pereza.
- *Decisión contraria aceptable:* extraer `ValidadorEmail` **si** la validación ya es no trivial y reutilizable
  por otras entidades (no solo `Usuario`). Debe nombrar esa reutilización real como el smell que lo justifica.

## Patrón que distingue los tres escenarios (lo que el ejercicio enseña)

| Escenario | ¿Smell HOY? | ¿Eje de variación real o especulado? | Dirección |
|---|---|---|---|
| 1 · Reporte PDF | No | Especulado ("quizás") | No abstraer (+ gatillo) |
| 2 · Pagos Stripe | Sí (testabilidad rota) | Real (2.º proveedor probable) | Abstraer (DIP) |
| 3 · `Usuario` | No | No hay (misma cohesión) | No separar (+ gatillo) |

La lección de fondo: **el smell presente HOY justifica el principio.** Un eje de variación especulado o una
lectura literal de SRP no bastan. Saber decir "no abstraigo, y este es el evento que me haría cambiar de
opinión" es la marca del criterio semi-senior.
