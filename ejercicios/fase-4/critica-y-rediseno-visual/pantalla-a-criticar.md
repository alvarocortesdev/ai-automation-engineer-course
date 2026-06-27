# Pantalla a criticar — "Configuración del asistente"

> Esta es la descripción detallada (con valores concretos) de una pantalla real de configuración de un
> asistente de IA. No hay imagen: la especificación de abajo es suficiente para diagnosticarla. Tu
> trabajo está en el `README.md` de esta carpeta.

La pantalla es un formulario de configuración, renderizado en un contenedor que ocupa **todo el ancho del
navegador** (no tiene `max-width`). De arriba a abajo:

## Encabezado
- Texto "Configuración del asistente" en **18px, bold, color #1a1a1a**, alineado a la **izquierda**.

## Texto introductorio
- Un párrafo de ayuda: "Ajusta el comportamiento de tu asistente. Estos cambios afectan a todas las
  conversaciones nuevas y no se aplican a las conversaciones ya iniciadas; para más detalles consulta la
  documentación de parámetros del modelo." Está en **18px, bold, color #1a1a1a**, ocupa **todo el ancho**
  (≈ 180 caracteres por línea en una pantalla normal) y con `line-height: 1.0`.

## Sección "Modelo"
- El título de sección "Modelo" está en **18px, bold, #1a1a1a**.
- Etiqueta del campo: "Selecciona el modelo", **centrada**, en **18px, bold, #1a1a1a**.
- Debajo, un `<select>` alineado a la **izquierda**.
- La etiqueta "Selecciona el modelo" tiene **5px** de separación con el título de sección de arriba y
  **22px** con su propio `<select>` de abajo.

## Sección "Temperatura"
- Título "Temperatura" en **18px, bold, #1a1a1a**.
- Etiqueta "Nivel de creatividad", **centrada**, **18px, bold**.
- Un input de rango (slider), alineado a la **izquierda**.
- Texto de ayuda bajo el slider: "Valores altos = más creativo, valores bajos = más predecible", en
  **#c4c4c4 sobre fondo blanco**, 14px.
- Si el valor es inválido, el único feedback es que **el borde del input se pone rojo** (sin ícono, sin
  mensaje de texto).

## Acentos de color en la pantalla
- El botón "Guardar" es **azul**. El enlace "Restablecer" es **verde**. Un badge "Beta" junto al título es
  **naranja**. El ícono de ayuda es **morado**. (Cuatro colores de acento distintos.)
- El botón "Guardar" (acción primaria) usa **#dcdcdc con texto #9a9a9a** — se ve igual que un botón
  deshabilitado.

## Botonera
- "Guardar" (a la **derecha**) y "Restablecer" (a la **izquierda**), separados del resto del formulario por
  **13px**.

## Espaciado general
- Los espacios verticales entre elementos mezclan **5px, 13px, 22px y 30px** sin patrón.
