---
ejercicio_id: fase-1/python-basico-intermedio-entornos-modulos
fase: fase-1
sub_unidad: "1.1"
version: 1
---

# Rúbrica — Entornos y módulos, explicados y montados

> Rúbrica **analítica** para un ejercicio **mixto** (razonamiento + setup). No hay tests automáticos: lo que se evalúa es la **predicción correcta del modelo de imports**, los **comandos reproducibles** de los dos entornos, y la **explicación con palabras propias** del aislamiento. Un alumno puede acertar las salidas por suerte; la justificación es lo que demuestra el objetivo.

## Objetivos evaluados
- **O1** — Predecir qué corre al importar un módulo vs. al ejecutarlo directo (guard `__main__`).
- **O2** — Crear y usar un entorno virtual con `venv` y con `uv`, con comandos reproducibles.
- **O3** — Explicar el trade-off del aislamiento de dependencias.

## Criterios y niveles

### C1 — Predicción del modelo de imports (Parte A) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay predicción, o ejecutó antes de predecir (copió la salida). |
| **en-progreso** | Acierta una de las dos salidas pero falla la otra, o no distingue qué línea viene del guard `__main__`. |
| **competente** | Predice ambas salidas correctas y explica que importar ejecuta el nivel superior una vez, y que el guard solo corre al ejecutar directo. |
| **excelente** | Además nombra el valor de `__name__` en cada caso (`"saludo"` al importar, `"__main__"` al ejecutar directo) como la causa raíz. |

### C2 — Entornos montados (Parte B) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No montó ningún entorno, o solo describe sin comandos. |
| **en-progreso** | Montó uno de los dos (`venv` o `uv`), o los comandos no son reproducibles (faltan pasos, activación, instalación). |
| **competente** | Montó ambos: `python -m venv` + activar + instalar + desactivar; y `uv init`/`add`/`run`. Comandos copiables. |
| **excelente** | Además identifica los artefactos generados (`.venv/`, `pyproject.toml`, `uv.lock`) y cuáles se commitean (`pyproject.toml`/`uv.lock` sí; `.venv/` no) con la razón. |

### C3 — Explicación del aislamiento (Parte C) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No explica, o repite la lección textual sin entenderla. |
| **en-progreso** | Explicación vaga ("para no ensuciar") sin el mecanismo (site-packages por proyecto). |
| **competente** | Explica con sus palabras que cada entorno tiene su propio `site-packages`, por eso dos proyectos pueden usar versiones distintas sin chocar. |
| **excelente** | Liga el aislamiento al "works on my machine": el lockfile/reproducibilidad permite que otra máquina recree el mismo entorno exacto. |

## Errores típicos a marcar
- **Creer que el guard `__main__` corre siempre:** predice que `python main.py` imprime `"módulo directo"`. Es el malentendido central.
- **Olvidar que importar ejecuta el `print` de nivel superior:** predice solo `"Hola, Ada"` y omite `"cargando saludo"`.
- **Commitear `.venv/`:** señal de no entender que el entorno se reconstruye y no es código fuente.
- **Confundir `venv` con `uv`** como si fueran rivales, en vez de `uv` creando un `.venv` estándar por debajo.
- **`sudo pip install` global:** justo lo contrario del aislamiento; marcarlo.
- (transversal) Explicación copiada de la lección sin reformular (señal de no interiorizar).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Predicción correcta pero **sin justificar** qué corre al importar (resultado sin proceso).
- Explicación del aislamiento con vocabulario muy por encima del nivel sin poder defenderlo.
- Comandos de `uv` impecables pero que no coinciden con los artefactos que dice haber visto (no los corrió).
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué cambia si en `main.py` se agrega una segunda línea `import saludo` (no se vuelve a ejecutar el nivel superior: los módulos se cachean). Si trazó de verdad, lo razona; si dependió de IA, duda.

## Feedback sugerido (graduado)
> Nunca dar las salidas antes de que cierre su intento.
- **Pista (nivel 1):** "Compara las dos ejecuciones. ¿Qué tiene `python saludo.py` que `import saludo` no? Fíjate en el valor de `__name__` en cada caso."
- **Pregunta socrática (nivel 2):** "Cuando importas un módulo, ¿se ejecuta su código de nivel superior? ¿Y el bloque bajo `if __name__ == '__main__':`? ¿Por qué uno sí y el otro no?"
- **Dirección concreta (nivel 3, solo tras intento real):** "La regla: importar ejecuta el nivel superior **una vez**; el guard `__main__` corre **solo** al ejecutar el archivo directo, porque ahí `__name__` vale `'__main__'`. Reescribe tu predicción marcando, línea por línea, de dónde sale cada salida."

## Conexión con el proyecto / capstone
- Montar el entorno con `uv` y entender módulos/imports es el **paso 0 del Capstone F1**: antes de escribir la mini-API se crea el proyecto, su `.venv` y su estructura de paquete. Equivocarse aquí es el bug que rompe el "demo que corre" del Definition of Done.
