---
ejercicio_id: fase-4/filtro-buscable-react
fase: fase-4
sub_unidad: "4.5"
version: 1
---

# Rúbrica — Filtro buscable tipado (sin un solo useEffect)

> Rúbrica analítica atada a los `objetivos` del contrato. Los tests (Vitest + Testing Library)
> verifican el **comportamiento** (input controlado, placeholder, filtrado case-insensitive,
> "Sin resultados"), pero **no** pueden ver si el alumno usó `useEffect` por dentro. El corrector
> abre `FiltroBuscable.tsx` y revisa el **método** (estado derivado, sin efecto, sin estado
> redundante) y si el alumno **entiende** lo que escribió.

## Objetivos evaluados
- **O1** — Componente funcional React 19 + TS con props tipadas, `useState` e input controlado.
- **O2** — Renderizar una lista con `key` estables a partir de un arreglo.
- **O3** — Calcular la lista filtrada como **estado derivado en el render**, sin `useEffect` ni estado redundante.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): un `useState<string>("")` para la
> consulta, una constante `visibles = items.filter(...)` calculada en el render, un `<input>`
> controlado con el `placeholder` de la prop, y un `<ul>` de `<li key={item}>`; sin `useEffect`.

## Criterios y niveles

### C1 — Componente, props tipadas e input controlado (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No compila, o el input no es controlado (sin `value`/`onChange`), o las props no están tipadas. |
| **en-progreso** | Input controlado pero props con `any`/sin `interface`, o el placeholder no se reenvía. |
| **competente** | `interface FiltroBuscableProps` con `items: string[]` y `placeholder?: string`; input controlado (`value` + `onChange`) con el placeholder de la prop; los tests de "estructura básica" e "input controlado" pasan. |
| **excelente** | Tipa además el evento (`React.ChangeEvent<HTMLInputElement>`) y/o explica por qué `value` sin `onChange` deja el input de solo lectura. |

### C2 — Lista con keys estables (corrección) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No renderiza la lista, o no usa `<ul>`/`<li>` (los tests de `listitem` fallan). |
| **en-progreso** | Renderiza la lista pero usa el **índice** del `map` como `key`, o no muestra "Sin resultados". |
| **competente** | `<ul>` de `<li key={item}>` con key estable (el string del item); muestra "Sin resultados" cuando no hay coincidencias; todos los tests verdes. |
| **excelente** | Explica por qué el índice sería mala key si la lista se reordenara/filtrara, y por qué el item string sirve (único y estable). |

### C3 — Estado derivado sin efecto (el corazón del ejercicio) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Usa un segundo `useState` para la lista filtrada **y** un `useEffect` que la "sincroniza". |
| **en-progreso** | Sin efecto, pero guarda la lista filtrada en estado de forma innecesaria, o recalcula de forma confusa. |
| **competente** | La lista filtrada es una constante calculada en el render; **cero `useEffect`**, **cero estado redundante**. |
| **excelente** | Articula por qué no hace falta efecto (el componente se re-ejecuta al cambiar el estado, así que el cálculo siempre está fresco) y por qué el efecto causaría un render de más. |

### C4 — Calidad de ingeniería (testing) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió los tests o los dejó en rojo. |
| **en-progreso** | Tests en verde, pero no agregó el test propio pedido. |
| **competente** | Todos los tests pasan **y** agregó al menos un test propio con un caso borde. |
| **excelente** | El test propio es significativo (acentos, espacios, `items=[]`, duplicados) y revela comprensión del contrato, no relleno. |

## Errores típicos a marcar
- Segundo `useState` para `filtrados` + `useEffect` que lo sincroniza (el antipatrón exacto que la lección combate; los tests pueden pasar y aun así está mal: márcalo en C3).
- Input **no** controlado (`<input />` sin `value`, leyendo del DOM con un ref): rompe O1.
- `key={index}` en el `map`.
- Filtrado sensible a mayúsculas (olvidó `.toLowerCase()` en ambos lados).
- Mutar `items` (p. ej. `items.sort()`) en vez de derivar una copia.
- Usar `class` en vez de `className`.
- (transversal) tests en verde sin entender: persigue "que pase" en vez de razonar el contrato.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución impecable con `useMemo` y tipos sofisticados pero el alumno no sabe explicar por qué NO hay `useEffect` (sofisticación impropia del primer contacto con hooks).
- Comentarios o nombres que no calzan con el código (delatan copiar/pegar).
- **Verificación sugerida:** pídele que, en vivo, **agregue** un `useEffect` que "sincronice" la lista filtrada y prediga qué empeora (debe decir: render de más, doble fuente de verdad, posible desfase). Si entiende, responde al instante; si copió, titubea. O pídele que cambie el filtrado a case-**sensitive** y prediga qué test se rompe.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el componente completo.
- **Pista (nivel 1):** "¿La lista filtrada es un *dato nuevo* o algo que puedes *calcular* a partir de `items` y la consulta? Si lo puedes calcular, ¿necesitas guardarlo en estado?"
- **Pregunta socrática (nivel 2):** "Cuando el usuario teclea, ¿qué hace React con tu función de componente? Si la vuelve a ejecutar entera, ¿qué pasa con una constante `const visibles = items.filter(...)` que está en el cuerpo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Borra el `useState` de la lista filtrada y el `useEffect`. Deja solo el `useState` de la consulta. Calcula `visibles` como una constante en el cuerpo, justo antes del `return`. No te doy el código del filtro."

## Conexión con el proyecto / capstone
- El input controlado y la lista renderizada con keys son **exactamente** el input del chat y la lista de mensajes del [Capstone F4](/fase-4-frontend/proyecto/); el reflejo "estado derivado, no efecto" evita el bug #1 de las apps de chat (renders de más al teclear).
