# leer-stack-traces — Lee el stack trace (a mano)

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.8` Spec-first y lectura de stack traces
**Ruta:** crítica · **Modalidad:** a-mano · **Timebox:** 25–35 min

## 🎯 Objetivo

Leer un stack trace de Python **de abajo hacia arriba** y diagnosticar con método: identificar el
tipo de error, el frame exacto donde reventó, la causa raíz en términos de los **datos**, y un fix
mínimo dirigido a esa causa — **sin ejecutar y sin IA**.

## 📋 Contexto

En el trabajo real (y en un *live coding* con cámara) tu código va a fallar. La diferencia entre un
junior y un semi-senior no es que el semi-senior no tenga bugs: es que **lee el error y razona el
arreglo** en vez de pegar el muro rojo en un chat y rezar. Esta es la mitad "cuando algo revienta"
del método que estrenas en el Capstone F0.

## 📏 Primero-Sin-IA

1. Diagnostica los **tres** casos **a mano**, sin ejecutar y sin IA (timebox arriba). Está bien ir lento.
2. Recién **después** de escribir tu diagnóstico, ejecuta cada programa para confirmar (paso *Investigate*).
3. Solo al final, usa IA para *revisar* tu diagnóstico — nunca para producirlo.
4. Mañana, provoca un error a propósito y léelo de memoria. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

En `casos/` hay tres programas (`caso1.py`, `caso2.py`, `caso3.py`). Abajo está el **stack trace ya
capturado** de cada uno (lo que Python imprime al ejecutarlos). Para **cada caso**, sin ejecutarlo,
escribe en un archivo `diagnostico.md` (lo creas tú) estas cuatro cosas:

1. **Tipo y significado** del error, en tus palabras (no copies el mensaje: explícalo).
2. **Frame culpable**: el archivo y el número de línea donde reventó (el frame de **más abajo**), y por
   qué ese y no el de arriba.
3. **Causa raíz**: por qué pasó, en términos del **dato** concreto que entró.
4. **Fix de una línea**: qué cambiarías (descríbelo; no hace falta reescribir todo el programa).

Recuerda la regla: el traceback se lee **de abajo hacia arriba** (su primera línea dice
`most recent call last`). La **última** línea es el tipo de error + el mensaje; el frame de **más
abajo** es donde explotó; los de arriba son el camino (quién llamó), no la causa.

### Caso 1 — `casos/caso1.py`

```text
Traceback (most recent call last):
  File "caso1.py", line 15, in <module>
    print(precio_total(carro))
          ^^^^^^^^^^^^^^^^^^^
  File "caso1.py", line 7, in precio_total
    total += item["precio"]
             ~~~~^^^^^^^^^^
KeyError: 'precio'
```

### Caso 2 — `casos/caso2.py`

```text
Traceback (most recent call last):
  File "caso2.py", line 12, in <module>
    print(suma_montos(datos))
          ^^^^^^^^^^^^^^^^^^
  File "caso2.py", line 7, in suma_montos
    total += m
TypeError: unsupported operand type(s) for +=: 'int' and 'str'
```

### Caso 3 — `casos/caso3.py`

```text
Traceback (most recent call last):
  File "caso3.py", line 12, in <module>
    reporte([])
  File "caso3.py", line 9, in reporte
    print("Promedio:", promedio(notas))
                       ^^^^^^^^^^^^^^^
  File "caso3.py", line 5, in promedio
    return sum(numeros) / len(numeros)
           ~~~~~~~~~~~~~^~~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

> El caso 3 tiene **tres** frames: el de más abajo (`promedio`, línea 5) es donde reventó; los otros dos
> (`reporte`, `<module>`) son el camino. No confundas el camino con la causa.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Diagnosticaste los **tres** casos **antes** de ejecutar.
- [ ] Para cada uno nombraste el frame de **más abajo** (no el de arriba) como culpable.
- [ ] Tu causa raíz apunta al **dato** concreto que rompió, no a "está mal el código".
- [ ] Tu fix es mínimo y dirigido a la causa, no un parche al azar.
- [ ] Después ejecutaste cada programa y confirmaste tu diagnóstico (o corregiste lo que fallaste).
- [ ] Puedes explicar **sin notas** en qué dirección se lee un traceback y por qué.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Lee siempre de abajo hacia arriba: última línea = tipo + mensaje; frame de abajo = dónde reventó. El
mensaje suele nombrar el culpable literal (`KeyError: 'x'` te da la clave que faltó; `'int' and 'str'`
te dice que mezclaste número y texto). Para la causa raíz, pregúntate qué **dato de entrada** llevó a
ese estado: ¿una clave mal escrita?, ¿un texto donde esperabas un número?, ¿una lista vacía? El fix casi
siempre es validar o convertir ese dato en su origen. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `diagnostico.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-0/leer-stack-traces.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-0/leer-stack-traces.md` — no la mires antes
de intentarlo de verdad.
