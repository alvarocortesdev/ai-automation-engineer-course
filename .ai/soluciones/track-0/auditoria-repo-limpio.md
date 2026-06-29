---
ejercicio_id: track-0/auditoria-repo-limpio
fase: track-0
sub_unidad: "T0.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay un núcleo no negociable
> (el secreto → rotar primero; la licencia faltante) y un margen de criterio en el resto.

# Solución de referencia — Audita y limpia un repo de portafolio

## 1. Problemas detectados (referencia)

| # | Gravedad | Problema | Dónde |
|---|---|---|---|
| 1 | 🔴 crítico | `OPENAI_API_KEY` filtrada: `.env` commiteado **y** key hardcodeada en `main.py` **y** un commit "add openai key so it works" que la deja en el historial. | `.env`, `main.py`, log |
| 2 | 🔴 crítico | Password de la DB expuesto en `DATABASE_URL` (`admin:admin123`) dentro del `.env` commiteado. | `.env` |
| 3 | 🟡 importante | Sin `.gitignore` → causa raíz: `.env`, `__pycache__`, checkpoints del notebook se cuelan al repo. | árbol |
| 4 | 🟡 importante | Sin `LICENSE` → el repo es legalmente "all rights reserved" por defecto; nadie puede usar/copiar tu código. Contradice un portafolio OSS. | árbol |
| 5 | 🟡 importante | `README.md` vacío (solo `# mi-rag-app`) → no comunica qué hace, cómo correrlo, ni demo. Cero señal. | README |
| 6 | 🟡 importante | Historial ilegible: commits "update", "asdf", "wip", "fix bug" → ninguna Conventional Commit; no cuentan una historia. | log |
| 7 | ⚪ menor | `notebook_pruebas.ipynb` → basura de exploración en un repo de portafolio. | árbol |

> ≥5 bien clasificados es competente. El secreto (1) y el password (2) **deben** ser 🔴.

## 2. Fix concreto por problema (referencia)

- **Secreto filtrado (1 y 2) — ORDEN CORRECTO:**
  1. **Rotar/revocar la `OPENAI_API_KEY` YA** en el dashboard del proveedor (asumir que ya la copiaron;
     una key commiteada es una key comprometida). Cambiar también el password de la DB.
  2. Añadir `.env` al `.gitignore`; crear `.env.example` con claves sin valores.
  3. Quitar la key hardcodeada de `main.py`; leerla con `os.environ` / variable de entorno.
  4. **Limpiar el historial:** `git filter-repo` (o BFG) para purgar el secreto de commits viejos —o,
     más simple para un repo pequeño, **arrancar un repo nuevo limpio** y archivar el viejo.
  - *Por qué en ese orden:* Git guarda todo el historial; borrar el archivo hoy no quita el secreto de
    los commits anteriores, y hacer el repo privado no garantiza que nadie ya lo clonó. Lo único que
    reduce el daño de inmediato es **rotar**.
- **Sin `.gitignore` (3):** añadir uno (plantilla Python: `.env`, `__pycache__/`, `*.ipynb_checkpoints`).
- **Sin `LICENSE` (4):** añadir un `LICENSE` (MIT para portafolio permisivo; usar choosealicense.com).
- **README vacío (5):** escribir un README real: qué hace, demo, cómo correrlo, stack, decisiones/trade-offs.
- **Historial ruido (6):** adoptar Conventional Commits de aquí en adelante; si el repo aún no es
  público/compartido, reescribir mensajes con un rebase.
- **Notebook basura (7):** eliminarlo del repo o moverlo a una carpeta `scratch/` ignorada.

## 3. Tres commits reescritos a Conventional Commits (referencia)

| Original | Reescrito | Por qué ese tipo |
|---|---|---|
| `fix bug` | `fix(ingest): evita índice fuera de rango al chunkear documentos vacíos` | `fix`: corrige un comportamiento incorrecto; el scope ubica el módulo. |
| `Update README (again)` | `docs: documenta cómo correr la app y agrega la sección de demo` | `docs`: solo cambia documentación, no código. |
| `wip` | `feat(rag): agrega reranking sobre los resultados del retriever` | `feat`: introduce una capacidad nueva (asumiendo que eso hacía el WIP). |

> Nota clave: el commit `add openai key so it works` **no se reescribe** —no debió existir. El fix no es
> renombrarlo; es que el secreto nunca se commitea (ver problema 1).

## 4. Veredicto (referencia)

> **No está listo para pinear.** Como mínimo, antes de mostrarlo: rotar las credenciales y purgar el
> secreto del historial (bloqueante), escribir un README real y añadir `LICENSE` y `.gitignore`. Con el
> historial ruido limpiado, recién entonces es vitrina.

## Puntos resbalosos (donde el corrector debe mirar)
- **Fix del secreto que empieza por "borrar el `.env`"** o "hacer el repo privado" → no rota la key, no
  aborda el historial. Es el error #1 del ejercicio.
- **Olvidar la key hardcodeada en `main.py`** (creer que solo está en `.env`).
- **No detectar la falta de `LICENSE`** o no saber su consecuencia legal.
- **Conventional Commits con tipo equivocado** (todo `feat:`) o sin justificar.
- **Mezclar gravedades:** poner el README vacío al mismo nivel 🔴 que la key filtrada.

## Rango de soluciones aceptables
- El conjunto exacto de problemas puede variar (≥5), pero el secreto y el password **deben** ser 🔴 y
  el fix del secreto **debe** empezar por rotar.
- Las reescrituras de commit pueden usar otros scopes/descripciones; lo que importa es formato válido
  `tipo(scope): descripción` + tipo apropiado + justificación.
- La limpieza del historial puede ser filter-repo, BFG o repo nuevo: cualquiera es válida si reconoce
  que borrar el archivo no basta.
