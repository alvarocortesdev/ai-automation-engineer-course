---
ejercicio_id: fase-2/piramide-decidir-nivel
fase: fase-2
sub_unidad: "2.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Ubica los tests en la pirámide y caza el sobre-mockeo

## Parte 1 — Clasificación de los seis tests

| # | Nivel | Justificación (la frontera decide) |
|---|---|---|
| 1 | **unit** | `calcular_iva(1000)` aislada, sin tocar nada externo: lógica pura, milisegundos. |
| 2 | **e2e** | Navegador real + login + carrito + resumen: el sistema completo como un usuario (Playwright). Pocos y lentos. |
| 3 | **integration** | Toca **Postgres real** a través del repositorio: dos piezas reales (tu código + la DB) verificando el pegamento. |
| 4 | **unit** | `formatear_fecha(d)` con la zona fijada por la propia función: determinista, sin frontera (no usa la hora del sistema). |
| 5 | **integration** | Arranca la app **en memoria** y la golpea con un cliente HTTP de prueba: varias piezas reales del sistema juntas, pero **no** es e2e (no hay navegador ni despliegue completo). |
| 6 | **unit** | `descuento(monto, "vip")` con el tipo pasado como argumento: lógica pura. |

> Los dos que más se confunden: el **3** (parece "solo un repositorio" pero toca DB real → integration, no unit) y el **5** (parece e2e por ser un endpoint, pero la app corre en memoria sin navegador → integration, no e2e).

## Parte 2 — Antipatrones en los fragmentos

### Fragmento A — sobre-mockeo
- **Qué está mal:** `_sumar_items` es una función **pura** (sin frontera). Mockearla con `mocker.patch(..., return_value=100)` hace que el test ya no pruebe el cálculo real del subtotal: solo prueba `100 + IVA`. Si `_sumar_items` tuviera un bug, **el test seguiría verde**. Además, el `mock_sumar.assert_called_once()` acopla el test a un detalle de implementación (que `total_carrito` use *esa* función interna): un refactor inocuo lo rompe.
- **Cómo arreglarlo:** no mockear nada. Pasar items reales y afirmar el `total` real esperado (`assert total_carrito([("pan", 1000, 2)]) == 2380` o el valor correcto). El único caso donde mockear tendría sentido sería si `_sumar_items` cruzara una frontera (consultar precios por red), lo que aquí no ocurre.

### Fragmento B — testear detalle interno
- **Qué está mal:** afirma sobre `_saldo` y `_ultima_operacion`, atributos **internos**. El test verifica *cómo* `Cuenta` guarda el estado, no *qué comportamiento* observa el usuario. Si renombras `_saldo` o cambias la representación interna (sin cambiar el comportamiento), el test se rompe — fragilidad pura.
- **Cómo arreglarlo:** testear comportamiento observable a través de la interfaz pública: `cuenta.depositar(500); assert cuenta.saldo() == 500` (un método público), o el efecto de una operación posterior (`cuenta.retirar(200); assert cuenta.saldo() == 300`). Si no existe un getter público, eso es una señal de diseño: el comportamiento que quieres garantizar debería ser observable.

## Parte 3 — Diagnóstico de la suite 4 e2e / 2 unit

- **Antipatrón:** **cono de helado** (ice-cream cone) — la pirámide invertida: muchos e2e arriba, casi nada de unit en la base.
- **Problemas concretos:** suite **lenta** (los e2e tardan segundos/minutos), **frágil/flaky** (fallan por timeouts, red, estado del navegador, no por bugs reales), y cuando algo falla **no localiza** el problema (te dice "el flujo se rompió", no "esta función falla con este input"). Mantenerla cuesta caro y la gente termina ignorando los rojos.
- **Acción concreta:** empujar la base de la pirámide. Identificar la lógica de negocio que hoy solo cubren los e2e y bajarla a **unit tests** rápidos (mockeando las fronteras). Conservar solo **unos pocos** e2e para los *happy paths* críticos (login + compra), añadir **integration** para el pegamento (DB, endpoints en memoria), y dejar el grueso en unit. Objetivo: muchos unit, algunos integration, pocos e2e.

## Notas para el corrector
- Lo central es la **justificación**, no la etiqueta: un alumno que clasifica los 6 bien "de memoria" pero no puede decir qué frontera toca cada uno no llega a "competente" en C1.
- En el Fragmento A, la prueba de comprensión es que el alumno note que **el test pasaría aunque `_sumar_items` tuviera un bug** — esa es la consecuencia del sobre-mockeo.
- En el Fragmento B, aceptar cualquier reorientación a comportamiento observable (getter público o efecto de operación), no exigir una API concreta.
