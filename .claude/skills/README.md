# Skills de re-iteración del curso

Dos agent skills para **mantener y crecer** el curso AI/Automation Engineer con IA, sin perder la coherencia pedagógica del diseño original (anatomía de lección, hilos transversales, Definition of Done, rúbricas).

| Skill | Para qué | Punto de entrada |
|---|---|---|
| **`extender-curso`** | Añadir, expandir, reordenar, marcar opcional o corregir una lección/sub-unidad respetando la ANATOMÍA DE LECCIÓN estándar y los hilos transversales. Incluye el CONTRATO DE LECCIÓN como template copiable. | `extender-curso/SKILL.md` |
| **`corregir-ejercicio`** | Corregir la entrega de un alumno usando el framework `.ai/` (rúbrica + solución privadas), con feedback socrático y anti-spoiler. | `corregir-ejercicio/SKILL.md` |

## Cómo invocarlas

- **Slash command:** escribe `/extender-curso` o `/corregir-ejercicio` en Claude Code.
- **Skill tool:** se cargan automáticamente cuando la tarea calza con su `description`.
- Son **agent skills**: una carpeta por skill con un `SKILL.md` que lleva frontmatter `name` + `description`.

## Cuándo usar cada una

- ¿Vas a escribir o tocar **contenido**? → `extender-curso`.
- ¿Vas a **evaluar el trabajo** de quien estudia? → `corregir-ejercicio`.

Son complementarias: `extender-curso` produce la lección **y** sus artefactos privados (`.ai/rubricas/…`, `.ai/soluciones/…`); `corregir-ejercicio` los consume para graduar sin filtrar la respuesta. La rúbrica que una escribe es exactamente la que la otra aplica.

## Mapa de rutas del framework (referencia rápida)

> `fase-N` = `fase-0`…`fase-8` o `track-0`. `<slug>` = `<id>-<kebab-corto>`, p.ej. `6.0b-puente-ml-dl`.

| Artefacto | Ruta | Visibilidad |
|---|---|---|
| Lección publicable (Astro Starlight) | `src/content/docs/fase-N/<slug>.md` | Pública |
| Ejercicios (enunciados + andamiaje) | `ejercicios/fase-N/<slug>/` | Pública |
| Rúbrica de corrección | `.ai/rubricas/fase-N/<slug>.md` | Privada |
| Solución de referencia anotada | `.ai/soluciones/fase-N/<slug>/` | Privada |
| Instrucciones del corrector | `.ai/INSTRUCCIONES-CORRECTOR.md` | Privada |
| Dashboard de avance | `progreso.md` | Pública |

**Regla dura:** nada de `.ai/` se enlaza desde la lección pública. La solución que ve el alumno para autocorregirse es un bloque revelable *dentro* de la lección, no la de `.ai/`.

## Insumos de contrato

Ambas skills se apoyan en `ROADMAP.md` (ids/títulos oficiales) y en `CURRICULUM-REVIEW.md` cuando está presente (sección **E** anatomía+rúbrica, **B** hilos transversales+DoD, **D** build list con marcas ruta-crítica/opcional).

## Reglas comunes

- Español latino estándar (tuteo) o chileno natural; términos técnicos en **inglés**.
- **Prohibido el voseo argentino** y sus modismos.
- Sin trailers de co-autoría de Claude en commits. Estas skills **no** hacen commit salvo petición explícita.
- No tocar `src/` de configuración ni `package.json`.
