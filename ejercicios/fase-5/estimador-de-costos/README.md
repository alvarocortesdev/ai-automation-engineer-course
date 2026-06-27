# Ejercicio 5.8 — Estimador de costos cloud (con la trampa del egress)

> **Modalidad: código (verificado por `pytest`, sin cuenta cloud).** Estimar el costo de una
> arquitectura **antes** de desplegarla es el primer reflejo de FinOps. No se despliega nada: se
> calcula. Es el mismo hábito que en la Fase 6 te salva de una factura de tokens fuera de control.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.8` Costos cloud
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Estimar el costo mensual de una arquitectura descomponiéndolo en los **4 drivers** (compute, storage, egress, requests).
- **O2** — Tratar correctamente el **tramo gratis de egress** (nunca negativo) y el compute **always-on vs. scale-to-zero** (cobrar por horas encendido).
- **O3** — Devolver un **desglose por driver** además del total, para poder explicar de dónde sale cada dólar.

## 📋 Contexto

Es el boceto de presupuesto de tu app del [capstone F5](/fase-5-devops/proyecto/): antes de subirla,
quieres saber si te costará USD 17 o USD 170 al mes, y **de qué balde** sale el grueso. La cifra que
calcules aquí va directo a tu write-up de trade-offs ("elegí scale-to-zero porque a este tráfico
cuesta ~X vs. ~Y de una VM 24/7").

## 📏 Primero-Sin-IA (en este orden, timebox 40 min)

1. Resuélvelo **solo**, a mano. Lee el contrato en `estimador.py` y hazlo pasar test por test.
2. Solo entonces, consulta **documentación oficial** (la sección 9 de la lección tiene los enlaces a las calculadoras).
3. **Solo al final**, usa IA para *revisar* tu código —no para generarlo.
4. Mañana, reescribe la función de memoria. Si no puedes, no la aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `estimador.py` y completa `estimar_costo_mensual` (no cambies la firma ni las claves del dict de salida).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos pasen en verde**. El caso clave: egress por debajo del tramo gratis = **0** (no negativo).
4. Añade **al menos un caso de prueba tuyo** en `test_estimador.py` (sugerencia: un escenario "viral" donde el egress domina el total, o uno sin el NAT Gateway always-on).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan (incluido egress=0 por debajo del tramo gratis).
- [ ] El egress nunca es negativo (`max(0, …)`).
- [ ] El `total` es exactamente la suma de los 4 drivers del desglose.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar sin notas** por qué el NAT always-on domina el total del caso de ejemplo, y cuándo una VM 24/7 le gana al scale-to-zero.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El egress es el único driver con truco: resta el tramo gratis **antes** de multiplicar, y protege con
`max(0, egress_gb - egress_gratis_gb)` para que servir menos que el tramo gratis no dé un número
negativo. El compute es una suma simple sobre la lista: `usd_por_hora * horas_encendido` de cada
recurso (por eso un recurso con 730 horas —always-on— pesa tanto). El `total` no es un cálculo
aparte: es la suma de los cuatro valores que ya calculaste. Revisa la sección 4 y 6 de la lección
antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/estimador-de-costos.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/estimador-de-costos.md` — no la mires
antes de intentarlo de verdad.
