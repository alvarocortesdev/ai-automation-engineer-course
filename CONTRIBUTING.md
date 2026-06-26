# Contribuir

Gracias por querer mejorar este curso. Es un repositorio de **conocimiento libre**: cada mejora —una
lección más clara, un ejercicio mejor, una corrección factual, una traducción— le sirve a la próxima
persona que está reconstruyendo su autonomía. Las contribuciones se reciben con gusto.

## Tipos de contribución

- **Correcciones factuales / de actualidad:** versiones de librerías, APIs, mejores prácticas
  vigentes. La tecnología se mueve rápido; mantenerla al día es la contribución más valiosa.
- **Mejoras pedagógicas:** mejores analogías, *worked examples*, errores comunes, diagramas.
- **Ejercicios y rúbricas:** nuevos ejercicios Primero-Sin-IA, casos de prueba, criterios de
  corrección.
- **Traducciones:** prosa a otros idiomas (ver política de idioma).
- **Erratas y enlaces rotos.**

Para cambios grandes (una sub-unidad nueva, reestructurar una fase), abre primero un **issue** para
acordar el enfoque antes de invertir tiempo.

## Cómo extender el curso

El curso se genera siguiendo un **contrato de lección** estricto. La forma recomendada de añadir o
extender contenido es la skill **`extender-curso`** en `.claude/skills/extender-curso/`, que conoce
el contrato, la estructura de carpetas y el estándar de rúbrica. Para corregir entregas de
ejercicios, usa `.claude/skills/corregir-ejercicio/`.

Si prefieres hacerlo a mano, respeta el estándar de abajo.

## Estándar de lección

Cada sub-unidad vive en `src/content/docs/fase-N-<slug>/<NN-subunidad>.mdx` y debe incluir, en este
orden:

1. **Frontmatter** con `title` y `description`.
2. **Objetivos observables (1–3)** — verbos medibles de Bloom (*implementar*, *explicar el
   trade-off*, *depurar*, *diseñar*). Lo que sabrás **hacer**, no "conocer".
3. **Hook / por qué importa** — relevancia de mercado y conexión con la carrera (reusa el "💰" del
   ROADMAP).
4. **Activación de conocimiento previo** — recuperación de lo anterior; prerrequisitos como
   wikilinks a sub-unidades previas.
5. **Worked example** — el experto razona en voz alta (no solo el resultado).
6. **Non-examples + misconceptions** — "podrías pensar X; aquí por qué está mal" (callouts
   `:::caution`).
7. **Práctica con andamiaje que se desvanece** — completar/Parsons → independiente.
8. **Ejercicios Primero-Sin-IA con timebox (25–45 min)** — cada uno con enunciado, criterios de
   "hecho", pista colapsable, link al scaffold en `ejercicios/` y a la rúbrica en `.ai/rubricas/`.
   Cada ejercicio trae **solución de referencia + errores comunes**.
9. **Check de dominio (active recall)** — "explícalo sin notas" / predecir salida.
10. **Recursos** — documentación oficial primero.
11. **Conexión con el proyecto** de la fase (constructive alignment).

> Para F0–F1, usa **PRIMM** (Predict–Run–Investigate–Modify–Make) y **Parsons problems**.

Cada ejercicio genera, además de la lección:

- Scaffold en `ejercicios/fase-N/<slug>/` — README (enunciado) + starter + tests (sigue
  `ejercicios/plantilla-ejercicio/`).
- Rúbrica en `.ai/rubricas/fase-N/<slug>.md`.
- Solución de referencia en `.ai/soluciones/fase-N/<slug>/` (marcada como spoiler; es para el
  corrector, no para el estudiante).

### Principios transversales

Donde corresponda, inyecta los hilos transversales: clean code, SOLID (con crítica), TDD,
spec-driven dev, seguridad (OWASP web + LLM/Agentic), observabilidad, evals de IA, costo/latencia.
La calidad **no es una fase posterior**: se teje desde el día 1.

## Conventional Commits

El historial usa [Conventional Commits](https://www.conventionalcommits.org/). Formato:

```text
<tipo>(<ámbito opcional>): <descripción en imperativo>
```

Tipos: `feat`, `fix`, `docs`, `content`, `style`, `refactor`, `test`, `chore`, `ci`.

Ejemplos:

```text
content(fase-6): añade lección 6.7 RAG con failure-mode diagnosis
fix(ejercicios): corrige caso borde en test de fase-1/cli-despensa
docs(readme): aclara el framing de plazos
```

Mantén el historial limpio y los mensajes en español (la descripción), con los términos técnicos en
inglés.

## Política de idioma

- **Prosa: español.** Los **términos técnicos** se mantienen en inglés (*embedding*, *prompt*,
  *retrieval*, *tool calling*, *idempotency*…). No los traduzcas.
- **Español neutro / latino estándar o chileno natural.** Tuteo: *puedes*, *tienes*, *implementa*,
  *revisa*, *fíjate*.
- **Prohibido el voseo rioplatense** (*podés*, *tenés*, *revisá*, *fijate*, *sos*…) y los modismos
  argentinos. Es una regla dura de este repositorio.
- **Código, identificadores y nombres de archivo:** en inglés o kebab-case según convención del
  stack; consistentes con el código existente.

## Estilo

- Markdown / MDX con componentes de Astro Starlight (callouts `:::note`, `:::tip`, `:::caution`).
- Diagramas con **Mermaid** cuando ayuden a entender un proceso o arquitectura.
- Bloques de código siempre con su etiqueta de lenguaje.
- Documentación oficial por sobre tutoriales sueltos.

## Licencia de tus contribuciones

Al contribuir aceptas que tu aporte se publique bajo la **licencia dual** del repositorio: contenido
bajo **CC BY-SA 4.0** y código bajo **MIT** (ver [`LICENSE`](./LICENSE) y
[`LICENSE-CODE`](./LICENSE-CODE)).
