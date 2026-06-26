# Ejercicio 1.1 — Entornos y módulos, explicados y montados

> **Modalidad: mixto (Primero-Sin-IA).** Mitad razonamiento (predecir imports sin ejecutar), mitad
> manos (montar entornos virtuales reales). No hay tests automáticos: el corrector evalúa tu
> **razonamiento** y tus **comandos reproducibles**.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.1` Python de básico a intermedio
**Ruta:** crítica · **Timebox:** 30–35 min

## 🎯 Objetivo

Predecir qué código corre al **importar** un módulo vs. al **ejecutarlo directo**, y montar un
entorno virtual aislado con `venv` y con `uv`, explicando por qué el aislamiento evita el "en mi
máquina funciona".

## 📏 Primero-Sin-IA

1. Haz la **predicción a mano, sin ejecutar y sin IA**.
2. Solo después, ejecuta para verificar.
3. Usa IA al final para *revisar* tu explicación, no para escribirla.

## Parte A — Puzzle de imports (predice sin ejecutar)

Tienes dos archivos en la misma carpeta:

```python
# saludo.py
mensaje = "cargando saludo"
print(mensaje)


def saludar(nombre):
    return f"Hola, {nombre}"


if __name__ == "__main__":
    print(saludar("módulo directo"))
```

```python
# main.py
import saludo

print(saludo.saludar("Ada"))
```

Sin ejecutar nada, predice y **justifica**:

1. ¿Qué imprime `python main.py`? (línea por línea, en orden)
2. ¿Qué imprime `python saludo.py` (ejecutar el módulo directo)?
3. ¿Por qué la línea bajo `if __name__ == "__main__":` aparece en un caso y no en el otro?

## Parte B — Monta los entornos (manos)

1. Crea un entorno con **`venv`**: créalo, actívalo, instala una librería (p. ej. `requests`),
   comprueba que quedó instalada solo ahí, desactívalo. Registra los comandos **exactos**.
2. Crea un proyecto con **`uv`**: `uv init`, `uv add` de una librería, corre algo con `uv run`.
   Registra los comandos.
3. Mira qué archivos/carpetas se generaron (`.venv/`, `pyproject.toml`, `uv.lock`). ¿Cuáles
   commitearías y cuáles no?

## Parte C — Explica el aislamiento

En 3–5 frases, con tus palabras: **por qué** un entorno virtual evita el "works on my machine".
Pista de encuadre: imagina dos proyectos que necesitan versiones distintas de la misma librería.

## ✅ Qué entregar (deja este archivo en esta carpeta)

- `RESPUESTAS.md` con:
  - **Parte A:** las dos salidas predichas + la justificación del guard `__main__`.
  - **Parte B:** la transcripción de comandos de `venv` y de `uv`, y qué se commitea y qué no.
  - **Parte C:** tu explicación del aislamiento (sin copiar la lección).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Predijiste ambas salidas **antes** de ejecutar y nombraste qué corre al importar vs. directo.
- [ ] Montaste un entorno con `venv` y otro con `uv`, con comandos reproducibles.
- [ ] Identificaste que `.venv/` no se commitea (y por qué) y que `pyproject.toml`/`uv.lock` sí.
- [ ] Explicaste el aislamiento con tus palabras, no copiando.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

**Importar un módulo ejecuta su nivel superior una vez** (la asignación y el `print` de `saludo.py`
corren). Pero el bloque bajo `if __name__ == "__main__":` corre **solo** cuando ejecutas ese archivo
directo, porque ahí `__name__` vale `"__main__"`; al importarlo, `__name__` vale `"saludo"`. Para el
aislamiento: piensa dónde "viven" los paquetes de cada proyecto — en el `site-packages` propio de
cada `.venv`. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `RESPUESTAS.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/python-basico-intermedio-entornos-modulos.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en
`.ai/soluciones/fase-1/python-basico-intermedio-entornos-modulos.md` — no la mires antes de
intentarlo de verdad.
