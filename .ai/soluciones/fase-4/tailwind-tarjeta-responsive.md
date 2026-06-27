---
ejercicio_id: fase-4/tailwind-tarjeta-responsive
fase: fase-4
sub_unidad: "4.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tarjeta responsive (utility-first)

## Respuesta canónica (marcado de ejemplo)

Una de muchas tarjetas válidas. Lo que importa es que cumple el método: utilidades + escala,
responsive `md:`, `hover:`, `dark:`, y cero CSS propio.

```html
<article
  class="flex w-full max-w-sm flex-col gap-4 rounded-lg bg-white p-6 shadow-sm
         md:max-w-md md:p-8
         dark:bg-gray-800"
>
  <div class="h-40 rounded-md bg-indigo-200 dark:bg-indigo-900"></div>

  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
    Auriculares inalámbricos
  </h3>
  <p class="text-sm text-gray-600 dark:text-gray-300">
    Cancelación de ruido y 30 horas de batería.
  </p>

  <div class="mt-2 flex items-center justify-between">
    <span class="text-xl font-bold text-gray-900 dark:text-white">$49.990</span>
    <button
      class="rounded-md bg-indigo-600 px-4 py-2 font-medium text-white
             hover:bg-indigo-700
             focus:outline-2 focus:outline-offset-2 focus:outline-indigo-500
             dark:bg-indigo-500 dark:hover:bg-indigo-400"
    >
      Comprar
    </button>
  </div>
</article>
```

## Razonamiento paso a paso
- **Contenedor:** `flex flex-col gap-4` apila los hijos con separación de la escala; `p-6`/`rounded-lg`/`shadow-sm`/`bg-white` dan el aspecto de tarjeta. Todo desde utilidades, sin un solo número mágico inline.
- **Responsive:** el base es móvil (`max-w-sm`, `p-6`); `md:max-w-md md:p-8` solo sobre-escribe desde 768px hacia arriba. Es mobile-first: el teléfono no necesita prefijo.
- **Estado:** `hover:bg-indigo-700` es la pseudo-clase `:hover` declarada como variante; `focus:outline-*` añade un foco visible (puente a accesibilidad, 4.4).
- **Dark mode:** por cada color base hay una gemela `dark:` (`bg-white`→`dark:bg-gray-800`, `text-gray-900`→`dark:text-white`). En tema oscuro toman el control; en claro no afectan.
- **Cero CSS propio:** ningún `style=` inline (no podría lograr `hover:`/`md:`/`dark:`) y ningún `@apply` (no se repite estructura aquí).

## Puntos resbalosos (donde el corrector debe mirar)
1. **`dark:` incompleto:** poner `dark:bg-gray-800` en el contenedor pero olvidar `dark:text-*` en los textos → en oscuro queda texto gris oscuro sobre fondo oscuro (ilegible). Marca C2.
2. **Mobile-first invertido:** usar `md:flex-col` creyendo que `md:` es "lo chico". El base es móvil; `md:` es de 768px hacia arriba.
3. **`style=` inline o CSS a mano:** rompe O3. El test atrapa el inline; el CSS a mano lo ve el corrector (un `<style>` con reglas propias para la tarjeta).
4. **`@apply` "para limpiar":** no corresponde aquí; es exactamente el anti-patrón del segundo ejercicio.
5. **Marcadores borrados o placeholder intacto:** el test falla en "estructura mínima"; antes de evaluar el resto, pídele restaurar marcadores / escribir su tarjeta.

## Rango de soluciones aceptables
- Cualquier paleta y estructura (precio arriba o abajo, imagen como `<img>` o bloque de color) es válida si cumple los seis criterios.
- `grid`/`grid-cols-*` en vez de `flex` es válido para el layout.
- El cambio responsive puede ser cualquiera (columna→fila, padding, ancho, tamaño de fuente) mientras use un prefijo `sm:`/`md:`/`lg:`.
- `focus:` es opcional (suma), pero un botón **sin** ningún estado de foco es una observación válida de accesibilidad aunque el test no lo exija.
- Usar `dark:` por preferencia de sistema (sin el toggle) también es válido; el starter trae el toggle solo para que lo pueda **ver**.
- **No** es aceptable lograr el aspecto con estilos inline o con CSS propio aunque "se vea igual": viola el objetivo del ejercicio (utility-first).
