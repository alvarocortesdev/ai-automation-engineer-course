---
ejercicio_id: fase-0/http-con-curl
fase: fase-0
sub_unidad: "0.4"
version: 1
---

> 🚫 **SPOILER — material para el CORRECTOR, no para el alumno.** No pegues ni parafrasees de forma reconstruible. Úsalo para detectar el error, nombrar la misconception y graduar pistas. Las salidas reales cambian con el tiempo y el sitio; lo que importa es que la **interpretación** del alumno calce con su captura.

# Solución de referencia — Inspecciona HTTP real con `curl`

## Respuesta canónica (qué debería observar y concluir)

El ejercicio depende de sitios vivos, así que no hay un status fijo por caso. Vara de corrección por caso:

### Caso 1 — `2xx`
`curl -I https://example.com` devuelve típicamente `HTTP/2 200` con `content-type: text/html`. **Conclusión correcta:** familia `2xx` = éxito; el servidor devolvió un recurso HTML. Si el sitio no acepta `HEAD`, puede dar `405`; en ese caso lo correcto es repetir con `GET` (`-s -o /dev/null -w "%{http_code}"`).

### Caso 2 — `4xx`
Una ruta inexistente da `404 Not Found`. **Conclusión correcta:** `4xx` = error del **cliente** (pedí algo que no existe). Punto fino: el servidor **respondió**; no está caído. Es un `404` y no un `403` porque el recurso no existe (no es un tema de permisos).

### Caso 3 — `3xx`
`curl -I http://github.com` devuelve un `301 Moved Permanently` con header `location: https://github.com/` (o similar). Con `curl -IL` se **sigue** la cadena y el status final es `2xx`. **Conclusión correcta:** `3xx` = redirección; el `location` dice a dónde; el navegador lo seguiría solo. Variantes válidas: `301`, `302`, `307`, `308`, o redirección raíz→`www`. Lo que importa es que identifique el `location` y entienda que `-L` sigue la cadena.

### Caso 4 — `http` vs `https`
En `curl -v https://example.com`, las líneas con `*` muestran el handshake TLS (`* TLSv1.3 ... `, `* Server certificate:`, `* SSL connection using ...`). **Conclusión correcta:** `https` agrega una capa TLS que **cifra todo el canal** y **verifica la identidad** del servidor con un certificado; `http` no tiene nada de eso (viaja en claro).

### Cierre — `4xx` vs `5xx`
`4xx` = la **petición** tiene el problema (cliente): ruta mala, no autenticado, sin permiso, demasiadas peticiones. `5xx` = el **servidor** falló al procesar una petición válida: `500` (bug interno), `502/504` (un proxy delante no obtuvo respuesta del backend), `503` (no disponible/sobrecargado). En `curl` se ven igual de fácil en la línea de estado; la diferencia es **de quién es la culpa**.

## Razonamiento paso a paso (para explicar, no solo marcar)

La habilidad central es **leer la primera línea** y razonar por familias antes de mirar el detalle:
- 1er dígito `2` → ok · `3` → "ve a otro lado" (busca `location`) · `4` → tú te equivocaste · `5` → el server se equivocó.
- Headers como **evidencia**: `content-type` dice qué es, `location` dice a dónde, `content-length` cuánto pesa.
- TLS es una **capa**, no un estado de HTTP: por eso aparece en el `-v` (capa de transporte/seguridad), no en la línea de estado HTTP.

Si el alumno hace eso, puede diagnosticar cualquier respuesta nueva. Si solo memorizó "404 = no encontrado", se traba con un `502` o un `429`.

## Puntos resbalosos / variantes
- **`HEAD` no soportado (`405`):** algunos sitios rechazan `-I`; la salida correcta es cambiar a `GET`. No es error del alumno.
- **Cadenas de redirección múltiples:** `http`→`https`→`www` puede encadenar dos `3xx`; con `-IL` se ven todos los saltos. Válido.
- **HTTP/2 o HTTP/3:** la línea de estado puede decir `HTTP/2 200` (sin "OK" textual). No es error; HTTP/2+ no manda la frase de razón.
- **Sin red / DNS falla:** `curl` da error de conexión, **no** un status HTTP. Buen contraste: un fallo de DNS/red no es lo mismo que un `5xx` (no hubo respuesta HTTP).
- **`429 Too Many Requests`:** es `4xx` (cliente) aunque "se siente" como culpa del server; útil para discutir.

## Rango de soluciones aceptables
- Cualquier elección de sitios es válida mientras las capturas sean reales y las conclusiones calcen con ellas.
- Se acepta usar `GET` en vez de `HEAD` si el sitio no soporta `-I`.
- Se acepta cualquier `3xx` real para el caso de redirección.
- **Penalizar** solo: clasificación incoherente con la salida pegada, llamar "caído" a un `404`, no encontrar el `location`, o conclusiones sin evidencia (afirmar algo que la captura no muestra).
