# Ejercicio 2.1 — Defiende la complejidad: auditoría Big-O

> **Modalidad: a mano (sin ejecutar, sin IA).** Este ejercicio entrena lo que de verdad mide un live
> coding: mirar código ajeno y **medirlo** en voz alta. No hay tests automáticos — la "verificación"
> es que puedas defender cada respuesta como si te preguntaran "¿por qué?".

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.1` DSA a nivel de trabajo
**Ruta:** crítica · **Timebox:** 25–35 min

## 🎯 Objetivo

Estimar por intuición la complejidad de tiempo y espacio de cuatro fragmentos, nombrar el patrón
dominante de cada uno, y justificar una elección de estructura (`list` vs `set`) con Big-O y órdenes
de magnitud.

## 📋 Contexto

La habilidad de trabajo no es recitar la tabla de complejidades: es la inversa — mirar un fragmento y
decir su Big-O y cómo mejorarlo. Este ejercicio te pone justo en esa silla.

## 📏 Primero-Sin-IA

1. Analiza **solo**, a mano (timebox arriba). Cuenta bucles, mira de qué dependen.
2. Solo entonces, consulta **documentación oficial** (la tabla de complejidades de Python).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Tu tarea

En un archivo `analisis.md`, para **cada uno** de los cuatro fragmentos escribe:
(a) complejidad de **tiempo** en Big-O, (b) complejidad de **espacio**, y (c) una frase que nombre el
**patrón dominante** que te llevó a esa respuesta.

```python
# A
def f(nums):
    total = 0
    for x in nums:
        total += x
    return total

# B
def g(nums):
    pares = []
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == 10:
                pares.append((i, j))
    return pares

# C
def h(ordenada, objetivo):     # `ordenada` ya viene ordenada
    lo, hi = 0, len(ordenada) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if ordenada[m] == objetivo: return m
        if ordenada[m] < objetivo: lo = m + 1
        else: hi = m - 1
    return -1

# D
def k(nums):
    return len(set(nums)) != len(nums)
```

Y al final, **decide y justifica con Big-O**: tienes que comprobar 10.000 veces si un `id` está dentro
de una colección de 1.000.000 de elementos. ¿La guardas en una `list` o en un `set`? Da el número
aproximado de operaciones de cada opción (orden de magnitud).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Diste tiempo **y** espacio para los cuatro fragmentos.
- [ ] Nombraste el patrón dominante de cada uno (no solo la letra O).
- [ ] En la decisión final, justificaste con Big-O y un orden de magnitud, no con "el set es más rápido".
- [ ] Puedes **defender cada respuesta en voz alta**, como en una entrevista.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para cada fragmento, cuenta los bucles y mira de qué dependen: ¿uno solo sobre `n`? ¿dos anidados?
¿se parte algo a la mitad? Para el espacio, pregúntate cuánta memoria *extra* crece con `n` (¿una
lista que puede tener `n` o `n²` elementos? ¿un par de variables?). El fragmento D esconde su costo
dentro de `set(...)`: ¿cuánto cuesta construir un `set` de `n` elementos, en tiempo y espacio? Para la
decisión final, `list` = O(n) por consulta × 10.000; `set` = O(1) por consulta × 10.000. Pon los
números. Revisa la sección 4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `analisis.md`,
- la **rúbrica**: `.ai/rubricas/fase-2/dsa-analisis-big-o.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/dsa-analisis-big-o.md` — no la mires antes
de intentarlo de verdad. El corrector revisará tu **razonamiento**, no solo si las letras O coinciden.
