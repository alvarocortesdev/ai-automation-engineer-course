---
ejercicio_id: fase-2/playwright-presupuesto-e2e
fase: fase-2
sub_unidad: "2.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio es de **juicio**: no hay una única etiqueta correcta por escenario, sino una **justificación valor/costo** defendible. Premia el razonamiento, no el calce exacto con esta tabla.

# Solución de referencia — Presupuesto de la pirámide: qué merece e2e y qué no

## Respuesta canónica (lo que debe haber en `decisiones.md`)

| # | Escenario | Nivel de referencia | Justificación (valor vs. costo) |
|---|---|---|---|
| 1 | **Login** | **e2e** | Flujo de usuario de punta a punta y **crítico**: si se rompe, **nadie** entra a la app. El valor justifica el costo de un e2e. Es el caso de libro. |
| 2 | **Agregar gasto desde la UI** | **e2e** *o* **integración** (defendible) | Fronterizo. Va a **e2e** si es el corazón del producto y el flujo (form → lista → total) importa de punta a punta; va a **integración** si la UI es trivial y basta probar `POST /gastos` contra una DB de prueba. Lo que se evalúa es que **justifique** su elección, no la etiqueta. |
| 3 | **Cálculo del total del mes** | **unit** | **Lógica pura** (suma ignorando "anulados"): no necesita navegador. Un unit test de milisegundos cubre los bordes (lista vacía, todos anulados, montos negativos) mejor y 100× más barato que un e2e. |
| 4 | **Validación del campo monto** | **unit** | Función pura con **muchos bordes** (`""`, `"abc"`, `"-5"`, `"0"`). Cada borde es un unit test trivial. Probarlos por la UI sería lento, frágil y dejaría bordes sin cubrir. |
| 5 | **Flujo de pago de una deuda** | **e2e** | Punta a punta y **el flujo que da plata**: si falla en silencio, se pierde dinero. Es el otro e2e indiscutible. Tocar tarjeta + comprobante + estado de la deuda exige verificar el sistema completo. |
| 6 | **Formateo de fecha** | **unit** | Cadena entra, cadena sale, sin efectos secundarios. El unit test ideal. Un e2e aquí es desperdicio puro de la pirámide. |
| 7 | **Endpoint `GET /api/gastos`** | **integración** | Es la **frontera** entre tu código y la base de datos (incluye el 401 sin token). Un test de integración (API real contra DB de prueba) da la confianza sin levantar un navegador. No es un flujo de usuario en pantalla. |
| 8 | **Render del gráfico por categoría** | **no-testear con e2e** (verificar el **dato**: unit/integración) | Los píxeles los pinta una **librería de terceros**: testearlos es frágil y de bajo valor. Lo que sí importa —y es barato— es un unit/integración que verifique que **los datos correctos** (totales por categoría) llegan al componente. |

**Núcleo no negociable:** **1 y 5 son los e2e**; **3, 4 y 6 son unit**; **7 es integración**; **8 no es e2e**. El **#2** es el caso fronterizo legítimo (e2e o integración, con argumento).

## Razonamiento paso a paso

La heurística que ordena todo es de **dos preguntas**, en este orden:

1. **¿Es un flujo de usuario de punta a punta Y crítico?** (Si se rompe, ¿pierdo plata o usuarios?) → candidato a **e2e**. Solo dos escenarios pasan ambos filtros: login (#1) y pago (#5).
2. **Si no, ¿dónde vive el riesgo?**
   - Riesgo en **lógica pura** (cálculo, validación, formateo) → **unit**. Nunca un navegador para verificar una suma o un regex: caro, lento y peor en cobertura de bordes (#3, #4, #6).
   - Riesgo en la **frontera** con otro sistema (DB, API, cola) → **integración** (#7).
   - Riesgo en **algo de terceros que no controlas** (el render de una librería de charts) → no lo testees a nivel de píxel; **verifica el dato de entrada** con un test barato (#8).

El principio detrás: la pirámide asigna **cobertura por costo**. El e2e da mucha confianza por test (cubre frontend + API + datos), pero cuesta segundos por corrida y se rompe con cualquier cambio de UI o red lenta. Por eso la cima es estrecha **a propósito**: solo lo que de verdad lo amerita. Invertir esto —un e2e por feature— es el **cono de helado**: suite lenta, flaky y, al final, ignorada por el equipo.

## Política de pirámide de referencia (lo que debe haber en `politica-piramide.md`)

Una política aceptable responde, **con el porqué**, las cuatro preguntas:

- **Cuántos y sobre qué (forma de pirámide, no cono):** muy pocos e2e —en esta app, **login y flujo de pago**—, reservados para flujos de usuario de punta a punta y críticos. Toda la lógica de negocio (totales, validaciones, formatos) se cubre con **unit** tests baratos, que son la base ancha. Las fronteras (API↔DB) van a **integración**. Regla operativa: *"un e2e nuevo se justifica por escrito (¿qué flujo crítico cubre que un test más barato no?), no por defecto."*
- **Selectores:** **por rol/accesibilidad** (`getByRole`, `getByLabel`, `getByText`) y nunca por CSS/`#id`. Razón: los selectores user-facing describen lo que el usuario percibe (estable si el comportamiento no cambia); los CSS describen la implementación interna y se rompen con cualquier refactor de markup, produciendo rojos que no son bugs. Bonus: fuerzan HTML accesible. `getByTestId` solo como último recurso, justificado.
- **Esperas:** **prohibido `waitForTimeout` como estabilizador.** Toda espera se resuelve con **web-first assertions** (`await expect(locator).toBeVisible()/toHaveText()/toHaveCount()`) que reintentan hasta que el estado esté listo y siguen apenas lo está. Razón: un `sleep` o está corto (flaky) o largo (lento); pierde en ambos casos y **esconde** la causa real (afirmar antes de tiempo) en vez de arreglarla.
- **Cadencia en CI (costo/latencia):** los **pocos e2e críticos corren en cada PR** (gate de merge); las suites más largas y secundarias (multi-navegador, casos no críticos) corren **nightly** o por etiqueta. Razón: los e2e cuestan tiempo (segundos por test) y a veces dinero (navegadores en CI); dispararlos todos en cada push vuelve la suite insufrible y el equipo deja de correrla. Se dosifica, no se dispara.

Una política **excelente** además: nombra el trade-off de `getByTestId` (cuándo sí), admite e2e "secundarios" fuera del happy path solo si el riesgo lo amerita, y conecta el presupuesto de e2e con el mismo criterio que se aplicará a los **evals** en la Fase 6 (la verificación de calidad cuesta y se presupuesta).

## Puntos resbalosos (donde el corrector debe mirar)

1. **El #2 es el termómetro de comprensión.** Cualquiera de las dos respuestas (e2e o integración) es válida **con argumento**. Si el alumno no puede defender qué lo inclinaría a cada lado (¿es el corazón del producto?, ¿la UI tiene lógica propia o es un form trivial?), no razonó: memorizó.
2. **El #8 atrapa al que "testea todo".** Querer un e2e que verifique los píxeles del gráfico de una librería de terceros es el error clásico de bajo valor / alta fragilidad. Lo correcto es testear **el dato** que entra, no el render.
3. **Confundir integración con e2e (#7).** Un endpoint de API **no** es un flujo de usuario en navegador; es frontera código↔DB. Si el alumno lo marca e2e, falta la distinción integración vs. e2e.
4. **Justificación genérica.** Una etiqueta correcta con un "porque es importante" no cumple C2. La justificación debe referirse al **detalle del escenario** (que #3 ignora "anulados", que #4 tiene varios bordes, que #8 usa terceros).
5. **Política que contradice las decisiones.** Si `politica-piramide.md` dice "pocos e2e" pero `decisiones.md` marcó 5-6 e2e, hay incoherencia: marcarla.

## Rango de soluciones aceptables

- **#2 → e2e o integración**, ambos correctos si están justificados. No penalizar ninguno.
- **#8** puede expresarse como "unit del transformador de datos" o "integración del componente con datos de prueba"; ambos cumplen ("no-testear los píxeles" es lo no negociable).
- Discrepar en **1–2 escenarios con un argumento sólido** puede ser señal de dominio, no de error: la rúbrica premia el razonamiento. Lo que **no** se acepta: lógica pura (#3/#4/#6) en e2e, o el cono de helado (casi todo e2e "para estar seguro").
- La política puede estructurarse distinto (tabla, prosa, bullets) mientras responda las **cuatro** preguntas con su porqué.
- Añadir niveles extra que la lección no exige (p. ej. *contract testing* para el #7, *visual regression* controlado para el #8) es **excelente solo si el alumno puede defenderlo**; si aparece como vocabulario decorativo sin sustento, es señal de dependencia-IA (ver rúbrica).
