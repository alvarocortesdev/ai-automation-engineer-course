---
ejercicio_id: fase-5/auditoria-finops
fase: fase-5
sub_unidad: "5.8"
version: 1
---

# Rúbrica — Auditoría FinOps

> Rúbrica **analítica** atada a los `objetivos` del contrato. No hay test automático: se corrige por
> la **calidad del diagnóstico, el orden por impacto y la viabilidad de los recortes**, no por una
> redacción única. Un plan distinto pero bien argumentado (otro umbral de budget, otra forma de servir
> los PDFs) es válido si el alumno defiende el trade-off y no rompe la app.

## Objetivos evaluados

- O1: Diagnosticar las trampas de costo a partir de la factura, ordenadas por impacto en dólares.
- O2: Diseñar el control faltante: tags + budget con umbrales + qué apagar/redimensionar sin romper la app.
- O3: Rehacer la estimación previa por driver, con supuestos, que habría anticipado el golpe.

## Criterios y niveles

### C1 — Diagnóstico ordenado por impacto (¿encuentra el balde grande?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Ataca el storage (92 centavos) o "la app usa mucha memoria"; no identifica el egress ni el compute always-on. |
| **en-progreso** | Encuentra algunas trampas pero el orden no es por dólares (alfabético / orden de la tabla), o se le escapa el NAT o la 2ª VM. |
| **competente** | Ordena por impacto: **egress (153)** y **las dos VMs 24/7 (140)** y **NAT (71)** arriba; storage al fondo; marca disco huérfano y 2ª VM como cero-valor. |
| **excelente** | Además explica el mecanismo de cada uno (egress = mover, no guardar; NAT = base fija + procesado encima del egress; "detener ≠ borrar" para el disco) y cuantifica el cero-valor (78 USD que no aportan nada). |

### C2 — Plan de control viable (tags + budget + recortes) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No propone budget ni tags, o "recorta" cosas que dejan la app sin funcionar (borra la VM principal, la DB). |
| **en-progreso** | Propone budget/tags vagos ("poner un budget") sin umbrales concretos, o recortes sin estimar ahorro. |
| **competente** | Tags con propósito (proyecto/entorno/dueño), budget con **umbrales concretos** (p. ej. 50/80/100% de un monto + forecast), recortes con ahorro estimado que respetan la app. |
| **excelente** | Distingue quick-wins sin riesgo (apagar 2ª VM + borrar disco huérfano = ahorro inmediato) de cambios de arquitectura (CDN para egress, scale-to-zero para la VM principal) con su trade-off; ADRs de una línea. |

### C3 — Estimación previa reconstruida (constructive alignment) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No reconstruye estimación, o repite la factura sin supuestos. |
| **en-progreso** | Estima por driver pero sin supuestos explícitos, o no señala qué supuesto habría disparado la alarma. |
| **competente** | Tabla `driver → estimación → supuesto` con un total razonable y nombra el supuesto crítico (volumen de egress de PDFs). |
| **excelente** | Conecta la estimación con un budget cuyo umbral, de haber existido, habría avisado el día ~5; menciona el techo de costo del LLM como línea propia (puente a F6). |

## Errores típicos a marcar

- Optimizar el storage (línea más barata) e ignorar el egress (la más cara). Mide antes de optimizar.
- Ordenar los hallazgos alfabéticamente o por el orden de la tabla, no por impacto en dólares.
- No ver la 2ª VM "de pruebas" ni el disco huérfano (gasto cero-valor que se apaga/borra gratis).
- Confundir "detener" con "borrar" el disco huérfano (detener la VM no necesariamente frena el disco).
- Proponer un budget "para enterarse a fin de mes" en vez de alertas por umbral/forecast (el punto es avisar ANTES).
- Recortes que rompen la app (borrar la DB, apagar la VM que sí sirve sin alternativa).
- (transversal) Ningún ADR ni un solo trade-off defendible cuando se pidió.

## Señales de dependencia-IA

- Lista exhaustiva y genérica de "mejores prácticas FinOps" sin aterrizar en **esta** factura ni en sus números concretos.
- Recomendaciones sofisticadas (Savings Plans, Spot, autoscaling multi-región) impropias para una app de portafolio y que no atacan el balde grande real.
- Orden "por impacto" declarado pero los dólares no calzan con la tabla (señal de que no hizo la aritmética).
- Plan impecable pero no puede decir qué le pasa a la app si apaga la 2ª VM (no entiende qué hace cada recurso).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Suma las líneas de mayor a menor. ¿Cuál es la #1 y a qué driver pertenece? No es el storage."
- **Pregunta socrática (nivel 2):** "De los recursos encendidos, ¿cuáles aporta algo a la app y cuáles solo queman plata? ¿Cuánto ahorras apagando exactamente lo que no sirve, sin tocar lo que sí?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Orden por impacto: egress (153) > VMs 24/7 (140, una inútil) > NAT (71) > DB (14) > huérfano (8) > storage (1). Quick-wins sin riesgo: apaga la 2ª VM y borra el disco huérfano (−78). Cambio de arquitectura: CDN para no pagar egress de origen y scale-to-zero para la VM principal. Y pon un budget con alerta al 50/80/100%. Revisa las secciones 4 y 5 de la lección."

## Conexión con el proyecto / capstone

- El budget con alerta de este ejercicio es un **entregable concreto** del [capstone F5](/fase-5-devops/proyecto/): la cuenta del proyecto debe tener uno puesto. El reflejo de "estimar antes, poner tope" es el mismo techo de costo de un agente de IA en F6/F7.
