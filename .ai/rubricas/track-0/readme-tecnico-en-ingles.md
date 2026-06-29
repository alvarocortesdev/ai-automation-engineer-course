---
ejercicio_id: track-0/readme-tecnico-en-ingles
fase: track-0
sub_unidad: "T0.1"
version: 1
---

# Rúbrica — Escribe un README técnico en inglés

> Rúbrica **analítica** atada a los `objetivos` del contrato. Se evalúa la **claridad y
> corrección del inglés técnico** y el uso de las convenciones de README, **no** cuán
> impresionante sea el proyecto. Un script de 10 líneas con un README impecable supera a
> un proyecto grande con inglés de traductor. El corrector NO reescribe el README por el
> alumno: marca patrones y gradúa pistas.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Producir un README en inglés con las secciones convencionales
  (título+descripción, Requirements, Usage, Example).
- **O2** — Distinguir el inglés de traductor del inglés técnico idiomático y corregir
  patrones frecuentes (conjugación, verbos técnicos, propósito con "to + verbo").
- **O3** — Construir un glosario personal ES→EN de términos técnicos reales del proyecto.

## Criterios y niveles

### C1 — Estructura y convenciones del README · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta(n) sección(es); o es prosa corrida sin encabezados; o no hay comando de uso ni ejemplo. |
| **en-progreso** | Tiene las secciones pero el ejemplo es vago/inexistente, o el Usage no trae el comando exacto, o el orden confunde al lector (Usage antes que Requirements). |
| **competente** | Las 4 secciones presentes y en orden lógico; descripción de **una frase**; Usage con el **comando exacto**; Example con una corrida realista (comando + salida). |
| **excelente** | Además el README es **escaneable** (títulos cortos, listas), el ejemplo es verosímil y autoexplicativo, y el título sigue convención (minúsculas, sin "My Project"). |

### C2 — Calidad del inglés técnico (idiomático, no traducción) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Traducción literal evidente y constante ("show in the screen", "for install", "execute the program"); errores de conjugación en casi toda frase. |
| **en-progreso** | Se entiende, pero con errores recurrentes: 3ª persona sin "s" ("it count"), "for + verbo" en vez de "to + verbo", verbos no técnicos ("give back" por "returns"). |
| **competente** | Gramática correcta en lo esencial; verbos técnicos idiomáticos (run/build/install/returns/raises); imperativos directos en Usage; sin calcos del español. |
| **excelente** | Inglés natural y conciso; usa convenciones de la industria (stdout, payload, by default, sorted by…) con naturalidad; ninguna frase "huele a traductor". |

### C4 — Comprensión demostrada: glosario propio · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin glosario, o menos de 8 entradas, o entradas que el alumno no usó (copiadas del starter sin añadir las propias). |
| **en-progreso** | 8 entradas pero genéricas/de lista, no las que de verdad le costaron; alguna traducción literal en la columna inglesa. |
| **competente** | 8 términos **reales del proyecto** con su forma idiomática correcta; se nota que salieron del esfuerzo de escribir el README. |
| **excelente** | Términos no triviales (los que un principiante traduciría mal) con la forma idiomática exacta; opcionalmente una nota de por qué el calco estaba mal. |

<!-- C3 (Seguridad) y C5 (Observabilidad/eval) no aplican: ejercicio de comunicación de Track-0. -->

## Errores típicos a marcar
- **Inglés de traductor:** "show in the screen", "for install", "execute the program",
  "the file not exists", "give back the data". Marcar el patrón, no solo la palabra.
- **3ª persona del singular sin "s":** "the function return", "it count". Sistemático.
- **Propósito mal construido:** "for install" / "for run" en vez de "to install" / "to run".
- **Orden de secciones ilógico:** Usage antes que Requirements (el lector se traba sin tener instalado lo necesario).
- **Ejemplo decorativo o ausente:** "the program shows the result" sin una corrida real.
- **README inflado:** párrafos de marketing en vez de claridad técnica.
- (transversal spec-driven) No versiona el README ni usa el commit pedido; trata el doc como descartable.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- README en inglés **perfecto y sofisticado** (voz pasiva impecable, vocabulario avanzado)
  pero el alumno **no puede leerlo en voz alta sin trabarse** ni explicar por qué eligió una
  frase — sofisticación impropia de F0/Track-0 sin defensa.
- El `glosario.md` no contiene los errores típicos de un principiante (todo "ya idiomático"),
  lo que sugiere que no hubo lucha real con el idioma.
- **Verificación sugerida:** pedir que **traduzca en vivo** una frase técnica nueva no
  presente en el README (p. ej. "esta función valida el payload y lanza un error si falta un
  campo"). Si interiorizó los patrones, sale en segundos; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca redactar el README por el alumno. De menos a más directo.

- **Pista (nivel 1):** "Lee tu sección Usage en voz alta. ¿Hay alguna frase que suene a
  traducción literal del español? Empieza por ahí."
- **Pregunta socrática (nivel 2):** "En 'the function return the sum', ¿qué persona y número
  es el sujeto? ¿Cómo se conjuga un verbo en inglés para 'it'?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tienes tres calcos del mismo
  patrón: usas 'for + verbo' para indicar propósito. En inglés el propósito se construye con
  'to + verbo' ('to install', 'to run'). Corrígelos y revisa si hay más del mismo tipo. No te
  doy la versión final: el patrón es lo que tienes que internalizar."

## Conexión con el proyecto / capstone
- Este README es el **molde** del README en inglés que el Definition of Done (§B, punto 8)
  exige en **todos** los capstones (F0 CLI, F3 API, F6 RAG, F7 automatización). Hacerlo bien
  aquí instala el hábito que se repite en cada fase.
