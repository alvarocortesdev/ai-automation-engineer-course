# Ejercicio 0.4 — Anatomía de una URL y su viaje

> **Modalidad: a mano (sin ejecutar, sin IA).** Entrenas el modelo mental del sistema completo: predecir qué pasa entre tu Enter y la página, igual que en [0.3] predecías la salida de un bucle. Si puedes contar el viaje sin abrir nada, lo entendiste. Si necesitas buscar "qué pasa cuando escribo una URL" para reconstruirlo, todavía no.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.4` Cómo funciona la web y un computador
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Descomponer una URL real en sus partes y **predecir, paso a paso y sin ejecutar nada**, el recorrido de la petición desde DNS hasta el render, nombrando IP, puerto, TCP, TLS y el método HTTP — e identificando qué parte de la URL **no** viaja al servidor.

## 📋 Contexto

Esta es la pregunta de entrevista "¿qué pasa cuando escribo una URL y aprieto Enter?". También es el modelo que necesitas para que tu **Capstone F0 (CLI sin IA)** construya URLs correctas y maneje respuestas sin caerse. Si el viaje no está claro en tu cabeza, depuras a ciegas.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo, a mano**, en `recorrido.md` (timebox 35 min). No abras `curl`, no abras el navegador con DevTools, no preguntes a una IA.
2. Solo entonces consulta **documentación oficial** (MDN, Cloudflare Learning).
3. **Solo al final**, usa IA para *revisar y explicar* tu recorrido — no para escribirlo.
4. Mañana, **reescribe los pasos de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Elige una URL **real y completa** — que tenga al menos esquema, host, ruta y `query string`; idealmente también un `#fragmento`. Ejemplos válidos: una búsqueda en un sitio que uses, una URL de tu propio dominio, una página de documentación con anclas. **Evita** una URL pelada tipo `https://google.com` (no tiene query ni fragmento que analizar).

Completa `recorrido.md` con dos entregables:

1. **Tabla de descomposición** de la URL: una fila por parte (esquema, host, puerto efectivo, ruta, query, fragmento). Para el puerto, si la URL no lo trae explícito, di cuál es el **efectivo** y por qué (pista: depende del esquema).
2. **Recorrido numerado** del viaje: desde que el navegador parsea la URL hasta que pinta la página. En cada paso nombra la pieza que actúa (DNS, IP, puerto, TCP, TLS, método HTTP, status code esperado, render). Marca **explícitamente** qué parte de la URL NO se envía al servidor y por qué.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla descompone **todas** las partes presentes en tu URL, con el puerto **efectivo** justificado.
- [ ] El recorrido tiene los pasos en **orden correcto** (nombre → número → canal → cifrado → pregunta → respuesta → render).
- [ ] Nombras IP, puerto, TCP, TLS y el método HTTP donde corresponde, no como adorno.
- [ ] Identificas qué parte de la URL **no viaja** al servidor y das la razón.
- [ ] Lo escribiste **sin ejecutar nada y sin IA**, y puedes **explicarlo sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El orden es siempre el mismo y cada paso **habilita** al siguiente: no puedes abrir TCP sin una IP, no puedes cifrar (TLS) sin canal TCP, no puedes hablar HTTP sin cifrado (en `https`). Para el "qué no viaja": piensa qué parte de la URL sirve para moverte **dentro** de una página ya descargada — eso lo resuelve el navegador, no el servidor. Revisa la sección 4 de la lección (el ejemplo resuelto) antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/anatomia-de-una-url/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **razonamiento** (el orden y el porqué), no si memorizaste una lista. La **solución de referencia** vive en `.ai/soluciones/fase-0/anatomia-de-una-url.md` — no la mires antes de intentarlo de verdad.
