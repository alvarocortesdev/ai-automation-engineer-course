---
ejercicio_id: fase-2/dsa-stack-parentesis
fase: fase-2
sub_unidad: "2.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Reconoce el stack: paréntesis balanceados

## Respuesta canónica

```python
def parentesis_balanceados(s: str) -> bool:
    pares = {")": "(", "]": "[", "}": "{"}
    pila: list[str] = []
    for c in s:
        if c in "([{":
            pila.append(c)
        elif c in ")]}":
            if not pila or pila.pop() != pares[c]:
                return False
    return not pila
```

- **Tiempo:** O(n) — un recorrido; `append`/`pop` y el lookup en el `dict` son O(1).
- **Espacio:** O(n) — la pila, en el peor caso (string todo de aperturas), guarda los `n` caracteres.

## Razonamiento paso a paso

1. **El stack guarda las aperturas pendientes.** Cada `(`, `[`, `{` se apila. Es "lo último que abrí es
   lo primero que tengo que cerrar" — LIFO puro.
2. **Cada cierre compara con la cima.** Al llegar `)`, `]` o `}`, la apertura correcta es la que está en
   la cima de la pila. El `dict` `pares` da el par esperado en O(1). Dos formas de fallar al cerrar:
   - la pila está **vacía** (`not pila`) → hay un cierre sin apertura;
   - la cima (`pila.pop()`) **no es** el par esperado → anidamiento cruzado.
3. **El chequeo final.** Tras recorrer todo, el string está balanceado **solo si la pila quedó vacía**
   (`return not pila`): si quedaron aperturas sin cerrar, no está balanceado.
4. **Otros caracteres se ignoran** porque no entran en ninguno de los dos `if`.

Traza de `([)]` (el caso revelador): `(` → pila `['(']`; `[` → pila `['(', '[']`; `)` → cima es `[`,
esperado `(` → **no coinciden** → `False`. Contar símbolos daría `True` (hay un par de cada): solo el
stack ve que el **orden** de cierre es inválido.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Contar en vez de apilar.** Comparar cantidades de `(` y `)` da `([)]→True`. Es el error que separa
   "entendió el patrón" de "encontró un atajo que falla".
2. **`IndexError` con el stack vacío.** Hacer `pila.pop()` sin comprobar `if not pila` primero revienta
   con `"]"`. La guarda `not pila or ...` (cortocircuito) lo evita.
3. **Olvidar `return not pila`.** Si se devuelve `True` al terminar el bucle sin chequear la pila,
   `"(()"` daría `True` incorrectamente.
4. **Stacks separados por tipo.** Mantener un contador o pila por cada tipo de símbolo pierde el orden
   *entre* tipos; `([)]` vuelve a fallar.
5. **Comparar `pila.pop()` con el carácter de cierre en vez del de apertura.** Hay que mapear el cierre a
   su apertura (de ahí el `dict`), no comparar `)` con `(` directamente.

## Rango de soluciones aceptables

- Mapear apertura→cierre en lugar de cierre→apertura es equivalente (apilar el cierre esperado y comparar
  el carácter entrante con la cima). Aceptar si la lógica es correcta.
- Usar `collections.deque` como pila en vez de `list` es válido (también O(1) en ambos extremos), aunque
  para un stack una `list` basta y es lo idiomático.
- Comprobar la pertenencia con `if c in pares.values()` / `if c in pares` en lugar de los literales
  `"([{"` / `")]}"` es aceptable.
- Para `NOTAS.md`, vale cualquier redacción que dé O(n)/O(n) y explique que el stack recuerda **el orden**
  de apertura. El nivel **excelente** conecta con el patrón general (anidamiento / undo / DFS = stack).
- **Variante de control para detectar dependencia-IA:** pedir que trace `([)]` a mano carácter por
  carácter mostrando el estado de la pila. Quien entendió lo hace sin dudar.
