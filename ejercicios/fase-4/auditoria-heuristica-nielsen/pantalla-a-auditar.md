# Pantalla a auditar — "Subir documentos" de una app de IA

> Descripción de una pantalla real (de una app de chat con RAG, donde el usuario sube documentos para que
> la IA los use como fuentes). Audítala según las 10 heurísticas de Nielsen. **No la rediseñes en código**:
> diagnostícala por escrito en `auditoria.md`.

## Qué hace la pantalla

Es la sección "Mis documentos" de la app. El usuario sube archivos (PDF, .docx) que luego la IA indexa para
responder preguntas. Esto es lo que se observa, tal cual:

## Layout y textos (de arriba a abajo)

- Un encabezado: **"Gestión de entidades documentales del repositorio"**.
- Una zona de subida con el texto **"Drop zone"** y, debajo, un botón gris claro (texto `#b8b8b8` sobre
  fondo blanco) que dice **"EXEC UPLOAD"**.
- Debajo, una tabla con las columnas: `doc_id`, `fname`, `status_code`, `ts_created`. Cuando el usuario
  todavía no ha subido nada, la tabla aparece **completamente vacía** (solo los encabezados de columna y un
  área en blanco; no dice nada más).
- Abajo del todo, un botón rojo **"PURGE ALL"** sin más explicación.

## Comportamiento observado

1. **Al subir un archivo**, el usuario hace click en "EXEC UPLOAD", elige el archivo, y... la pantalla no
   cambia en nada durante varios segundos. No hay barra de progreso, ni spinner, ni texto. El usuario no
   sabe si el archivo se está subiendo o si la app se colgó. A veces vuelve a hacer click y sube el archivo
   dos veces.
2. **Si el archivo pesa más de lo permitido** (el límite es 10 MB, pero ese dato no aparece en ninguna
   parte), la subida se procesa unos segundos y luego aparece, en rojo: **"Error: ERR_PAYLOAD_413"**. No
   dice cuál es el límite ni qué hacer.
3. **Si la subida falla por un problema de red**, aparece un texto pequeño que dice **"Algo salió mal."** y
   nada más. No hay forma de reintentar sin recargar toda la página.
4. **El botón "PURGE ALL"** borra **todos** los documentos del usuario de inmediato, sin confirmación y sin
   posibilidad de deshacer. Un usuario lo presionó pensando que limpiaba solo la lista visual y perdió 40
   documentos.
5. **El estado de un documento** se muestra en la columna `status_code` como un número: `0`, `1` o `2`. En
   otra pantalla de la misma app, los mismos estados se muestran como texto ("Procesando", "Listo",
   "Error"). El usuario debe recordar qué número significa qué.
6. Para subir un documento hay que hacer click en "EXEC UPLOAD"; pero para subir una **carpeta** hay que ir
   a un menú distinto llamado "Importar", con un flujo totalmente diferente y otra terminología.
7. La "Drop zone" **parece** una caja decorativa: no tiene borde punteado ni ícono ni cursor que sugiera que
   puedes arrastrar archivos ahí. Varios usuarios nunca descubren que se puede arrastrar y soltar.

## Tu tarea

Diagnostica **al menos seis** problemas, cada uno atado a una **heurística de Nielsen concreta** (número +
nombre). Al menos uno debe ser un **estado faltante**. Cierra con un **top-3 priorizado** por impacto. Deja
todo en `auditoria.md`.
