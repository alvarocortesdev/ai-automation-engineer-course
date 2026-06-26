# 2.3 — Caracteriza y refactoriza código legado (sin red)

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.3` Code smells y refactoring
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Refactorizar código legado **sin tests** de la única forma segura: construyendo
**primero** una red de *characterization tests* que pinte el comportamiento actual,
y solo entonces moviendo el código. Vas a sentir, en carne propia, por qué la red
es el prerrequisito y no un trámite — y practicar la disciplina de los **dos
sombreros**: preservar el comportamiento exacto, rarezas incluidas.

## 📋 Contexto

`etiqueta_envio(peso_gramos, zona)` clasifica un envío. Está enredada, duplica
lógica entre zonas y **no tiene ni un test**. Es el caso realista: en un trabajo,
casi todo el código que tocas está así. Quien sabe entrar, asegurarlo con tests y
dejarlo mejor **sin romper producción** es quien vale la banda semi-senior. Esto
conecta directo con [`2.12` Debugging y código legado](/fase-2-ingenieria/2-12-debugging-codigo-legado/).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Red primero, refactor después.
2. Solo entonces, consulta el [catálogo oficial de Fowler](https://refactoring.com/catalog/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones (orden ESTRICTO)

1. **Caracteriza primero.** En `test_solucion.py` (trae un esqueleto con TODOs),
   escribe characterization tests que pinten lo que la función hace **hoy**:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

   Cubre cada rama y cada **borde**: 499/500 g y 1999/2000 g (zonas 1 y 2),
   999/1000 g (zona 3), y el **caso raro**: una `zona` desconocida (p. ej. `5`).
   El `esperado` lo obtienes leyendo el código o ejecutándolo y copiando el
   resultado real. No corras a "arreglar" nada: solo **congela** lo que hay.
2. **Solo cuando esa suite esté toda en VERDE**, refactoriza `solucion.py`:
   elimina la duplicación entre zonas (extrae el "tamaño según peso" y compón con
   el prefijo), aplana los condicionales anidados. Corre `pytest` después de cada
   paso: debe seguir verde sin que cambies un solo `esperado`.
3. Documenta en `notas.md`.

> ⚠️ **Preserva el comportamiento, rarezas incluidas.** La `zona` desconocida hoy
> cae en la rama internacional. Eso quizá sea un bug — pero **refactorizar no es
> arreglar bugs**. Lo preservas y lo anotas como deuda separada (un `fix:` futuro
> con su propio test). Dos sombreros: uno a la vez.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Escribiste los characterization tests **antes** de refactorizar (red verde primero).
- [ ] Tus tests cubren los **bordes** de peso y el caso de `zona` desconocida.
- [ ] Refactorizaste eliminando la **duplicación** entre zonas, con todo aún en verde.
- [ ] **No cambiaste el comportamiento** — ni el de la `zona` desconocida.
- [ ] `notas.md` registra el comportamiento raro preservado **a propósito** y por qué.
- [ ] Puedes explicar **sin notas** por qué el characterization test es el prerrequisito.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `test_solucion.py` — la red de characterization tests que construiste.
- `solucion.py` — la versión refactorizada (misma conducta, estructura limpia).
- `notas.md` — smells encontrados, refactorings aplicados, y el comportamiento raro
  que preservaste a propósito (con la razón).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para la red: un `@pytest.mark.parametrize` con `(peso, zona, esperado)` donde el
`esperado` lo sacas del código actual (el "golden master"). Cubre cada frontera:
499→ligero, 500→medio, 1999→medio, 2000→pesado (zonas 1 y 2), y zona 3 con
999→estándar, 1000→especial. Para `zona` 5, observa que cae en el `else` final y se
comporta como internacional: **pinta ese** comportamiento. Para refactorizar, nota
que zona 1 y 2 comparten los umbrales 500/2000: extrae `tamano_por_peso(peso)` que
devuelva `"ligero"/"medio"/"pesado"` y compón `f"{prefijo}-{tamano}"`. La rama
internacional (zona 3 y cualquier otra) usa su propio umbral 1000. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `test_solucion.py` y `notas.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/caracterizar-y-refactorizar-legado.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en
`.ai/soluciones/fase-2/caracterizar-y-refactorizar-legado.md` — no la mires antes
de intentarlo de verdad.
