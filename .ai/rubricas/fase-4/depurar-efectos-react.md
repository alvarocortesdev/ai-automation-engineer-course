---
ejercicio_id: fase-4/depurar-efectos-react
fase: fase-4
sub_unidad: "4.5"
version: 1
---

# Rúbrica — Depura un panel lleno de useEffect

> Ejercicio **a-mano**: no hay suite de tests. El corrector evalúa el `diagnostico.md` del alumno
> contra `PanelBuggy.tsx` y la solución de referencia. Lo que se mide es **precisión diagnóstica**
> (nombrar el antipatrón exacto, no describirlo vagamente) y la **calidad del arreglo propuesto**,
> no la prosa.

## Objetivos evaluados
- **O1** — Depurar los cuatro antipatrones de `useEffect` y nombrarlos con precisión.
- **O2** — Distinguir el uso **legítimo** de `useEffect` (sincronizar con un sistema externo) del injustificado.
- **O3** — Explicar la consecuencia observable de cada antipatrón y proponer el arreglo mínimo.

> Veredicto esperado (el corrector lo sabe; NO se lo entrega):
> **EFECTO 1** = mal (estado derivado) · **EFECTO 2** = mal (dependencia faltante: `modelo`) ·
> **EFECTO 3** = mal (falta cleanup → race condition) · **EFECTO 4** = **bien** (sync con `document`,
> deps completas, sin cleanup necesario) · **EFECTO 5** = mal (debió ser event handler).

## Criterios y niveles

### C1 — Precisión diagnóstica (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Marca al azar, o "se ve raro" sin nombrar antipatrones; confunde más de dos veredictos. |
| **en-progreso** | Acierta 2–3 veredictos y nombra algún antipatrón, pero falla otros o los describe vagamente. |
| **competente** | Acierta los cinco veredictos y nombra los cuatro antipatrones con el término correcto. |
| **excelente** | Además distingue matices: p. ej. nota que EFECTO 2 *sí* tiene cleanup (su único bug es la dep faltante), y que EFECTO 4 *parece* sospechoso pero es correcto. |

### C2 — Reconocer el efecto correcto · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Marca el EFECTO 4 como roto (cae en el sesgo "todo es bug"). |
| **en-progreso** | Lo marca bien pero no sabe justificar por qué es legítimo. |
| **competente** | Identifica EFECTO 4 como correcto y explica: sincroniza con `document` (sistema externo), todas las deps que lee están presentes, y no necesita cleanup (asignar un string no es una suscripción). |
| **excelente** | Contrasta explícitamente: por qué EFECTO 4 (sync externo legítimo) es correcto y EFECTO 5 (respuesta a interacción) no, aunque ambos "reaccionan a un cambio". |

### C3 — Consecuencia + arreglo mínimo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No explica consecuencias, o propone reescribir todo sin foco. |
| **en-progreso** | Consecuencias a medias o arreglos correctos pero sobredimensionados. |
| **competente** | Cada roto tiene su consecuencia observable y un arreglo mínimo concreto (derivar en render / añadir `modelo` a deps / flag `ignorar` + cleanup / mover a `enviar()`). |
| **excelente** | Las consecuencias son específicas y verificables (p. ej. "EFECTO 3 sin cleanup: al cambiar de modelo rápido, la respuesta del modelo viejo puede llegar después y pisar la del nuevo"). |

## Errores típicos a marcar
- Llamar a EFECTO 1 "bucle infinito": no lo es (`setConteo` solo corre cuando cambia `mensajes`); es un **render de más** y doble fuente de verdad. El bucle infinito real aparece si quitas el array de deps.
- Marcar EFECTO 4 como roto "porque toca `document.title` en un efecto": ese es justo el caso legítimo.
- Confundir EFECTO 2: decir "falta cleanup" cuando **sí** lo tiene (`socket.close`); su bug es la **dependencia faltante** (`modelo`), que deja escuchando el socket del modelo viejo.
- Para EFECTO 3 proponer `async` directo en `useEffect` (no se puede: el setup no debe devolver una promesa); el patrón es función interna + flag `ignorar`.
- Para EFECTO 5 proponer "agregar más deps" en vez de **mover la acción al event handler** `enviar()`.
- (transversal) no mencionar el comportamiento doble de `<StrictMode>` en dev al hablar de cleanup.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diagnóstico perfecto con terminología de blog (cita "stale closure", "tearing") pero no puede explicar con sus palabras qué se vería mal en pantalla.
- Los cinco veredictos correctos pero los arreglos son genéricos ("usa cleanup") sin el código mínimo concreto.
- **Verificación sugerida:** pídele que prediga, para EFECTO 2, qué pasa **exactamente** si el usuario cambia el prop `modelo` de "gpt" a "claude" (debe decir: sigue conectado al socket de "gpt", "claude" nunca se conecta). Si entiende el stale, responde al toque.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el componente arreglado completo.
- **Pista (nivel 1):** "Aplica las cuatro preguntas de la pista del README a cada efecto, en orden. Una de las cinco fichas pasa las cuatro sin problema."
- **Pregunta socrática (nivel 2):** "EFECTO 1 guarda en estado algo que es `mensajes.length`. ¿Podrías escribir ese valor sin `useState`? Si sí, ¿qué gana el componente al quitar el efecto?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa tus deps efecto por efecto: ¿el efecto lee alguna variable que no está en el array? Ese es EFECTO 2. Y busca el efecto que reacciona a un *clic* (vía una bandera de estado) en vez de a un sistema externo: ese debió ir en el handler. No te doy el veredicto de los demás."

## Conexión con el proyecto / capstone
- En el [Capstone F4](/fase-4-frontend/proyecto/), el streaming del LLM es un efecto con cleanup (cancelar el stream al desmontar o al cambiar de conversación) y el "enviar mensaje" es un event handler: este ejercicio entrena justo esa frontera, que es donde se rompen las apps de chat.
