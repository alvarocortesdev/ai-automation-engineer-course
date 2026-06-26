# Ejercicio 0.4 — Inspecciona HTTP real con `curl`

> **Modalidad: mixta (terminal + escritura, sin IA).** Aquí no predices un modelo abstracto: miras HTTP **de verdad**. `curl` te muestra lo que el navegador esconde — la línea de estado, los headers, la redirección. Leer esto es la forma más básica de **observabilidad**: depurar mirando lo que el sistema te dice, no adivinando.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.4` Cómo funciona la web y un computador
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Capturar respuestas HTTP reales con `curl` y **clasificarlas**: distinguir `2xx`/`3xx`/`4xx`/`5xx`, leer headers para concluir tipo de contenido y si hubo redirección, y comparar `http://` contra `https://` — diagnosticando en cada caso si el problema (si lo hay) es del cliente o del servidor.

## 📋 Contexto

Cuando tu **Capstone F0 (CLI sin IA)** haga una request, vas a tener que leer exactamente esto para saber por qué falló. "Confía en la respuesta sin mirarla" es como manejar con los ojos cerrados. Este ejercicio te enseña a abrir los ojos.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, en la terminal, anotando en `informe.md` (timebox 40 min). **Predice** el status code **antes** de correr cada comando. No le pidas a una IA que interprete la salida: léela tú.
2. Solo entonces consulta **documentación oficial** (MDN status codes, `man curl`).
3. **Solo al final**, usa IA para *revisar* tus conclusiones — no para generarlas.
4. Mañana, repite **una** captura de memoria (sin mirar los flags) y predice los headers antes de verlos.

## 🛠️ Instrucciones

> `curl` viene preinstalado en macOS y Linux. En Windows, está en PowerShell moderno o en WSL. Verifica con `curl --version`.

Captura y documenta en `informe.md` estos cuatro casos. En **cada uno**, escribe tu **predicción del status code antes de correrlo**, luego pega la(s) línea(s) relevante(s) de la salida, y luego tu **conclusión**.

1. **Un `2xx` (éxito).** Pide solo los headers de un sitio que funcione:
   ```bash
   curl -I https://example.com
   ```
   `-I` hace una petición `HEAD` (headers sin body). Anota el status, el `content-type` y el `content-length`.

2. **Un `4xx` (error del cliente).** Pide un recurso que no existe y muestra solo el código:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://example.com/ruta-que-no-existe
   ```
   `-s` silencia el progreso · `-o /dev/null` descarta el body · `-w "%{http_code}"` imprime solo el código. ¿Por qué este número y no otro?

3. **Una redirección `3xx` y seguirla.** Encuentra una URL que redirija (pista fuerte: muchos sitios redirigen de `http://` a `https://`, o de la raíz a `www`). Primero **sin** seguir, luego **siguiendo** con `-L`:
   ```bash
   curl -I http://github.com
   curl -IL http://github.com
   ```
   Anota el primer status (`3xx`) y el header `location` que dice **a dónde** te mandan; luego el status final tras seguir la cadena.

4. **`http://` vs `https://`.** Compara la misma idea cifrada y sin cifrar. Usa `-v` (verbose) para ver el handshake:
   ```bash
   curl -v https://example.com 2>&1 | head -n 20
   ```
   Busca en la salida las líneas del **TLS handshake** (empiezan con `*`, mencionan `TLS`/`SSL`/`certificate`). Explica en una frase qué te da `https` que `http` no.

Al final del informe, escribe **2–3 frases** que respondan: ¿en qué se diferencia un error `4xx` de uno `5xx`, y cómo lo verías en `curl`?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los cuatro casos están capturados con **predicción → salida real → conclusión**.
- [ ] Clasificas correctamente cada status en su familia (`2xx`/`3xx`/`4xx`/`5xx`) y dices qué significa.
- [ ] En la redirección, identificas el header `location` y el status final tras `-L`.
- [ ] Señalas en la salida de `-v` **dónde** ocurre el TLS y qué aporta frente a `http`.
- [ ] Distingues `4xx` (culpa del cliente) de `5xx` (culpa del servidor) con un ejemplo de cada uno.
- [ ] Puedes **explicar cualquier captura sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Si un comando se queda colgado, agrega `--max-time 10` para que corte a los 10 segundos. Si `curl -I` te da un `405 Method Not Allowed`, ese sitio no acepta `HEAD`: usa `curl -s -o /dev/null -w "%{http_code}\n" <url>` (que hace `GET`). Para la redirección, recuerda que el header `location` solo aparece en respuestas `3xx`; si no lo ves, el sitio no redirige y necesitas otro. Revisa la sección 7 de la lección (status codes) antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/http-con-curl/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tus **conclusiones** (clasificación y diagnóstico), no solo si pegaste salidas. La **solución de referencia** vive en `.ai/soluciones/fase-0/http-con-curl.md` — no la mires antes de intentarlo.
