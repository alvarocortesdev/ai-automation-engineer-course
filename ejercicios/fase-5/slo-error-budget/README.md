# Ejercicio 5.10 — SLO, error budget y la decisión de desplegar

> **Modalidad: a mano (razonamiento, sin IA). Timebox 25–35 min.** No hay código. Eres el ingeniero de guardia de la `api-despensa` y tienes que decidir, con números, si el sistema cumple lo prometido y si puedes desplegar. Esto entrena el músculo que ninguna IA tiene por ti: **decidir bajo un objetivo de confiabilidad explícito.**

## Objetivos

- **O1** — Distinguir **SLI** (la medición), **SLO** (la meta) y **error budget** (`100% − SLO`), y calcular el budget en peticiones y en tiempo.
- **O2** — Tomar una decisión de despliegue justificada por el **budget restante**, no por intuición.
- **O3** — Distinguir **RED** (servicios/usuario) de **USE** (recursos/máquina) y elegir **qué alertar** (síntoma, no causa).

## El escenario

Operas la `api-despensa`. Los datos de la ventana actual:

- **Meta de negocio:** "el **99.9%** de las peticiones deben responder con éxito (status 2xx) y en **menos de 300 ms**, medido en una ventana de **30 días**".
- **Tráfico de la ventana:** **2.000.000** de peticiones.
- **Fallos acumulados este mes:** **1.500** peticiones (un incidente de ayer que ya se resolvió).
- **Plan:** quieres desplegar una **feature experimental** que, por su historial, **suele causar incidentes**.

## Tu tarea (responde en `respuestas.md`, mostrando los cálculos)

1. **SLI y SLO.** Escribe el **SLI** (qué mides exactamente, con la condición de éxito) y el **SLO** (la meta sobre ese SLI). Explica por qué el umbral de latencia se define sobre el **p99** y no sobre el **promedio**.
2. **Error budget.** Calcula cuántas peticiones puedes fallar en la ventana. Exprésalo también en **minutos equivalentes** de downtime sobre los 30 días. Muestra la aritmética.
3. **La decisión.** Con los 1.500 fallos ya gastados, ¿cuánto budget queda (en peticiones y en %)? ¿Despliegas la feature experimental? Justifica con el número.
4. **RED vs USE.** El p99 de latencia se disparó. Nombra **una métrica RED** que te avisó del síntoma y **una métrica USE** que mirarías para encontrar la causa, y explica la relación entre ambas.
5. **Qué alertar.** De estas cuatro, ¿sobre cuál pondrías una alerta que **despierte a alguien a las 3 AM**, y por qué las otras tres no?
   - (a) CPU del servidor al 75%.
   - (b) Error budget consumido al 90% y la quema **acelerándose**.
   - (c) Un log de nivel `warning`.
   - (d) p50 de latencia en 80 ms.

## Qué entregar

- `respuestas.md` con las 5 respuestas y los cálculos a la vista.

**Hecho significa:**

- [ ] Distingues claramente SLI, SLO y error budget; el cálculo del budget es correcto (peticiones **y** minutos).
- [ ] La decisión de desplegar se justifica con el budget restante, no con "me parece".
- [ ] Explicas RED (mirada del usuario) vs USE (mirada de la máquina) y cómo el síntoma de uno lleva a la causa del otro.
- [ ] Eliges alertar sobre el **síntoma que afecta al usuario / agota el budget**, no sobre una causa sin impacto.
- [ ] Puedes defender por qué perseguir el **100%** de disponibilidad es una mala decisión de ingeniería.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-5/slo-error-budget/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **razonamiento** (la aritmética del budget y la lógica de la decisión), no que llegues a una única "respuesta correcta" en la parte de juicio.
