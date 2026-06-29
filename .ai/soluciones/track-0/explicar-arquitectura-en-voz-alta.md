---
ejercicio_id: track-0/explicar-arquitectura-en-voz-alta
fase: track-0
sub_unidad: "T0.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de
> medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio
> es de **comunicación hablada + auto-diagnóstico**: no hay una única respuesta correcta;
> esta es una **referencia ejemplar** + el criterio para juzgar otras.

# Solución de referencia — Explica tu arquitectura en voz alta, en inglés

## Respuesta canónica (ejemplo de entrega "excelente")

Mismo proyecto de ejemplo: el contador de frecuencias de palabras.

### `transcript.md` (lo que un alumno B2 podría decir, ~75s, honesto)

> "Okay, so, it's a small CLI tool that counts word frequencies in a text file. The flow
> is: it reads the file, it, um, splits the text into words, it counts them using a
> dictionary, and then it prints each word with its count, sorted by frequency. One
> decision I made: I used a dictionary instead of, eh, sorting the list first, because
> counting is O(n) and I only sort once at the end. What I'd improve — if the file were
> really big, I'd stream it line by line instead of loading the whole thing into memory."

Nota: la transcripción **incluye muletillas** ("um", "eh"). Eso es correcto y esperado:
es una grabación real, no un guion.

### `autoevaluacion.md` (ejemplo)

- 4 movimientos: 1 ✅ · 2 ✅ · 3 ✅ · 4 ✅
- Duración: 75s (en rango).

| # | Lo que dije (trabado) | Corrección idiomática |
|---|------------------------|------------------------|
| 1 | "the whole thing into memory" | "load the entire file into memory" (más técnico) |
| 2 | dudé en "splits" (dije "cuts") | "splits the text into words" |
| 3 | "if the file were really big" (bien, pero lento de armar) | practicar el subjuntivo: "if the file were large" |

- Ataco primero: **velocidad de recuperación de vocabulario técnico** (me trabé buscando
  "splits"); practicaré la frase 2 (the flow) hasta que salga sin pensar.

> **Clave de corrección:** el contenido depende del proyecto del alumno. Lo que se mide es
> (a) los 4 movimientos presentes, (b) una decisión con porqué, y (c) un auto-diagnóstico
> honesto con correcciones. Una transcripción **con** errores y un buen diagnóstico es
> MEJOR que una pulida sin diagnóstico.

## Razonamiento paso a paso (lo que debe entender el alumno)

1. **La estructura de 4 movimientos salva bajo presión.** No se improvisa: se rellenan
   cuatro casillas. Aunque el inglés tropiece, si los 4 están, suena a ingeniero.
2. **El movimiento 3 (decisión + porqué) es el que da seniority.** Sin un trade-off
   defendible, la explicación suena junior por bien pronunciada que esté.
3. **El movimiento 4 (qué mejoraría) demuestra criterio y honestidad**, no debilidad.
4. **Grabarse es el feedback.** La transcripción honesta (con muletillas) es el espejo;
   sin ella no hay diagnóstico, y sin diagnóstico el error se fija.
5. **Inglés hablado bajo presión ≠ inglés social.** Trabarse en vocabulario técnico
   específico es lo normal al principio y lo que este ejercicio entrena.

## Puntos resbalosos (donde el corrector debe mirar)
- **Falta el movimiento 3** (decisión + porqué): el error más frecuente y el más caro.
- **"What I'd improve" genérico** ("make it better", "add features").
- **Transcripción pulida** sin muletillas → sospecha de guion leído o texto generado;
  rompe el propósito del auto-espejo.
- **Auto-diagnóstico sin correcciones** o con menos de 3 puntos.
- **Confundir fluidez social con técnica:** "mi inglés es bueno" pero se trabó justo en
  los términos técnicos (que es lo que importa aquí).

## Rango de soluciones aceptables
- Cualquier proyecto y cualquier nivel de inglés hablado: un B1 trabado **con los 4
  movimientos y buen diagnóstico** es "competente"; no se exige fluidez nativa.
- La decisión técnica puede ser cualquiera real y defendible (estructura de datos,
  librería, patrón, formato de archivo…), siempre con un porqué que contraste alternativas.
- La duración puede ir de 60 a 120s; salir un poco fuera no es descalificante si la
  estructura está.
- El diagnóstico puede priorizar gramática, muletillas o velocidad de vocabulario — lo que
  importa es que sea **honesto, concreto y con correcciones idiomáticas**.
- Es perfectamente válido (y deseable) que la 1ª toma sea floja: el ejercicio mide el
  **proceso de mejora**, no la perfección de la primera grabación.
