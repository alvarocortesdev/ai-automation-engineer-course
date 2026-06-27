---
ejercicio_id: fase-4/tailwind-cuando-extraer
fase: fase-4
sub_unidad: "4.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Criterio: utilidades, componente o @apply

## Respuesta canónica (las cuatro decisiones)

El eje rector es, **en orden**: (1) ¿controlo el marcado? (2) si lo controlo, ¿se repite la
estructura completa o es de una vez?

| # | Escenario | Decisión | Por qué |
|---|---|---|---|
| 1 | Botón repetido en 12 pantallas (React) | **Componente** | Controlo el marcado **y** se repite la estructura completa (marcado + estilo + comportamiento). Un `<Boton>` es una sola fuente de verdad. `@apply` aquí reintroduciría una clase CSS global acoplada que utility-first vino a eliminar. |
| 2 | Hero usado una sola vez | **Utilidades (no abstraer)** | Controlo el marcado, pero **no se repite**. Abstraer lo único es YAGNI: agrega indirección sin pagar nada. Se dejan las utilidades inline en el marcado. |
| 3 | Date-picker de terceros | **`@apply` (o `@variant`)** | **No controlo** ese HTML (`<div class="dp-cell">` lo renderiza la librería). No hay componente que extraer porque no soy dueño del marcado: estilar sus selectores con `@apply` es el caso legítimo. |
| 4 | HTML generado al renderizar Markdown | **`@apply` (o patrón de tipografía)** | Tampoco escribo ese marcado (`<h1>`, `<p>`… salen del render). Estilo por etiqueta con `@apply`, o uso el patrón de tipografía (`prose`/plugin de typography). El eje vuelve a ser: no controlo el marcado. |

## Regla general de referencia
> "**Primero pregunto si el marcado es mío.** Si no lo es (librería, contenido generado), `@apply`/`@variant` sobre sus selectores. Si lo es, abstraigo a un **componente** solo cuando la **estructura** se repite; lo de una sola vez se queda como utilidades."

## Razonamiento paso a paso
- El error que el ejercicio caza es usar `@apply` para "ordenar" HTML propio cargado (escenario 1). Es tentador porque "limpia" el marcado, pero reintroduce el CSS global, el acoplamiento y los nombres que mantener —justo lo que utility-first elimina—. La duplicación real ahí es la **estructura**, no el estilo, y la cura es un componente (DRY bien aplicado, ver 2.2).
- El componente le gana a la clase `.btn` porque encapsula **marcado + estilo + comportamiento** en una sola fuente de verdad; `.btn` solo encapsula estilo y te obliga a repetir el `<button>`.
- `@apply` no es "malo": es la herramienta correcta cuando **no puedes** añadir clases al marcado (3 y 4). Ese es su nicho.
- El hero único (2) es la trampa opuesta: sobre-abstraer. Una sola aparición no justifica componente ni clase.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`@apply` en el escenario 1:** error central. Aunque "suene a DRY", la salida correcta es componente. Marca C1/C3.
2. **Abstraer el hero único (2):** YAGNI; lo de una vez se deja.
3. **Proponer "editar el HTML de la librería" (3) o "tocar el render de Markdown" (4):** no controla ese marcado; por eso `@apply` existe.
4. **Justificar todo con "es más limpio":** sin nombrar control del marcado ni repetición, no demuestra el criterio.
5. **Regla general sin el eje "¿es mío el marcado?":** queda en intuición, no en criterio defendible.

## Rango de soluciones aceptables
- En el 4, **tanto** `@apply` por etiqueta **como** el patrón de tipografía (`prose`/plugin) son válidos: ambos reconocen que no controlas el marcado.
- En el 3, mencionar `@variant` dentro de CSS propio (en vez de `@apply`) también es válido y demuestra mayor dominio.
- En el 1, proponer un componente **con variantes** (p. ej. `variant="primary"`) es excelente, no exigido.
- Es válido que el alumno señale que, antes de `@apply` en 3/4, conviene revisar si la librería ofrece *slots*/props de clase; si no, `@apply` es la salida.
- **No** es aceptable resolver el 1 con `@apply` ni el 2 con un componente, aunque la prosa suene convincente: contradicen los ejes.
