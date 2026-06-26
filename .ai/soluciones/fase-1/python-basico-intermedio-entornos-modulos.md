---
ejercicio_id: fase-1/python-basico-intermedio-entornos-modulos
fase: fase-1
sub_unidad: "1.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Entornos y módulos, explicados y montados

## Parte A — Puzzle de imports

### `python main.py`

```text
cargando saludo
Hola, Ada
```

Razonamiento:
1. `import saludo` ejecuta el **nivel superior** de `saludo.py` una vez: asigna `mensaje` y corre su
   `print(mensaje)` → imprime `cargando saludo`.
2. El bloque `if __name__ == "__main__":` de `saludo.py` **NO corre**: al importarse, dentro de
   `saludo.py` la variable `__name__` vale `"saludo"`, no `"__main__"`.
3. Vuelve a `main.py`: `print(saludo.saludar("Ada"))` → `Hola, Ada`.

### `python saludo.py` (ejecutar el módulo directo)

```text
cargando saludo
Hola, módulo directo
```

Razonamiento:
1. Nivel superior: imprime `cargando saludo`.
2. Ahora `__name__ == "__main__"` (lo ejecutas directo), así que el guard **sí corre**:
   `print(saludar("módulo directo"))` → `Hola, módulo directo`.

### La causa raíz
La diferencia es el valor de `__name__`: `"__main__"` cuando ejecutas el archivo directo,
`"<nombre del módulo>"` cuando lo importas. El guard separa "soy una librería que me importan" de
"me están corriendo como programa".

## Parte B — Entornos montados

### `venv` (viene con Python)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install requests
python -c "import requests; print(requests.__version__)"
deactivate
```

### `uv` (estándar moderno del curso)

```bash
uv init demo-uv
cd demo-uv
uv add requests
uv run python -c "import requests; print(requests.__version__)"
```

### Artefactos y qué se commitea
- `.venv/` → **NO** se commitea (va en `.gitignore`): es reconstruible, pesado y específico de la
  máquina.
- `pyproject.toml` → **SÍ**: declara las dependencias del proyecto.
- `uv.lock` → **SÍ**: congela versiones exactas para que otra máquina reproduzca el entorno idéntico.

## Parte C — Por qué evita el "works on my machine"
Cada entorno virtual tiene su **propio** `site-packages`: las dependencias viven dentro del proyecto,
no en el Python del sistema. Así, dos proyectos pueden usar versiones distintas de la misma librería
sin pisarse. Y como `pyproject.toml` + `uv.lock` declaran y congelan esas versiones, cualquiera puede
recrear el **mismo** entorno desde cero (`uv sync`); el "en mi máquina funciona" desaparece porque la
máquina deja de ser la variable: el entorno es explícito y reproducible.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Guard `__main__` "corre siempre":** error central de la Parte A. Si predijo
   `Hola, módulo directo` para `python main.py`, no entendió la importación.
2. **Omitir `cargando saludo`:** olvidó que importar ejecuta el nivel superior.
3. **Commitear `.venv/`:** marcar siempre.
4. **`venv` vs `uv` como rivales:** `uv` crea un `.venv` estándar por debajo; no se oponen.
5. **`sudo pip install` global:** lo opuesto al aislamiento.

## Rango de soluciones aceptables
- Cualquier librería sirve para la demo (`requests`, `rich`, `httpx`…); no se exige `requests`.
- En Windows la activación es `.venv\Scripts\activate`; aceptar esa variante.
- Para `uv`, tanto `uv init` + `uv add` + `uv run` como crear el `.venv` con `uv venv` + `uv pip
  install` son válidos; lo que importa es que sea reproducible y que entienda el rol del lockfile.
- La explicación de la Parte C puede enfatizar el lockfile o el `site-packages` aislado: ambas vías
  son correctas si nombran el mecanismo (no solo "para no ensuciar").
