# Ejercicio 2.1 — Reconoce el stack: paréntesis balanceados

> **Modalidad: código (Primero-Sin-IA).** Este ejercicio no mide si sabes apilar y desapilar: mide
> si **reconoces** que un problema de anidamiento pide un stack. Esa es la habilidad de trabajo —ver
> la estructura correcta antes de escribir una línea.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.1` DSA a nivel de trabajo
**Ruta:** crítica · **Timebox:** 30–40 min

## 🎯 Objetivo

Implementar `parentesis_balanceados(s)` con un stack (`list` + `append`/`pop`), en O(n), y explicar
por qué `([)]` es inválido aunque tenga el mismo número de cada símbolo.

## 📋 Contexto

El "balanceo de paréntesis" es el problema de stack canónico, y el patrón está en todas partes:
parsers, editores con *undo*, validadores de expresiones, recorridos en profundidad (DFS). Si el
problema tiene **anidamiento** o necesita "recordar dónde estaba para volver", es un stack.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Traza `([)]` en papel antes de codear.
2. Solo entonces, consulta **documentación oficial**.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa `parentesis_balanceados` (no cambies su firma).
2. Pregúntate primero, en papel: ¿por qué `([)]` está mal? Eso te revela que necesitas recordar **el
   orden** en que se abrieron los símbolos — no basta con contar.
3. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. Itera hasta verde. Añade al menos **un caso borde tuyo** en `test_solucion.py`.
5. Escribe una línea en `NOTAS.md`: la complejidad (tiempo y espacio) y **por qué** el stack es la
   estructura correcta.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Pasan todos los casos del enunciado más un caso borde tuyo.
- [ ] Usas una `list` como stack (`append`/`pop`), no cuentas separadas por tipo de símbolo.
- [ ] Manejas un cierre con el stack vacío sin reventar (`IndexError`).
- [ ] Puedes **explicar sin notas** por qué `([)]` exige un stack y contar símbolos no basta.

### Casos que tu solución debe respetar

| `s` | esperado | por qué |
|---|---|---|
| `"()"` | `True` | par simple |
| `"([])"` | `True` | anidamiento correcto |
| `"{[()]}"` | `True` | anidamiento profundo |
| `"([)]"` | `False` | cierre cruzado (mal anidado) |
| `"("` | `False` | apertura sin cerrar |
| `")"` | `False` | cierre sin apertura |
| `""` | `True` | vacío está balanceado |
| `"a(b)c"` | `True` | ignora otros caracteres |

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Recorre `s` carácter a carácter. Si es apertura `([{`, apílalo. Si es cierre `)]}`, mira la **cima**:
si el stack está vacío o la cima no es el par que abre este cierre, devuelve `False`. Un `dict`
`{')': '(', ']': '[', '}': '{'}` te da el par esperado en O(1). Al final, balanceado **solo si el
stack quedó vacío**. `([)]` tiene cuentas correctas pero orden de cierre inválido — solo el stack lo
detecta. Revisa la sección 6.3 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, incluido `NOTAS.md`),
- la **rúbrica**: `.ai/rubricas/fase-2/dsa-stack-parentesis.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/dsa-stack-parentesis.md` — no la mires
antes de intentarlo de verdad.
