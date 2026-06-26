---
ejercicio_id: fase-2/dsa-analisis-big-o
fase: fase-2
sub_unidad: "2.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Defiende la complejidad: auditoría Big-O

## Respuesta canónica

| Fragmento | Tiempo | Espacio (extra) | Patrón dominante |
|---|---|---|---|
| **A** `f` | O(n) | O(1) | un solo bucle sobre `n`, acumulador |
| **B** `g` | O(n²) | O(n²) | bucle anidado sobre `n`; la salida `pares` puede crecer a n² |
| **C** `h` | O(log n) | O(1) | búsqueda binaria: descarta la mitad cada vuelta |
| **D** `k` | O(n) | O(n) | `set(nums)` recorre y guarda hasta `n` elementos |

**Decisión final (10.000 consultas sobre 1.000.000 de elementos):** usar un `set`.
- `list`: cada `id in lista` es O(n) ≈ 10⁶ operaciones, × 10.000 consultas ≈ **10¹⁰ operaciones**.
- `set`: cada `id in conjunto` es O(1), × 10.000 ≈ **10⁴ operaciones** (más O(n) ≈ 10⁶ una vez para
  construir el `set`).
- El `set` gana por un factor de ~un millón. El costo de construirlo una vez se amortiza de sobra.

## Razonamiento paso a paso

- **A** — Un bucle que toca cada elemento una vez: O(n). Solo usa `total` (una variable): O(1) de espacio
  extra. Patrón: recorrido lineal con acumulador.
- **B** — Dos bucles `range(len(nums))` anidados: la línea del `if` se ejecuta n×n veces → O(n²) tiempo.
  El detalle fino: `pares` puede acumular hasta n² tuplas (si muchísimos pares suman 10), así que el
  **espacio** también es O(n²) en el peor caso. Marcar el espacio O(1) aquí es un error común.
- **C** — `lo` y `hi` se acercan partiendo el rango por la mitad en cada vuelta (`m = (lo+hi)//2`, luego
  `lo = m+1` o `hi = m-1`). Partir `n` por la mitad hasta quedar en 1 son log₂(n) pasos → O(log n).
  Solo variables índice → O(1) espacio. Precondición: `ordenada` ya viene ordenada.
- **D** — Parece O(1) ("una línea"), pero `set(nums)` construye un conjunto recorriendo `nums`: O(n)
  tiempo y O(n) espacio. `len(...)` es O(1). El costo está **escondido en la llamada a `set`**.

## Puntos resbalosos (donde el corrector debe mirar)

1. **B marcado O(n):** no ver el bucle anidado. Es el error central del fragmento más importante.
2. **B con espacio O(1):** ignorar que la lista de salida crece con la entrada (hasta n²).
3. **C marcado O(n):** no reconocer la división por mitades, o no notar la precondición de lista ordenada.
4. **D marcado O(1):** creer que `set(nums)` y `len(...)` son gratis. Construir el `set` es O(n)/O(n).
5. **Decisión sin números:** "el set es más rápido" sin los órdenes de magnitud 10⁴ vs 10¹⁰. El objetivo
   O3 exige cuantificar.

## Rango de soluciones aceptables

- Para el espacio de B, aceptar tanto "O(n²) en el peor caso" como una explicación de que depende de
  cuántos pares cumplan la condición (con el peor caso siendo n²). Penalizar solo "O(1)".
- Para C, aceptar "O(log n)" sin la base del logaritmo (Big-O ignora la base); exigir mencionar la
  precondición de lista ordenada solo en el nivel **competente/excelente**.
- En la decisión final, aceptar cualquier estimación que ponga el contraste de magnitud correcto (lineal
  por consulta vs constante por consulta, ~10⁶× de diferencia). El nivel **excelente** menciona además el
  costo único de construir el `set` (~10⁶) y por qué se amortiza.
- No se exige notación Θ/Ω ni demostraciones formales: es F2, intuición y reconocimiento de patrones. Un
  alumno que la usa pero no puede explicar B en una frase simple es señal de dependencia-IA, no de dominio.
- **Variante de control:** pedir que analice en el momento un quinto fragmento con `x in lista` dentro de
  un bucle. Quien razona ve el O(n²) escondido; quien dependió de la IA no lo deriva solo.
