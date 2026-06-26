# Escenarios candidatos a test — App de finanzas "Gastos"

> Material del ejercicio 2.10 (presupuesto de la pirámide). NO escribas tests aquí:
> tu trabajo es **decidir el nivel** de cada uno y justificarlo. Lee la lección
> ([`2.10`](/fase-2-ingenieria/2-10-playwright-e2e/)) y la pirámide de [`2.6`](/fase-2-ingenieria/2-6-testing-fundamentos/).

Una app web de finanzas personales (frontend + API + base de datos) tiene estos 8
escenarios que alguien propuso "testear". Para cada uno se describe qué hace.

1. **Login.** El usuario escribe email y contraseña correctos, presiona "Entrar" y ve
   su panel con sus gastos. Si la contraseña es incorrecta, ve un error. Es la puerta
   de entrada: si se rompe, nadie puede usar la app.

2. **Agregar un gasto desde la UI.** El usuario llena descripción y monto en un
   formulario, hace clic en "Agregar", y el gasto aparece en la lista y suma al total.
   Es una de las acciones más usadas del producto.

3. **Cálculo del total del mes.** Una función `calcularTotal(gastos)` recibe una lista
   de gastos y devuelve la suma, ignorando los marcados como "anulados". Pura aritmética
   sobre datos en memoria; no toca red ni navegador.

4. **Validación del campo monto.** Una función `validarMonto(texto)` devuelve `true`
   solo si el texto representa un número positivo (rechaza `""`, `"abc"`, `"-5"`, `"0"`).
   Lógica pura, con varios bordes.

5. **Flujo de pago de una deuda.** El usuario elige una deuda, ingresa los datos de su
   tarjeta, confirma, y la app le muestra un comprobante de pago exitoso y marca la deuda
   como pagada. Es el flujo que genera ingresos: si falla en silencio, se pierde plata.

6. **Formateo de fecha.** Una función `formatearFecha(iso)` convierte `"2026-06-25"` en
   `"25-06-2026"`. Cadena entra, cadena sale; sin efectos secundarios.

7. **Endpoint `GET /api/gastos`.** Devuelve, en JSON, los gastos del usuario autenticado
   leyéndolos de la base de datos, y rechaza con 401 si no hay token. Es la frontera entre
   tu código y la base de datos.

8. **Render del gráfico de gastos por categoría.** Un componente dibuja un gráfico de
   barras con los totales por categoría usando una librería de charts de terceros. Lo que
   importa es que reciba los datos correctos; los píxeles exactos los pinta la librería.

---

## Tu entregable

- `decisiones.md` — para cada uno de los 8: `e2e` / `integración` / `unit` / `no-testear`,
  con **una frase** de justificación (valor vs. costo).
- `politica-piramide.md` (máx. 1 página) — la política de e2e que propondrías al equipo.
