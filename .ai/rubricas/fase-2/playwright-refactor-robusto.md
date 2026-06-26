---
ejercicio_id: fase-2/playwright-refactor-robusto
fase: fase-2
sub_unidad: "2.10"
version: 1
---

# Rúbrica — Estabiliza un e2e flaky (refactor robusto + Page Object)

> Rúbrica **analítica** atada a los `objetivos`. El producto no es "el test pasa": un
> `waitForTimeout(5000)` también hace pasar el test. El producto es un e2e **robusto y
> determinista** (selectores por rol, web-first assertions, cero sleeps) con un **Page
> Object** que separa el qué del cómo. Evalúa el `diagnostico.md` tanto como el código:
> un alumno puede copiar la pista y dejar el test verde sin entender por qué `toBeVisible()`
> reemplaza al sleep. La rúbrica distingue ambos.

## Objetivos evaluados
- **O1** — Diagnosticar los antipatrones (selectores CSS, `waitForTimeout`, `textContent` + expect manual).
- **O2** — Reescribir con selectores por rol/label y web-first assertions con auto-waiting, sin sleeps.
- **O3** — Extraer un Page Object con las aserciones en el test y las interacciones en la clase.

## Criterios y niveles

### C1 — Diagnóstico razonado (Primero-Sin-IA) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `diagnostico.md`, o solo dice "lo refactoricé" sin nombrar antipatrones. |
| **en-progreso** | Nombra alguno (p. ej. "uso sleep") pero no explica *por qué* es malo, o se le escapa el de los selectores o el de `textContent`. |
| **competente** | Nombra los tres antipatrones y explica el daño de cada uno: selectores acoplados a la implementación, `waitForTimeout` (frágil si corto / lento si largo), foto inmediata con `textContent`. |
| **excelente** | Además articula la causa raíz común —"afirmar antes de que el estado esté listo"— y por qué la latencia variable de la app es justo lo que un sleep no maneja bien. |

### C2 — Selectores robustos y web-first assertions (corrección) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sigue habiendo selectores CSS/`#id` o algún `waitForTimeout`; o el test quedó flaky/rojo. |
| **en-progreso** | Migró parte a `getByRole`/`getByLabel` pero deja algún `locator('.x')`, o usa `textContent()` + expect en vez de `expect(locator)`, o solo cubre el camino feliz. |
| **competente** | Todos los selectores son user-facing; toda verificación es web-first assertion; **sin** `waitForTimeout`; cubre camino feliz **y** validación; `pnpm test` determinista (3/3). |
| **excelente** | Usa la assertion más expresiva por caso (`toHaveText`, `toHaveCount` para la lista), justifica cualquier `getByTestId` como último recurso, y deja el test legible como una historia. |

### C3 — Page Object (diseño) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `GastosPage`, o el `.spec.ts` sigue lleno de selectores crudos. |
| **en-progreso** | Hay una clase, pero mete **aserciones** dentro del Page Object, o deja selectores en el test, o el método `agregar` no encapsula bien. |
| **competente** | `GastosPage` con `readonly` locators en el constructor y método(s) de interacción; el `.spec.ts` no tiene selectores crudos; las aserciones se quedan en el test. |
| **excelente** | Locators bien nombrados, un método `agregar(desc, monto)` reutilizado por ambos caminos, y una separación qué/cómo que se explica sola. |

## Errores típicos a marcar
- **Cambiar un sleep por otro sleep más largo** "para que no flakee": esconde la causa y vuelve lento el test. La cura es `expect(locator).toBeVisible()`.
- **Dejar selectores `#id`/`.clase`** creyendo que "igual funcionan": son detalle de implementación; se rompen con un rediseño.
- **`textContent()` + `expect` manual**: toma una foto inmediata; con la latencia de la app, falla o flakea. Usa la web-first assertion.
- **Meter aserciones en el Page Object**: la aserción es el corazón del test y se queda en el `.spec.ts`.
- **Modificar `app.html`** para "facilitar" el test: el SUT está correcto; el problema está en el test.
- **Solo el camino feliz**: el enunciado pide también el de validación (`role="alert"`).
- (transversal costo/latencia) no notar que el sleep de 1 s se paga en cada corrida.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `diagnostico.md` impecable pero el código sigue con un `waitForTimeout` (la explicación no calza con la entrega), o al revés: código perfecto y diagnóstico vacío.
- Page Object con abstracciones impropias del nivel (fixtures custom, herencia de un BasePage genérico) que el ejercicio no pide y que el alumno no puede justificar.
- Uso de `page.waitForSelector`/`waitForLoadState` rebuscado en vez de la web-first assertion simple: sofisticación que sugiere copy-paste sin entender el auto-waiting.
- **Verificación sugerida:** pídele que explique, sin notas, qué pasa si la latencia de la app sube a 800 ms: ¿su test sigue verde? ¿por qué? Si entendió `toBeVisible()`, responde al instante que sí (auto-waiting), y que el viejo `waitForTimeout(1000)` habría quedado al filo.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu test espera con `waitForTimeout`. ¿Qué pasa si la app un día tarda más que ese número? ¿Y si tarda menos, cuánto tiempo estás regalando en cada corrida?"
- **Pregunta socrática (nivel 2):** "¿Qué línea sabe, sola, esperar hasta que el mensaje aparezca y seguir apenas aparece, sin que tú adivines los milisegundos? ¿Dónde la pondrías?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Borra el `waitForTimeout` y el `textContent`. Reemplázalos por `await expect(page.getByText('Gasto agregado')).toBeVisible()`. Cambia `#desc`/`#monto`/`.btn-add` por `getByLabel`/`getByRole`. Mueve los locators a `GastosPage`. Repasa las secciones 4.2–4.5 de la lección."

## Conexión con el proyecto / capstone
- Es el músculo del **Capstone F2** cuando tiene UI: un solo e2e robusto sobre el flujo crítico, con Page Object, como prueba de que la "demo que corre" del Definition of Done no se romperá en silencio. Y es el mismo instinto —verificar el comportamiento de punta a punta, no las piezas sueltas— que en la Fase 6 se vuelve el eval harness de la IA.
