# Pantalla a auditar — "Panel de revisión de documentos con IA"

> Esta es la **descripción** de una pantalla real (no la vas a ejecutar: la audita a mano). Léela como si
> tuvieras el HTML y el render delante. Tu trabajo está en el `README.md` del ejercicio.

## Contexto

Un panel donde un revisor aprueba o rechaza acciones que una IA propuso sobre documentos subidos. Tiene un
header fijo, una lista de acciones, y un modal de confirmación. Funciona perfecto con mouse.

## Estructura y comportamiento (lo que verías)

**Header (fijo, sticky arriba, ~80px de alto):**
- Logo (una `<img src="logo.png">`, sin `alt`).
- Un campo de búsqueda con `placeholder="Buscar documento"` y **sin** etiqueta visible ni label.
- Un botón circular con solo un ícono de engranaje (sin texto), marcado como
  `<button>` pero **sin** `aria-label` ni texto interno. Mide 16×16 px.

**Orden del HTML y `tabindex`:**
- El campo de búsqueda tiene `tabindex="1"`.
- El botón "Aprobar todo" (abajo del todo en la página) tiene `tabindex="2"`.
- El resto de los controles no tiene `tabindex` declarado.

**Lista de acciones (cada fila):**
- Un título de acción en texto gris claro `#bdbdbd` sobre fondo blanco.
- Un gráfico de barras (`<img src="grafico.png">`) que muestra la confianza del modelo, con
  `alt="imagen"`.
- Un control "Ver detalle" hecho con `<div class="link" onclick="verDetalle()">Ver detalle</div>`.
- Un campo de comentario que, si lo dejas vacío y envías, muestra el borde en **rojo** y nada más
  (sin texto ni ícono que explique el error).

**Modal de confirmación (al pulsar "Aprobar todo"):**
- Aparece centrado, tapando la lista.
- El foco **no** se mueve al modal al abrirse; sigue en el botón de atrás.
- Una vez que tabulas hasta dentro del modal, el `Tab` cicla **solo** entre sus dos botones y **nunca**
  vuelve a salir; `Esc` **no** cierra el modal. La única forma de cerrarlo es con el mouse en la "X".
- Los botones del modal ("Confirmar" / "Cancelar") tienen `outline: none` en el CSS, así que al tabular
  no se ve cuál está enfocado.

**Otros detalles:**
- "Confirmar" es un `<div role="button" onclick="confirmar()">Confirmar</div>` (no es un `<button>`).
- Cuando el modal está abierto, parte del contenido enfocable de la lista de atrás sigue siendo alcanzable
  con `Tab` (no se inertiza), y al recibir foco un elemento de la fila superior, queda **tapado** por el
  header fijo.

## Lo que NO debes hacer

No reescribas la pantalla en código. Este ejercicio es de **diagnóstico**: trazar el orden de foco,
nombrar el SC de WCAG 2.2 que viola cada problema, proponer la corrección y priorizar.
