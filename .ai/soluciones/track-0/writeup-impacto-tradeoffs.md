---
ejercicio_id: track-0/writeup-impacto-tradeoffs
fase: track-0
sub_unidad: "T0.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). El contenido varía según el proyecto
> del alumno; esto es un **molde de calidad**, no una respuesta única. Lo que se mide es si las decisiones
> son reales (con alternativa y porqué) y si las métricas son honestas.

# Solución de referencia — Del "hice X" al "X redujo Y" + write-up de trade-offs

## 1. Write-up de trade-offs (molde, sobre el capstone agéntico de `brief.md`)

### Decisión 1 — Validación de salida + human-in-the-loop antes de ejecutar
- **Elegí:** que el agente valide su clasificación contra un esquema y pida confirmación humana para
  acciones sensibles (cerrar el ticket de un cliente) antes de ejecutar.
- **Descarté:** el agente totalmente autónomo que ejecuta directo.
- **Por qué:** una clasificación errónea que cierra el ticket de un cliente real cuesta mucho más que el
  segundo de latencia de validar. Least-privilege + HITL es lo que hace al agente seguro de poner en prod.
- **Hilo de producción:** seguridad/HITL (Definition of Done §6: validación de salida + least-privilege +
  HITL para acciones sensibles + techo de costo).

### Decisión 2 — Ruteo de modelos + caché semántico por costo
- **Elegí:** rutear el ~80% de tickets comunes a un modelo barato y reservar el caro para los ambiguos.
- **Descarté:** usar el modelo caro siempre.
- **Por qué:** baja el costo por ticket de forma medible sin perder calidad en los casos fáciles. El
  costo/latencia es un requisito de producción, no un detalle.
- **Hilo de producción:** costo-latencia (token budgeting + USD/request + ruteo de modelos).

### (Decisión 3 opcional) — Fallback determinista ante salida fuera de esquema
- **Elegí:** ante una respuesta del LLM fuera del esquema, reintentar una vez y, si falla, escalar a humano.
- **Descarté:** confiar en la salida del LLM sin validar / reintentar en bucle.
- **Por qué:** "nunca confíes en la salida del LLM sin validar"; un escalamiento controlado es preferible a
  ejecutar basura o colgar el sistema.
- **Hilo de producción:** observabilidad/manejo de fallas (traza del call-chain con tokens/latencia/costo).

## 2. Tres bullets de impacto (molde)

1. "Automaticé el triage de tickets de soporte, bajando el tiempo de clasificación de ~15 min a menos de
   1 min por ticket (~90% menos)." — **(estimado)**
2. "Reduje el costo por ticket ~60% ruteando el 80% de los casos comunes a un modelo barato y reservando el
   caro para los ambiguos." — **(medido)**
3. "Atrapé el ~4% de clasificaciones fuera de esquema con un paso de validación antes de ejecutar, evitando
   acciones erróneas sobre tickets de clientes." — **(medido)**

## 3. Checklist de los tres no-negociables (molde)

| No-negociable | Estado | Acción de cierre |
|---|---|---|
| Demo que CORRE | parcial (no desplegado) | grabar video real de 60-90 s con un ticket de verdad |
| README en inglés | sí | — |
| Write-up de trade-offs | sí (este documento) | — |

## Puntos donde el corrector debe mirar
1. **¿Las decisiones tienen alternativa real?** "Usé FastAPI/Postgres" no es decisión: no hay trade-off
   visible. Una decisión nombra el camino descartado y por qué.
2. **¿El porqué es defendible o circular?** "Porque es mejor" no cuenta. El porqué fuerte compara el **costo
   de la falla** con el costo de la opción elegida.
3. **¿Las métricas están marcadas medido/estimado?** Un número sin marcar se cae en la entrevista. Números
   redondos perfectos presentados como medidos sin forma de haberlos medido = señal de inflado/IA.
4. **¿≥1 decisión toca un hilo de producción?** Dos decisiones cosméticas no alcanzan.
5. **¿Screenshot contado como demo que corre?** Error: el no-negociable exige link vivo o video real.

## Rango de soluciones aceptables
- Cualquier par de decisiones con alternativa real y porqué defendible es válido, aunque no sean las de este
  molde (el proyecto del alumno puede ser otro). Lo que importa es el **formato decisión → alternativa →
  porqué** y que al menos una toque producción.
- Métricas honestamente **estimadas** son perfectamente aceptables (incluso preferibles a medidas dudosas);
  lo inaceptable es un número preciso presentado como medido sin base.
- Si el alumno articula su **propio** proyecto en vez del brief, se evalúa igual contra los criterios; no se
  exige que use el dominio de tickets.
