---
ejercicio_id: fase-4/route-handler-modelos
fase: fase-4
sub_unidad: "4.6"
version: 1
---

# Rúbrica — Route Handler con validación de entrada

> Rúbrica analítica atada a los `objetivos` del contrato. Los tests (Vitest, entorno node)
> verifican el **contrato del endpoint** (filtrado, validación, status codes, forma de la
> respuesta). El corrector abre `route.ts` y revisa el **método** (validar ANTES de procesar,
> usar status codes correctos) y si el alumno **entiende** por qué la validación va en el servidor.

## Objetivos evaluados
- **O1** — Route Handler `GET` con `Request`/`Response` web estándar que filtra un catálogo por query params.
- **O2** — Validación de entrada en el servidor (acotar `q`, validar `limit`) con status codes correctos (200/400).
- **O3** — Respuesta JSON con forma estable `{ query, count, items }`.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): leer params de `new URL(request.url).searchParams`,
> validar `q` (largo) y `limit` (entero ≥ 1) devolviendo `400` ante basura, filtrar case-insensitive contra
> `nombre` y `proveedor`, acotar con `slice(0, Math.min(limit, 50))` y responder `{ query, count, items }`.

## Criterios y niveles

### C1 — Mecánica del handler (corrección) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No compila, o no lee los query params, o no filtra (los tests de "filtrado" fallan). |
| **en-progreso** | Lee `q` y filtra, pero solo contra `nombre` (olvida `proveedor`), o el filtrado es case-sensitive, o la forma de la respuesta no es `{ query, count, items }`. |
| **competente** | Lee `q` y `limit` desde la URL; filtra case-insensitive contra `nombre` **y** `proveedor`; responde la forma exacta; pasan los tests de "respuesta base" y "filtrado". |
| **excelente** | Calcula `q.toLowerCase()` una sola vez; nombres claros; el código se lee como el flujo firma→leer→validar→procesar→responder. |

### C2 — Validación de entrada y status codes (seguridad) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida nada: `limit=abc` rompe o devuelve 200; `q` enorme se procesa. Los tests de "limit" y "seguridad" fallan. |
| **en-progreso** | Valida una de las dos (p. ej. `limit` pero no acota `q`), o devuelve el status equivocado (500 en vez de 400, o 400 cuando debía acotar `limit` a 50). |
| **competente** | `q` largo → 400; `limit` no entero / `< 1` → 400; `limit > 50` se **acota** (no error); todos los tests verdes; los 400 traen `{ error }`. |
| **excelente** | Articula el principio: el cliente puede mentir, así que la validación del servidor es la frontera de confianza real; menciona el riesgo de entrada no acotada (ReDoS / consumo) y por qué `400` (no `500`) es el código correcto. |

### C3 — Calidad de ingeniería (testing) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió los tests o los dejó en rojo. |
| **en-progreso** | Tests en verde, pero no agregó el test propio pedido. |
| **competente** | Todos los tests pasan **y** agregó al menos un test propio con un caso borde. |
| **excelente** | El test propio es significativo (`limit=50` exacto, `q` con espacios/acentos, mayúsculas contra proveedor) y revela comprensión del contrato, no relleno. |

### C4 — Comprensión demostrada · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué valida en el servidor ("porque sí"). |
| **en-progreso** | Dice "para evitar errores" pero no distingue validación de cliente vs. servidor. |
| **competente** | Explica que el cliente es no confiable y que cualquiera puede llamar al endpoint directo (curl), saltándose la validación del navegador. |
| **excelente** | Conecta con el capstone: el mismo endpoint sirve la UI de chat con la clave de API en el servidor; valida y autoriza ahí. |

## Errores típicos a marcar
- No valida `limit`: `Number("abc")` da `NaN` y se cuela como si fuera válido (debe ser 400).
- Filtra solo por `nombre` y olvida `proveedor` (rompe el test `q=openai`).
- Filtrado case-sensitive (olvidó `.toLowerCase()` en un lado).
- Devuelve `500` (excepción no controlada) en vez de `400` ante entrada inválida.
- Trata `limit > 50` como error 400 en vez de **acotar** a 50.
- `count` mal calculado: usa el total de coincidencias en vez de los items realmente devueltos tras el `slice`.
- Confía en que "el frontend ya valida" y deja el handler sin validar (el antipatrón de seguridad central del ejercicio).
- (transversal) tests en verde sin entender: persigue "que pase" en vez de razonar el contrato.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Usa `NextRequest`/`NextResponse` y middlewares sofisticados que el ejercicio no pide ni necesita (sofisticación impropia del primer contacto con Route Handlers), sin poder explicar por qué `Request`/`Response` bastan.
- Validación con una librería de esquemas (zod) impecable pero no sabe explicar qué status code corresponde ni por qué.
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué responde el endpoint ante `?limit=51` (debe decir: 200, acotado a 50) y ante `?limit=0` (400). Si entiende, responde al instante; si copió, titubea. O pídele que cambie el filtro a case-sensitive y prediga qué test se rompe.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el handler completo.
- **Pista (nivel 1):** "¿Qué pasa con `Number('abc')`? ¿Tu código distingue un `limit` válido de uno basura antes de usarlo?"
- **Pregunta socrática (nivel 2):** "Si yo llamo a tu endpoint con `curl` (sin pasar por tu frontend), ¿qué me protege de mandar un `q` de 10.000 caracteres? ¿Dónde tiene que vivir esa protección?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Antes de filtrar, agrega dos guardias que devuelvan `Response.json({ error }, { status: 400 })`: una para el largo de `q`, otra para `limit` no entero o `< 1`. No te doy el código del filtro."

## Conexión con el proyecto / capstone
- Este endpoint es el molde del Route Handler que sirve la UI de chat del [Capstone F4](/fase-4-frontend/proyecto/): el cliente pide datos, el servidor valida la entrada y responde JSON con la clave de API a salvo. El hábito de validar en el servidor es el que el Definition of Done exige en todo capstone con endpoint.
