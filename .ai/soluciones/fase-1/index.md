---
ejercicio_id: fase-1/index
fase: fase-1
sub_unidad: "1.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).
> Ojo: este ejercicio es de **diseño personal**. No existe una única respuesta
> correcta; esta es una **referencia ejemplar** + el criterio para juzgar otras.

# Solución de referencia — Diagnóstico de entrada y plan de Fase 1

## Respuesta canónica (ejemplo de entrega "excelente")

### 1. `diagnostico.md` (ejemplo para un cero real)

| Sub-unidad | Pista | Nivel | Por qué |
|---|---|---|---|
| 1.1 Python básico | Python | nuevo | Nunca escribí Python; no sé qué es un dict. |
| 1.2 Python intermedio | Python | nuevo | No sé qué es un generador ni un decorador. |
| 1.3 Python asíncrono | Python | nuevo | No he visto `async`; ni sé qué problema resuelve. |
| 1.4 Type hints + pydantic | Python | nuevo | No conozco el tipado de Python ni la validación. |
| 1.5 Archivos, JSON y APIs | Python | lo reconozco | He visto JSON; nunca llamé una API desde código. |
| 1.6 Primer test unitario | Python | nuevo | Nunca escribí un test. |
| 1.7 JavaScript moderno | TypeScript | lo reconozco | Toqué algo de JS copiando snippets; no domino closures. |
| 1.8 TypeScript desde cero | TypeScript | nuevo | No sé qué es un tipo ni un generic. |
| 1.9 Errores idiomáticos | (opcional) | nuevo | No sé la diferencia entre excepción y `Result`. |
| 1.10 Primer LLM + mini-CLI | Python | nuevo | Nunca llamé a un modelo por API. |

> **Clave de corrección:** los niveles **dependen del alumno**. Para un perfil
> oxidado-con-experiencia, 1.1, 1.5 o 1.7 pueden ser legítimamente "lo sé hacer
> sin notas" → Primero-Sin-IA de entrada, y sería igualmente válido. Lo que **no**
> es válido: marcar "lo sé hacer" sin poder defenderlo, o no asignar la pista.

### 2. `plan-fase-1.md` (ejemplo a 12 h/sem, con las dos pistas alternadas)

- **Bloques fijos:** Lun/Mié/Vie 20:00–21:00 (pista Python, la larga) · Sáb
  10:00–12:00 (proyecto + repaso). **Mar 20:00–21:00 reservado a la pista
  TypeScript** una semana de cada dos, para que no se enfríe.
- **Orden / alternancia:** avanzo Python 1.1 → 1.6 como columna; intercalo 1.7–1.8
  (TS) un bloque por semana desde la semana 2; 1.9 (opcional) la dejo para repaso.
- **Victoria-IA (1.10):** la agendo **en cuanto cierre 1.5** (sé leer JSON y llamar
  una API). Es la zanahoria: ver un LLM responder desde mi propia CLI sostiene la
  motivación para volver a la columna Python.
- **Ritual de repaso (recall + spacing):**

  | Hito | Acción de recuperación |
  |---|---|
  | Mismo día | Resumen de 3 líneas de memoria. |
  | +1 día | Reescribir la función/idea sin mirar. |
  | +3 días | Re-derivar un caso **nuevo** del mismo concepto. |
  | +1 semana | Explicárselo a alguien o quiz rápido. |

### 3. `por-que-dos-lenguajes.md` (ejemplo)

> El curso pide **Python** porque es donde se sirve casi toda la IA en producción:
> los SDK de los modelos, FastAPI y los pipelines de datos son Python. Es mi puente
> directo a la especialización IA. Pide **TypeScript** porque es el filtro #1 de
> las ofertas fullstack: sin él, un buscador automático me descarta antes de la
> entrevista, y es el lenguaje del frontend (React/Next.js) que viene en la Fase 4.
> Usaría Python para el backend de IA, scripts y automatizaciones; TypeScript para
> la interfaz y para cualquier rol fullstack. Y noto que `pydantic` (Python) y
> `zod` (TS) son el **mismo hábito** —validar datos en el borde— en dos idiomas.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **El diagnóstico se mide con una prueba operativa,** no con una sensación:
   "¿podría resolver un ejercicio del tema, ahora, sin notas ni IA?". Si dudo, no
   es "lo sé hacer".
2. **Interleaving, no bloques.** Alternar Python y TS fija mejor cada uno que hacer
   toda una pista y luego la otra (que además deja una enfriándose semanas).
3. **La victoria-IA va temprano.** 1.10 es la Pista B del curso: el "para esto
   vine". Agendarla tras 1.5 mantiene la motivación del que entró por la IA.
4. **El orden Python importa:** básico → intermedio → asíncrono. Decoradores y
   `async` son soluciones a problemas que aún no se tienen; saltar ahí es copiar
   magia.
5. **Repaso = recuperación distribuida,** no relectura. Reescribir/predecir/enseñar
   en hitos espaciados; releer hasta que "suene familiar" es ilusión de fluidez.

## Puntos resbalosos (donde el corrector debe mirar)
- **Sobreconfianza** en el diagnóstico (todo "lo sé hacer" sin evidencia).
- **Plan sin alternancia** (toda Python, luego todo TS) o **sin agendar la 1.10**.
- **Horario-deseo** sin bloques concretos; repaso por "relectura".
- **Roles de lenguaje** vagos, invertidos o calcados de la portada sin caso propio.
- **Arrancar por lo avanzado** (decoradores/`async`) saltándose 1.1–1.2.

## Rango de soluciones aceptables
- Cualquier horario realista y concreto cuenta, sin importar los días/horas, si
  tiene bloques fijos + alternancia de pistas + victoria-IA agendada + cadencia de
  recall.
- Los niveles del diagnóstico pueden diferir de este ejemplo y seguir siendo
  `excelente` **si la justificación es coherente con la experiencia del alumno** y
  asigna bien la pista.
- La justificación de los dos lenguajes puede enfatizar otra meta (más
  automatización, más fullstack) y seguir siendo válida si da a cada lenguaje un
  **rol concreto** y un caso de uso, no una frase de relleno.
- La cadencia de spacing puede usar otros intervalos (+2/+5/+10) o una app como
  Anki; lo que importa es que sea **recuperación distribuida**, no relectura masiva.
