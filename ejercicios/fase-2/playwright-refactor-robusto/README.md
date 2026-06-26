# 2.10 — Estabiliza un e2e flaky (refactor robusto + Page Object)

**Fase:** Fase 2 — Ingeniería de software · **Lección:** [`2.10` Playwright e2e](/fase-2-ingenieria/2-10-playwright-e2e/)
**Ruta:** opcional/profundización · **Timebox:** 40–45 min · **Modalidad:** código

## 🎯 Objetivo

Tomar un test end-to-end **frágil, lento y flaky** y convertirlo en uno **robusto y
determinista**: selectores por rol/label en vez de CSS, web-first assertions con
auto-waiting en vez de un `sleep`, y un **Page Object** que separe el *qué* del *cómo*.
Es el músculo central de la lección, aplicado contra una app que corre de verdad.

## 📋 Contexto

`app.html` es el **SUT** (system under test): una mini-app de "agregar gasto" que
**funciona correctamente**. NO la modifiques. Dos detalles de diseño importan para tu test:

- El mensaje de éxito (`Gasto agregado: ...`) aparece tras una **latencia variable**
  (~150–450 ms): por eso leer el texto de inmediato falla y un `waitForTimeout` es frágil.
- El form es **accesible** (`<label>` + `<button>`), así que `getByLabel` y `getByRole`
  funcionan. El error de validación vive en un elemento con `role="alert"`.

El archivo `gastos.spec.ts` de partida "pasa hoy", pero arrastra **tres antipatrones**:
1. Selectores acoplados a la implementación (`#desc`, `.btn-add`, `.toast`).
2. `await page.waitForTimeout(1000)` — un `sleep`.
3. `textContent()` + `expect` manual — una foto inmediata, no una espera.

Y solo cubre el camino feliz.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Diagnostica los antipatrones **antes**
   de tocar el teclado.
2. Solo entonces, consulta las [best practices oficiales de Playwright](https://playwright.dev/docs/best-practices)
   y la [guía de locators](https://playwright.dev/docs/locators).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, reescribe el Page Object **de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

> ⚠️ **Usa pnpm, nunca npm.** Es la regla del curso para todo proyecto JS/TS.

1. Instala dependencias y los navegadores (una sola vez):

   ```bash
   pnpm install
   pnpm exec playwright install chromium
   ```

2. Corre el test de partida para verlo "pasar pero lento":

   ```bash
   pnpm test
   ```

3. **Diagnostica** en `diagnostico.md`: lista los antipatrones y por qué cada uno hace
   al test frágil, lento o flaky.
4. **Refactoriza** `gastos.spec.ts` y **completa** `gastos.page.ts`:
   - selectores `getByRole` / `getByLabel` / `getByText` (o `getByTestId` solo si no hay
     alternativa, justificado),
   - web-first assertions (`await expect(locator).toBeVisible()` / `toHaveText()` /
     `toHaveCount()`), **sin un solo `waitForTimeout`**,
   - un Page Object `GastosPage` con los locators y un método `agregar(desc, monto)`;
     el `.spec.ts` no debe tener selectores crudos.
   - cubre **dos** caminos: el feliz (gasto válido se agrega) y el de **validación**
     (monto inválido → aparece el error con `role="alert"`).
5. Corre la suite **3 veces seguidas**: debe pasar las 3 (determinista).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `diagnostico.md` existe y nombra los 3 antipatrones **antes** del refactor.
- [ ] El test **no** usa ningún `waitForTimeout` ni selector CSS/`#id`.
- [ ] Las verificaciones son web-first assertions, no `textContent()` + `expect` manual.
- [ ] Existe `gastos.page.ts` con la clase `GastosPage`; el `.spec.ts` no tiene selectores crudos.
- [ ] Cubres el camino feliz **y** el de validación (monto inválido).
- [ ] `pnpm test` pasa **3 de 3** corridas seguidas, sin tocar `app.html`.
- [ ] Puedes explicar **sin notas** por qué `toBeVisible()` reemplaza al sleep sin volver lento el test.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `gastos.spec.ts` — tu test refactorizado, verde y determinista.
- `gastos.page.ts` — tu Page Object completo.
- `diagnostico.md` — los antipatrones que encontraste y por qué.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Reemplaza **toda** la espera por una sola línea:
`await expect(page.getByText("Gasto agregado")).toBeVisible();` — auto-espera lo justo,
robusto ante la latencia variable. Para el resto:

```ts
// en gastos.page.ts
this.descripcion = page.getByLabel("Descripción");
this.monto = page.getByLabel("Monto");
this.agregar = page.getByRole("button", { name: "Agregar" });
this.mensajeExito = page.getByText("Gasto agregado");
this.error = page.getByRole("alert");
this.items = page.getByRole("listitem");
```

El camino de validación: llena un monto inválido (`"abc"`, `"-1"` o `"0"`), haz clic y
`await expect(gastos.error).toHaveText("Monto inválido")`. La aserción se queda en el
test; las interacciones, en el Page Object. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluidos `gastos.spec.ts`, `gastos.page.ts` y `diagnostico.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/playwright-refactor-robusto.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/playwright-refactor-robusto.md`
— no la mires antes de intentarlo de verdad.
