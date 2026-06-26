# Ejercicio 0.6 — Predice las referencias (modelo mental de Git)

> **Modalidad: a mano (sin ejecutar Git, sin IA).** Este ejercicio entrena tu *notional machine* para Git: el modelo mental de qué pasa con los punteros (`HEAD`, ramas) en cada comando. Si puedes dibujar el grafo antes de ejecutar, entendiste el modelo. Si necesitas correr Git para saber dónde quedó cada rama, todavía no.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.6` Git y GitHub a fondo
**Ruta:** crítica · **Timebox:** 30 min

## 🎯 Objetivo

Predecir, sin ejecutar Git, a qué commit apunta cada referencia tras una secuencia que ramifica y diverge; y razonar el resultado de `merge` vs `rebase` sobre ese grafo.

## 📋 La secuencia a trazar

En una carpeta vacía corres, **en este orden exacto**:

```bash
git init
echo "a" > f.txt && git add f.txt && git commit -m "feat: A"   # C1
echo "b" >> f.txt && git commit -am "feat: B"                  # C2
git switch -c feature                                          # crea rama feature
echo "c" >> f.txt && git commit -am "feat: C"                  # C3
git switch main                                                # vuelve a main
echo "d" > g.txt && git add g.txt && git commit -m "feat: D"   # C4
```

## 🛠️ Tu tarea (Primero-Sin-IA, en este orden)

**No ejecutes Git hasta haber terminado los puntos 1–5 a mano.**

1. **Dibuja el grafo de commits** (C1…C4) con flechas de cada commit **hacia su padre**. Pista: un commit nunca tiene más de un padre aquí.
2. **Etiqueta cada referencia**: ¿a qué commit apunta `main`? ¿`feature`? ¿`HEAD`? (Di también a qué apunta `HEAD` de forma simbólica: ¿a una rama o a un commit?)
3. **Merge:** si ahora, parado en `main`, corres `git merge feature`, ¿es un *fast-forward* o un merge de **3 vías** (con commit de fusión)? **Explica por qué** y dibuja el grafo resultante.
4. **Rebase:** como alternativa, si parado en `feature` corres `git rebase main`, dibuja el grafo resultante. ¿Qué le pasa a la **identidad** (el hash) de C3? ¿Por qué?
5. **Criterio propio:** escribe en 2–3 frases una regla para decidir entre merge y rebase, incluyendo la "regla de oro" del rebase.
6. **Solo ahora**, ejecuta la secuencia y verifica con:
   ```bash
   git log --oneline --all --graph
   cat .git/HEAD
   cat .git/refs/heads/main
   cat .git/refs/heads/feature
   ```

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `grafo.md` — el grafo de commits con las referencias etiquetadas (puntos 1–2). Dibújalo en ASCII o con un bloque ` ```mermaid `.
- `respuestas.md` — puntos 3, 4 y 5 (merge vs rebase + tu criterio).
- `verificacion.md` — qué te dijo Git al ejecutar y si coincidió con tu predicción. Si no coincidió, **qué idea tenías equivocada** (no "me equivoqué de commit" — la idea de fondo).

> No ejecutes Git antes de predecir. El valor del ejercicio está en **predecir primero**.

## ✅ Criterios de "hecho"

- [ ] El grafo muestra C1←C2, la bifurcación en C2, y C3/C4 en sus ramas.
- [ ] `main`, `feature` y `HEAD` están etiquetados en el commit correcto.
- [ ] Justificaste *por qué* el merge es de 3 vías (no fast-forward).
- [ ] El grafo del rebase es lineal y explicas el cambio de hash de C3.
- [ ] Tu criterio menciona la regla de oro (no rebasear lo ya compartido).
- [ ] Puedes explicar todo **sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/git-modelo-mental/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisa tu **razonamiento** (el grafo y la justificación), no solo si acertaste el commit final. La **solución de referencia** vive en `.ai/soluciones/fase-0/git-modelo-mental.md` — no la mires antes de intentarlo de verdad.
