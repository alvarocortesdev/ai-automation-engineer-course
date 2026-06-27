---
ejercicio_id: fase-4/auditoria-a11y-teclado
fase: fase-4
sub_unidad: "4.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Ejercicio de **razonamiento**: no
> existe una única redacción correcta. El alumno puede agrupar o nombrar problemas distinto y estar
> `excelente` si el SC es correcto y la corrección es defendible.

# Solución de referencia — Auditoría de accesibilidad

## 1. Orden de foco trazado (ejemplo canónico)

Con `Tab` repetido, los **`tabindex` positivos van primero** (en orden numérico), luego el resto en orden
de DOM:

1. **Campo de búsqueda** (`tabindex="1"`).
2. **"Aprobar todo"** (`tabindex="2"`) — ¡al final visualmente, pero segundo en foco! Eso ya es un bug.
3. Botón de engranaje del header (orden de DOM).
4. (Las filas) campos de comentario, etc., en orden de DOM.
5. ...

**Inalcanzables con teclado:** "Ver detalle" (`<div onclick>` sin `tabindex` ni rol) — un usuario de teclado
no puede abrir el detalle.

**Trampa de foco:** el modal de confirmación. Al abrirse el foco **no** se mueve a él; una vez dentro, `Tab`
cicla solo entre sus botones y no sale; `Esc` no cierra. Quien no tiene mouse queda **atrapado**.

## 2. Problemas diagnosticados (ejemplo de entrega "excelente")

> Cada entrada: problema · SC violado · corrección.

1. **`tabindex="1"` y `"2"` fuerzan un orden de foco que no calza con el visual.** · **SC 2.4.3 Focus
   Order** (y antipatrón general). · Corrección: quitar los `tabindex` positivos; ordenar el DOM para que
   el orden natural sea correcto.

2. **"Ver detalle" es un `<div onclick>`: inalcanzable y sin rol.** · **SC 2.1.1 Keyboard** y **SC 4.1.2
   Name, Role, Value**. · Corrección: usar `<button>` (o `<a href>` si navega). HTML nativo, **no**
   `tabindex="0"` + handlers a mano.

3. **El modal atrapa el foco; `Esc` no cierra y el foco no entra al abrir.** · **SC 2.1.2 No Keyboard
   Trap** (y patrón de diálogo). · Corrección: mover foco al modal al abrir, atraparlo *a propósito*
   mientras está abierto, `Esc` cierra, devolver el foco al disparador al cerrar; `inert`/`aria-hidden` en
   el fondo.

4. **Los botones del modal tienen `outline: none`: no se ve cuál está enfocado.** · **SC 2.4.7 Focus
   Visible**. · Corrección: reemplazar por `:focus-visible` con anillo de contraste ≥ 3:1.

5. **El contenido de la lista de atrás sigue enfocable con el modal abierto, y al recibir foco queda
   tapado por el header fijo.** · **SC 2.4.11 Focus Not Obscured (Minimum)** (+ el fondo debería ser
   `inert`). · Corrección: inertizar el fondo cuando el modal está abierto; dar `scroll-margin`/offset para
   que el foco no quede bajo el header.

6. **"Confirmar" es un `<div role="button">`: ARIA que miente.** · **SC 4.1.2** (y la Primera Regla de
   ARIA). · Corrección: `<button>`. El `role` lo anuncia como botón pero no lo hace enfocable ni operable
   con `Enter`/`Space`: "no ARIA es mejor que mal ARIA".

7. **El campo de búsqueda y el botón de engranaje no tienen nombre accesible** (solo placeholder / solo
   ícono). · **SC 4.1.2** (y 1.3.1 para el label). · Corrección: `<label>` (visible o `aria-label`) para la
   búsqueda; `aria-label="Ajustes"` para el botón de ícono.

8. **El botón de engranaje mide 16×16 px.** · **SC 2.5.8 Target Size (Minimum)** (mínimo 24×24, ideal 44).
   · Corrección: agrandar el área táctil a ≥ 24×24 (mejor 44×44).

9. **Título de acción en `#bdbdbd` sobre blanco (~1.6:1).** · **SC 1.4.3 Contrast (Minimum)**. ·
   Corrección: oscurecer a ≥ 4.5:1 (p. ej. `#595959`).

10. **El error del comentario es solo un borde rojo, sin texto ni ícono.** · **SC 1.4.1 Use of Color** (+
    **3.3.1 Error Identification** y **4.1.3 Status Messages** para anunciarlo). · Corrección: añadir
    mensaje de texto + ícono, enlazado con `aria-describedby` y `role="alert"`.

11. **El logo no tiene `alt`; el gráfico de confianza tiene `alt="imagen"`.** · **SC 1.1.1 Non-text
    Content**. · Corrección: logo informativo → `alt="Acme Revisión"` (o `alt=""` si es puramente
    decorativo junto al nombre en texto); el gráfico es **informativo** → `alt` que dé el dato (p. ej.
    "Confianza del modelo: 86%"), no "imagen".

## 3. Top-3 priorizado (ejemplo)

1. **#3 — Trampa de foco del modal (2.1.2).** Es el peor: un usuario de teclado queda **completamente
   atrapado** y no puede ni confirmar ni salir. Bloquea la función entera.
2. **#2 — "Ver detalle" inalcanzable (2.1.1).** Un control clave es **imposible** de usar sin mouse:
   bloquea, no solo molesta.
3. **#9/#10 — Contraste ilegible (1.4.3) + error solo por color (1.4.1).** Dejan fuera a usuarios de visión
   baja y daltónicos; fallan en accesibilidad **y** en legibilidad básica.

> Criterio de priorización: **¿bloquea por completo a alguien o solo lo molesta?** Trampa de foco y control
> inalcanzable bloquean → primero. Contraste y "solo color" excluyen a grupos enteros → segundo.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **El orden de foco no es "el de aparición":** los `tabindex` positivos lo rompen. Detectarlo es la mitad
   del ejercicio.
2. **Diagnosticar = nombrar el SC, no el síntoma.** "El modal molesta" es síntoma; "SC 2.1.2 No Keyboard
   Trap" es la causa nombrable y buscable.
3. **La mayoría de los arreglos son 'usa HTML nativo'**, no 'agrega ARIA'. La Primera Regla aparece tres
   veces aquí (div→button, ícono→aria-label como excepción legítima, modal→patrón de diálogo).
4. **Priorizar es ingeniería:** se justifica por impacto (bloquea vs. molesta), no por gusto.

## Puntos resbalosos (donde el corrector debe mirar)
- Que detecte la **trampa de foco** (2.1.2): es el problema estrella y el que más se omite.
- Que **no confunda** 2.4.7 (foco invisible) con 2.4.11 (foco tapado): son dos problemas distintos en esta
  pantalla.
- Que marque el **"solo color"** (1.4.1) en el error, no solo "falta contraste".
- Que entienda que el gráfico es **informativo** (necesita `alt` con el dato), no decorativo.
- Que la priorización use el eje **bloquea vs. molesta**, no "el que más le incomoda".

## Rango de soluciones aceptables
- El alumno puede listar 5–11 problemas y agruparlos distinto; `excelente` si los SC son correctos.
- Algunos SC admiten matiz (el orden de foco roto puede citarse como 2.4.3 y/o como antipatrón de
  `tabindex`; el error puede mapear a 1.4.1 + 3.3.1 + 4.1.3). Se acepta cualquiera bien argumentado.
- El top-3 puede variar mientras la justificación por impacto sea sólida; la trampa de foco y el control
  inalcanzable casi siempre deberían entrar.
