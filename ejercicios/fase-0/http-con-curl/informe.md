# Mi informe — Inspección HTTP con curl

> Esqueleto del entregable. Para cada caso: **predicción → salida real → conclusión**.
> Predice el status **antes** de correr el comando. Borra esta cita cuando empieces.

## Caso 1 — Un `2xx` (éxito)

- **Comando:** `curl -I https://example.com`
- **Mi predicción (antes de correr):** status `<...>`
- **Salida relevante:**
  ```
  <pega aquí la línea de estado y los headers content-type / content-length>
  ```
- **Conclusión:** `<¿qué familia es? ¿qué tipo de contenido devolvió?>`

## Caso 2 — Un `4xx` (error del cliente)

- **Comando:** `curl -s -o /dev/null -w "%{http_code}\n" https://example.com/ruta-que-no-existe`
- **Mi predicción:** status `<...>`
- **Salida real:** `<...>`
- **Conclusión:** `<por qué este código y no otro; ¿de quién es la "culpa"?>`

## Caso 3 — Una redirección `3xx`

- **Comandos:** `curl -I http://<sitio>` y luego `curl -IL http://<sitio>`
- **Mi predicción:** primer status `<...>`, status final `<...>`
- **Salida relevante (sin -L):**
  ```
  <pega la línea de estado 3xx y el header location>
  ```
- **Salida relevante (con -L):**
  ```
  <pega el status final tras seguir la cadena>
  ```
- **Conclusión:** `<a dónde te mandó y por qué el navegador haría lo mismo automáticamente>`

## Caso 4 — `http://` vs `https://`

- **Comando:** `curl -v https://example.com 2>&1 | head -n 20`
- **Líneas del TLS que encontré:**
  ```
  <pega las líneas con * que mencionan TLS / SSL / certificate>
  ```
- **Conclusión:** `<qué te da https que http no, en una frase>`

## Cierre — `4xx` vs `5xx`

`<2–3 frases: en qué se diferencian y cómo los verías en curl>`
