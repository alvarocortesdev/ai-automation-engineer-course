# Formulario actual — "Conectar fuente de datos"

> Descripción del formulario tal como está hoy. Funciona, pero es hostil. Rediseña su UX por escrito en
> `rediseno-ux.md`. **No lo implementes en código.**

## Qué hace

Es el formulario donde el usuario conecta una fuente de datos a la app de IA: pega una **API key** del
proveedor y la **URL** del endpoint, le pone un **nombre** a la conexión, y elige cada cuánto se sincroniza.
Al enviar, la app valida la key contra el proveedor y guarda la conexión.

## Los campos (tal cual)

1. **Nombre de la conexión** — campo de texto libre, obligatorio.
2. **API key** — campo de texto normal (la key se ve en pantalla mientras la pegas; no hay toggle de
   mostrar/ocultar). Debe empezar con `sk-` y tener al menos 40 caracteres.
3. **URL del endpoint** — campo de texto libre. Debe ser una URL `https://`.
4. **Frecuencia de sincronización** — campo de texto libre donde el usuario escribe el número de minutos
   (ej: escribe "60"). Si escribe letras, falla al enviar.

## Comportamiento observado (lo hostil)

1. **Valida en cada tecla, desde la primera letra.** Apenas escribes la `a` en "Nombre", aparece en rojo
   "Campo inválido". En "API key", mientras pegas, parpadea "API key inválida" hasta que terminas de pegar.
2. **Mensajes de error vagos o que culpan al usuario:**
   - Nombre vacío → **"Campo inválido"**.
   - API key mal → **"API key inválida"** (no dice qué formato espera).
   - URL mal → **"Escribiste mal la URL"**.
   - Frecuencia con letras → **"Error de tipo: se esperaba number, se recibió string"**.
3. **No previene errores:** el campo de frecuencia es texto libre (deja escribir "sesenta", "60 min",
   emojis). La API key se pega a ciegas y no hay forma de verificar que pegaste la correcta.
4. **El botón "Conectar" no da feedback:** al hacer click, no se deshabilita ni cambia de texto. Si la
   validación contra el proveedor tarda 3 segundos, el usuario no sabe si pasó algo y vuelve a hacer click,
   creando **dos** conexiones.
5. **Si la validación contra el proveedor falla** (key revocada, proveedor caído), aparece arriba del todo,
   fuera de la vista si hiciste scroll, un texto **"No se pudo conectar"** sin más. El foco no se mueve y un
   lector de pantalla no lo anuncia.
6. **No hay confirmación de éxito:** cuando sí funciona, el formulario simplemente se limpia. El usuario no
   está seguro de si se guardó.
7. **Los `<label>` no están asociados a sus campos** (son `<div>` arriba de cada input); el placeholder hace
   de etiqueta y desaparece al escribir.

## Tu tarea

Rediseña la UX por escrito en `rediseno-ux.md`: mensajes de error, timing de validación por campo,
prevención/affordances/feedback, estados del envío, y al menos tres conexiones con la accesibilidad.
