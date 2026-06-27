---
ejercicio_id: fase-5/slo-error-budget
fase: fase-5
sub_unidad: "5.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es un ejercicio de razonamiento:
> las partes 1, 2 y la aritmética tienen respuesta correcta; las partes 3, 4 y 5 admiten matices
> mientras la **lógica** (decidir por el budget, alertar el síntoma) sea sólida. Penaliza errores
> de fondo (confundir SLI/SLO/budget, alertar causas sin impacto), no el fraseo.

# Solución de referencia — SLO, error budget y la decisión

## 1. SLI, SLO y por qué p99

- **SLI:** la proporción de peticiones "buenas" = `(peticiones con status 2xx Y latencia menor que 300 ms) / (peticiones totales)`, medida en la ventana. (Es un SLI de tipo *request-based*; también se acepta uno de disponibilidad puro 2xx más uno de latencia, separados.)
- **SLO:** ese SLI debe ser `>= 99.9%` sobre la ventana de 30 días.
- **Por qué p99 y no promedio:** el promedio aplasta la cola. Si 95% responde en 100 ms y 5% en 4 s, el promedio (~295 ms) "parece sano" pero el 5% que sufre es invisible. El SLO se define sobre la **experiencia del peor caso razonable** (p95/p99), que es justo de donde salen los tickets de soporte. Un promedio bueno con p99 horrible es un sistema que miente en el dashboard.

## 2. Error budget

- Budget = `100% − 99.9% = 0.1%` del tráfico.
- En peticiones: `0.1% × 2.000.000 = 2.000` peticiones que puedes fallar en la ventana.
- En tiempo: 30 días = `30 × 24 × 60 = 43.200` minutos; el `0.1%` son `~43,2` minutos de downtime equivalente al mes.

## 3. La decisión

- Budget restante = `2.000 − 1.500 = 500` peticiones, es decir **25%** del budget (`500 / 2.000`).
- **Decisión:** queda poco budget (25%) y la feature "suele causar incidentes". Lo prudente es **no desplegar el experimento ahora**, o hacerlo solo detrás de un *feature flag* / *canary* con rollback inmediato y vigilando la quema. Lo defendible es la **lógica**, no un sí/no dogmático: gastar el 25% restante en algo históricamente riesgoso puede agotar el budget y forzar un *freeze*. Si el alumno decide desplegar, debe condicionarlo (canary, % de tráfico, rollback) y reconocer el riesgo sobre el budget. Decisión sin mencionar el budget = incompleto.

## 4. RED vs USE

- **RED (síntoma):** la **D**uration (p99 de latencia) disparándose — y/o la **E**rrors subiendo. Es la mirada del usuario.
- **USE (causa):** la **S**aturation del recurso cuello de botella, p. ej. el **pool de conexiones a Postgres** lleno (peticiones haciendo cola), o **U**tilization de CPU al 100%. Es la mirada de la máquina.
- **Relación:** RED detecta el **síntoma** que sufre el usuario; USE suele tener la **causa**. El flujo es: la latencia (RED) sube → miras saturación del pool/CPU (USE) → encuentras que la cola de conexiones está llena. Complementarios, no redundantes.

## 5. Qué alertar a las 3 AM

- **Se alerta (b): error budget consumido al 90% con la quema acelerándose.** Es la promesa al usuario rompiéndose en tiempo real; amerita acción inmediata (los *burn-rate alerts* de Google SRE son exactamente esto).
- Las otras tres **no** despiertan a nadie:
  - (a) CPU al 75% **sin degradación de servicio** es una causa potencial, no un síntoma; puede ser perfectamente normal. Alertar sobre causas sin impacto genera fatiga de alertas.
  - (c) un `warning` suelto no implica impacto al usuario; va a un dashboard, no a un pager.
  - (d) p50 en 80 ms es **bueno**: no hay nada que atender.
- **Regla:** se alerta sobre **síntomas que afectan al usuario o agotan el budget**, no sobre causas internas sin impacto.

## Extra — por qué no perseguir el 100%

El último 0,01% de disponibilidad cuesta exponencialmente más (redundancia, multi-región, on-call agresivo) por un valor marginal casi nulo para el usuario, que muchas veces no distingue 99.9% de 99.99%. Perseguir el 100% paraliza la entrega de features (cero tolerancia al riesgo = cero despliegues) y desperdicia el error budget, que existe **para gastarse en velocidad**. La confiabilidad perfecta no es una meta de ingeniería: es un costo infinito.

## Notas para el corrector

- **Aritmética no negociable (parte 2 y 3):** 2.000 peticiones, ~43 min, 500 restantes / 25%. Un error aquí (p. ej. calcular 0.01% en vez de 0.1%, o no convertir a minutos) es `en-progreso` aunque el razonamiento cualitativo sea bueno.
- **Confundir SLI/SLO/budget** (usar "SLA" como sinónimo, o llamar SLO a la métrica cruda) → marcar; es el malentendido central.
- **Parte 5:** elegir (a) "porque CPU alta es peligrosa" es el error clásico de alertar **causas** en vez de **síntomas**. Nómbralo.
- **Señal de dependencia-IA:** menciona *burn-rate multiwindow*, *Multi-SLO*, *El Toro* u otros términos avanzados pero no puede hacer la aritmética básica del budget; o da un número exacto de minutos sin mostrar la conversión.
