---
ejercicio_id: fase-4/auditoria-heuristica-nielsen
fase: fase-4
sub_unidad: "4.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). No hay una única respuesta correcta:
> el alumno puede encontrar problemas válidos no listados aquí, o asignar una heurística defendible
> distinta cuando se solapan. Lo que importa es el **razonamiento** y que nombre la heurística con criterio.

# Solución de referencia — Auditoría de usabilidad (panel "Subir documentos")

## Diagnóstico canónico (lista de referencia)

1. **Sin feedback al subir** (la pantalla no cambia durante segundos) → **H1 Visibility of system status**.
   *Estado de loading faltante.* Corrección: barra de progreso o spinner anunciado (`role="status"`) +
   deshabilitar "EXEC UPLOAD" mientras sube (evita la doble subida del punto 1).

2. **Error inútil "Error: ERR_PAYLOAD_413"** → **H9 Help users recognize, diagnose, recover from errors**.
   *Estado de error pobre.* Corrección: "El archivo pesa 14 MB; el máximo es 10 MB. Comprímelo o súbelo en
   partes." Y `role="alert"` para que se anuncie.

3. **El límite de 10 MB no se muestra en ninguna parte** → **H5 Error prevention**. Corrección: mostrar
   "PDF o .docx, hasta 10 MB" junto a la zona de subida, y rechazar el archivo en el cliente **antes** de
   subirlo. (Prevenir, no solo avisar — par con el punto 2: prevención vs. recuperación.)

4. **"PURGE ALL" borra todo sin confirmación ni deshacer** → **H3 User control and freedom**. (Pérdida de
   datos irreversible.) Corrección: ofrecer **deshacer** con una ventana de gracia (toast 5–10 s) — mejor
   que un "¿estás seguro?" que se clica sin leer.

5. **`status_code` como número (0/1/2)** que el usuario debe memorizar → **H6 Recognition rather than
   recall** (mostrar el significado, no obligar a recordarlo). Corrección: mostrar "Procesando / Listo /
   Error" como texto (idealmente con color + ícono).

6. **El mismo estado se muestra como número aquí y como texto en otra pantalla** → **H4 Consistency and
   standards**. Corrección: una sola representación de estado en toda la app.

7. **Jerga de base de datos en la UI** ("Gestión de entidades documentales", `doc_id`, `fname`,
   `ts_created`, "EXEC UPLOAD", "PURGE ALL") → **H2 Match between system and the real world**. Corrección:
   "Mis documentos", "Nombre", "Subido el", "Subir documento", "Borrar todo".

8. **La tabla vacía no dice nada** (solo encabezados) cuando el usuario no ha subido nada → **H1 Visibility
   of system status** (y desperdicia el empty de onboarding). *Estado empty faltante.* Corrección: un empty
   que explique e invite ("Aún no tienes documentos. Sube el primero para que la IA pueda usarlo").

9. **La "Drop zone" no parece interactiva** (sin borde punteado, ícono ni cursor) → **H1/affordance** (y
   roza **H10 Help and documentation**). Corrección: borde punteado, ícono de subida, texto "Arrastra aquí
   o haz click".

10. **Subir archivo vs. subir carpeta son flujos y terminología distintos** → **H4 Consistency and
    standards** / **H7 Flexibility and efficiency**. Corrección: unificar en un solo flujo.

11. **Sin reintento ante fallo de red** ("Algo salió mal" y hay que recargar la página) → **H9** (recuperación
    sin salida). Corrección: botón "Reintentar" en el propio mensaje de error.

## Estados faltantes (lo que la lección enfatiza)
- **Loading:** no hay (punto 1). **Error:** existe pero es inútil y sin salida (puntos 2, 11). **Empty:** no
  hay (punto 8). Tres de los cuatro estados de primera clase están mal o ausentes; solo el success (la tabla
  con datos) está cubierto. Es el caso de libro del "happy path solamente".

## Top-3 priorizado (referencia)
1. **"PURGE ALL" sin deshacer (H3).** Va primero: causa **pérdida de datos irreversible** (un usuario ya
   perdió 40 documentos). El impacto más alto posible.
2. **Sin feedback al subir (H1, loading).** Bloquea la tarea principal: el usuario no sabe si funcionó,
   sube dos veces, o abandona. Afecta a todos, todo el tiempo.
3. **Errores inútiles + sin reintento (H9) y límite oculto (H5).** El usuario que falla queda atascado sin
   saber por qué ni cómo salir; prevenir el error de tamaño y dar un mensaje + reintento desbloquea el flujo.

> Criterio de orden: primero lo que **destruye o bloquea** (pérdida de datos > tarea imposible de completar),
> después lo que **confunde** (jerga, números), al final lo cosmético. La jerga (H2) y la inconsistencia (H4)
> son reales pero no bloquean: van debajo del top-3.

## Notas para el corrector
- Aceptar asignaciones de heurística defendibles distintas cuando hay solapamiento (el número de estado puede
  argumentarse como H2 *o* H6 *o* H4 — lo importante es que justifique). Penalizar solo el "se ve feo" sin
  nombre y la heurística claramente equivocada (p. ej. llamar H8 a la falta de loading).
- Un excelente nota que `ERR_PAYLOAD_413` además **filtra jerga interna** (roce de seguridad/comunicación) y
  que el empty de la tabla es onboarding desperdiciado, no solo "falta un texto".
