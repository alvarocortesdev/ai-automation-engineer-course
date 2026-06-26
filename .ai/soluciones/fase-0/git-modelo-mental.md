---
ejercicio_id: fase-0/git-modelo-mental
fase: fase-0
sub_unidad: "0.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Predice las referencias (modelo mental de Git)

## Respuesta canónica

Tras la secuencia completa:

- `main` → **C4**
- `feature` → **C3**
- `HEAD` → **`main`** (porque el último comando fue `git switch main`), que apunta a C4. De forma simbólica: `.git/HEAD` contiene `ref: refs/heads/main`.

Estado del grafo (flechas = commit → su padre):

```text
C1 ← C2 ← C3        (feature → C3)
       ↖ C4         (main → C4, HEAD → main)
```

Es decir, C2 tiene **dos hijos**: C3 (en `feature`) y C4 (en `main`). El ancestro común de ambas ramas es C2.

## Razonamiento paso a paso

| Comando | Qué se mueve | Estado de referencias |
|---|---|---|
| `commit "feat: A"` (C1) | crea C1; `main`→C1 | main→C1, HEAD→main |
| `commit "feat: B"` (C2) | crea C2 (padre C1); `main`→C2 | main→C2, HEAD→main |
| `git switch -c feature` | crea post-it `feature` en C2; mueve `HEAD`→`feature` | main→C2, feature→C2, HEAD→feature |
| `commit "feat: C"` (C3) | crea C3 (padre C2); **solo** `feature`→C3 | main→C2, feature→C3, HEAD→feature |
| `git switch main` | mueve `HEAD`→`main` (no crea commits) | main→C2, feature→C3, HEAD→main |
| `commit "feat: D"` (C4) | crea C4 (padre C2); **solo** `main`→C4 | main→C4, feature→C3, HEAD→main |

Clave: en C3 solo avanzó `feature` y en C4 solo avanzó `main`, porque cada commit mueve **únicamente la rama a la que apunta `HEAD`**.

## Punto 3 — merge (3 vías)

`git merge feature` desde `main` es un **merge de 3 vías**, NO fast-forward. Razón: un fast-forward solo es posible cuando la rama destino (`main`) **no avanzó** desde que la otra divergió, de modo que Git solo "adelanta el puntero". Aquí **ambas** ramas avanzaron desde el ancestro común C2 (main→C4, feature→C3), así que las historias **divergieron** y Git debe crear un **commit de fusión** `M` con dos padres (C4 y C3):

```text
C1 ← C2 ← C3 ←──┐
       ↖ C4 ←── M   (main → M; M tiene padres C4 y C3)
```

## Punto 4 — rebase (reescritura)

`git rebase main` desde `feature` toma los commits exclusivos de `feature` (C3) y los **reaplica uno por uno sobre C4**. Resultado lineal:

```text
C1 ← C2 ← C4 ← C3'   (feature → C3', main → C4)
```

C3' tiene **el mismo cambio (diff) que C3, pero distinto padre (C4 en vez de C2) y por tanto distinto hash**. El C3 original queda huérfano (sin rama que lo apunte) hasta que el garbage collector lo recoge; no se "pierde" trabajo, se reescribe la identidad. Es consecuencia de que Git es *content-addressed*: el hash deriva del contenido + el padre + la metadata, así que cambiar el padre cambia el hash.

## Punto 5 — criterio (incluida la regla de oro)

- **rebase** para ordenar tu rama **local/privada** antes de compartirla (historial lineal, fácil de leer).
- **merge** para integrar ramas **ya compartidas/públicas** (preserva la verdad, no reescribe hashes ajenos).
- **Regla de oro:** *nunca hagas rebase de commits que ya existen fuera de tu repo local* (que empujaste y otros pudieron usar), porque reescribir esos hashes obliga al resto a `push --force` y rompe su historial.

## Rango de soluciones aceptables

- El grafo puede dibujarse en ASCII, Mermaid o a mano fotografiado: cuenta cualquier representación donde se vea la **bifurcación en C2** y las referencias bien ubicadas.
- Es válido (y `excelente`) describir el estado **intermedio** justo antes del último `git switch main` (HEAD→feature) además del final.
- Para el merge, aceptar tanto "3 vías" como "true merge / merge commit" si la justificación menciona la divergencia.
- Para el criterio, cualquier formulación correcta de la regla de oro vale; no se exige una redacción concreta. Mencionar "historial lineal vs preservar la verdad" es señal de comprensión profunda.
