---
ejercicio_id: fase-3/circuit-breaker-estados
fase: fase-3
sub_unidad: "3.14"
version: 1
---

# Rúbrica — Circuit breaker: la máquina de estados (a mano)

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `solucion.py` + `bitacora.md` con
> `test_acceptance.py` en verde (reloj inyectado, sin esperas reales). Pasar los tests verifica
> las transiciones; la `bitacora.md` verifica que el alumno distingue breaker de retry.

## Objetivos evaluados
- **O1** — Tres estados (closed/open/half-open) con las transiciones correctas.
- **O2** — Rechazar sin invocar `fn` estando abierto; permitir UNA prueba al pasar la ventana.
- **O3** — Explicar la diferencia breaker vs retry y el propósito del half-open.

## Criterios y niveles

### C1 — Corrección de la máquina de estados · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_acceptance.py` en rojo: no abre al umbral, invoca `fn` estando abierto, o no llega nunca a half-open. |
| **en-progreso** | Closed/open funcionan pero half-open falla: la prueba exitosa no cierra, o la fallida no reabre/no reinicia el temporizador. |
| **competente** | Todos los tests en verde: abre al umbral, rechaza sin invocar `fn`, half-open tras la ventana, prueba exitosa cierra, fallida reabre con temporizador reiniciado, éxito reinicia el contador. |
| **excelente** | Verde + `estado` derivado limpio (open con ventana cumplida se reporta half-open) y `llamar` que reusa esa misma condición; sin duplicar la lógica del reloj. |

### C2 — Disciplina de las transiciones · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cuenta fallos TOTALES en vez de consecutivos (un éxito no reinicia el contador). |
| **en-progreso** | Reinicia el contador en éxito pero olvida reiniciar el temporizador al reabrir desde half-open (el breaker se queda "casi abierto"). |
| **competente** | Fallos consecutivos (éxito → 0); al reabrir desde half-open marca el instante de nuevo; rechazo inmediato sin tocar `fn`. |
| **excelente** | Maneja el caso `umbral_fallos=1`; el reloj es monotónico inyectable (no `datetime.now()` ni `time.time()`, que pueden retroceder). |

### C3 — Comprensión demostrada (bitácora) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `bitacora.md` ausente o "es como un retry". |
| **en-progreso** | Describe los estados pero no contrasta breaker (deja de intentar) con retry (insiste). |
| **competente** | Explica que el retry asume falla breve y el breaker asume falla prolongada; el half-open prueba si la dependencia volvió sin abrir las compuertas de golpe. |
| **excelente** | Conecta con costo/latencia: el breaker convierte fallas lentas (timeout × intentos) en fallas rápidas, y protege a la dependencia caída de la avalancha. |

## Errores típicos a marcar
- **Invocar `fn` estando abierto:** si llama y atrapa, no está protegiendo nada; el breaker debe rechazar ANTES de llamar.
- **Contar fallos totales, no consecutivos:** un éxito intercalado debe reiniciar el contador; si no, abre por acumulación histórica.
- **Half-open que deja pasar varias pruebas:** debe ser UNA; varias en paralelo reabren la avalancha que el breaker evita.
- **No reiniciar el temporizador al reabrir desde half-open:** la siguiente prueba llegaría de inmediato en vez de esperar otra ventana.
- **Usar `time.time()` en vez del reloj inyectado:** rompe los tests deterministas y, en prod, `time.time()` puede retroceder (NTP); `monotonic` no.
- **Estado half-open no observable:** si `estado` no refleja la ventana cumplida, el test `test_tras_la_ventana_queda_half_open` falla.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Trae una implementación con `threading.Lock`, métricas, o ventana deslizante de fallos (sliding window) no pedida — sofisticación impropia del enunciado.
- Código correcto pero no sabe explicar por qué half-open deja pasar **una sola** llamada.
- **Verificación sugerida:** pídele que prediga el estado tras `falla, falla, éxito, falla, falla` con `umbral=3` (queda `closed`: el éxito reinicia, solo hay 2 fallos finales). Y en qué se diferencia de un retry. Si no puede, no razonó la FSM.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de la clase antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Estando 'open', ¿tu `llamar` invoca `fn` y atrapa el error, o rechaza ANTES de llamar? Debe ser lo segundo."
- **Pregunta socrática (nivel 2):** "Cuando pasa la ventana de espera, ¿cómo sabe el breaker que puede volver a probar, y por qué deja pasar UNA llamada y no todas las que lleguen?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Deriva `estado`: si interno=='open' y `reloj()-abierto_en >= espera` → 'half-open'. En `llamar`, si `estado=='open'` lanza `CircuitoAbierto`; en el `except`, si estabas en half-open reabre y `abierto_en=reloj()`, si no incrementa y abre al umbral. Repasa 4.5."

## Conexión con el proyecto / capstone
- Es la protección de cualquier dependencia externa crítica del capstone (proveedor de pagos, otra API). Junto con el retry y la idempotency key cierra el trío de resiliencia del Definition of Done, y la decisión de umbral/ventana es material de ADR.
