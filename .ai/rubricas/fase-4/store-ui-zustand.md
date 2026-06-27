---
ejercicio_id: fase-4/store-ui-zustand
fase: fase-4
sub_unidad: "4.8"
version: 1
---

# Rúbrica — Store de UI con Zustand (persist + selectores atómicos)

> Rúbrica analítica atada a los `objetivos` del contrato. Los tests (Vitest + Testing Library)
> verifican el **comportamiento** (actions, inmutabilidad, lectura por selector, `partialize`),
> pero **no** pueden ver si el alumno destructura el store entero o si un selector devuelve un
> objeto nuevo. El corrector abre `useUiStore.ts` y el test, revisa el **método** (selectores
> atómicos, persistir solo lo duradero) y si el alumno **entiende** lo que escribió.

## Objetivos evaluados
- **O1** — Store de Zustand v5 en TS con la forma currificada `create<UiState>()(...)` y actions inmutables.
- **O2** — `persist` con `createJSONStorage` y `partialize` que guarda solo el estado que debe durar.
- **O3** — Lectura con selectores atómicos desde un componente, evitando re-renders innecesarios.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): `create<UiState>()(persist((set) => ({...}), { name: "ui-chat-storage", storage: createJSONStorage(() => localStorage), partialize: (s) => ({ tema: s.tema, modelosFavoritos: s.modelosFavoritos }) }))`, con toggle inmutable (`filter`/spread) y el componente leyendo con `useUiStore(s => s.modeloActivo)`.

## Criterios y niveles

### C1 — Store, tipos y actions inmutables (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No compila, o las actions no cambian el estado, o muta con `push` (los tests de inmutabilidad/toggle fallan). |
| **en-progreso** | Las actions funcionan pero alguna muta el estado (el test "NO muta: crea un arreglo nuevo" falla), o no usa la forma currificada. |
| **competente** | `create<UiState>()(...)`; `setModelo`/`alternarTema`/`alternarFavorito` correctas e **inmutables** (arreglos nuevos); todos los tests de actions pasan. |
| **excelente** | Distingue cuándo `set` con objeto (merge superficial) vs `set` con función (depende del estado previo) y lo explica; tipa limpio sin `any`. |

### C2 — persist + partialize (corrección) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `persist`, o nada se escribe en `localStorage` (el test de persist falla con `crudo === null`). |
| **en-progreso** | Persiste, pero guarda el estado **entero** (incluye `modeloActivo`): el test "no persiste el modelo de sesión" falla. |
| **competente** | `persist` con `name` y `createJSONStorage(() => localStorage)`; `partialize` persiste **solo** `tema` y `modelosFavoritos`; el test de persist pasa. |
| **excelente** | Articula por qué `modeloActivo` es de sesión (no debe "recordarse") y por qué un token/PII jamás iría en `persist` a `localStorage` (XSS) — hilo de seguridad por iniciativa. |

### C3 — Selectores atómicos (rendimiento) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Destructura el store entero (`const { modeloActivo } = useUiStore()`) o no lee con el hook. |
| **en-progreso** | Usa selector, pero devuelve un **objeto nuevo** sin `useShallow` (riesgo de re-render en bucle), o suscribe a más de lo necesario. |
| **competente** | Lee con selector atómico `useUiStore(s => s.modeloActivo)`; el componente refleja el cambio (test verde). |
| **excelente** | Si necesita varios campos, usa dos selectores o `useShallow`; explica por qué el objeto-literal en el selector re-renderiza siempre en v5. |

### C4 — Calidad de ingeniería (testing) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió los tests o los dejó en rojo. |
| **en-progreso** | Tests en verde, pero no agregó el test propio pedido. |
| **competente** | Todos los tests pasan **y** agregó al menos un test propio con un caso borde. |
| **excelente** | El test propio es significativo (dos favoritos distintos, persistir tras varias acciones, quitar un favorito inexistente) y revela comprensión, no relleno. |

## Errores típicos a marcar
- Mutar `modelosFavoritos` con `push`/`splice` en vez de crear un arreglo nuevo (rompe la detección de cambios; el test de inmutabilidad lo atrapa).
- Persistir el estado entero (olvidar `partialize` o incluir `modeloActivo`): el test lo detecta.
- Destructurar el store entero (`const { x } = useUiStore()`): los tests no lo ven, pero es C3-incompleto; márcalo.
- Selector que devuelve `{ a, b }` sin `useShallow`: re-render en bucle en v5 (márcalo aunque los tests pasen).
- Usar `useStore(selector, shallow)` al estilo v4 (no compila en v5) o importar `shallow` en vez de `useShallow`.
- Olvidar la forma currificada `create<T>()(...)` (el segundo par de paréntesis) y pelear con los tipos.
- (transversal) tests en verde sin entender: persigue "que pase" en vez de razonar qué persistir y por qué.
- (transversal seguridad) sugerir guardar el token en el store "porque también es global".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Store impecable con `devtools`, `immer` y tipos sofisticados, pero el alumno no sabe explicar por qué `modeloActivo` no se persiste (sofisticación impropia del primer contacto con Zustand).
- Comentarios/nombres que no calzan con el código, o un `partialize` "mágico" que no sabe defender.
- **Verificación sugerida:** pídele que, en vivo, cambie `partialize` para que también persista `modeloActivo` y **prediga** qué test se rompe y por qué (debe decir: el test que afirma `modeloActivo` undefined en el blob). O pídele que explique qué pasaría si destructurara el store entero en un componente con un store de 15 campos.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el store completo.
- **Pista (nivel 1):** "¿Todo lo que hay en el estado merece sobrevivir a una recarga? ¿`modeloActivo` debería 'recordarse' mañana, o es de esta sesión?"
- **Pregunta socrática (nivel 2):** "Cuando llamas `set((state) => ({ modelosFavoritos: ... }))`, ¿estás creando un arreglo nuevo o tocando el que ya estaba? ¿Cómo decide Zustand si re-renderizar?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Agrega la opción `partialize` a `persist`: es una función que recibe el estado y devuelve un objeto solo con `tema` y `modelosFavoritos`. No te doy el resto del store."

## Conexión con el proyecto / capstone
- Este store **es** el estado global de cliente del [Capstone F4](/fase-4-frontend/proyecto/): tema, modelo y preferencias con `persist`. Persistir solo lo duradero y leer con selectores atómicos evita el bug de UI que se repinta entera y el de "recordar" estado que no debía durar.
