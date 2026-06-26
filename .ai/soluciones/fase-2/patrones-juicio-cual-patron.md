---
ejercicio_id: fase-2/patrones-juicio-cual-patron
fase: fase-2
sub_unidad: "2.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio **no tiene respuesta única**:
> esta solución da las decisiones *bien defendidas* como vara de medir, pero un alumno que elige el bando
> contrario con un trade-off explícito y un gatillo observable puntúa igual o mejor. Se evalúa el **razonamiento**.

# Solución de referencia — El juicio: ¿qué patrón, o ninguno?

## El eje que ordena los cuatro escenarios

La pregunta no es "¿qué patrón sé?", sino **"¿cuántas fuerzas reales y presentes empujan a abstraer?"**:

- **Una sola fuerza, y especulativa** ("quizás algún día") → **no abstraer** (Rule of Three / YAGNI), con gatillo.
- **Dos o más fuerzas reales y presentes** (testabilidad *hoy* + cambio *probable* + duplicación *actual*) → **abstraer**.

| Escenario | Fuerzas presentes | Decisión defendida |
|---|---|---|
| 1 — exportador PDF único | 1, especulativa ("quizás Excel") | **Ninguno (YAGNI)** + gatillo |
| 2 — cliente LLM en 8 sitios | 2 reales (testabilidad hoy + migración probable) | **Adapter** |
| 3 — `confirmar_pedido` 2 cosas fijas | 1, especulativa ("por si acaso") | **Ninguno (Observer sería pattern-itis)** + gatillo |
| 4 — SQL crudo duplicado en `users` | 2-3 reales (duplicación hoy + testabilidad + más queries) | **Repository** |

## Decisión por escenario

### 1 — El exportador de un solo formato → **NINGUNO (YAGNI)**
- **(b) Smell:** *ausente*. No hay un `if/elif` de formatos que crezca; hay un solo formato. El "quizás algún día Excel" es especulación, no un eje de variación presente.
- **(c) Trade-off:** *a favor* de abstraer está OCP/Strategy (preparar la extensión); *en contra*, YAGNI + Rule of Three: con un solo caso adivinas el eje de variación y casi siempre mal; la interfaz + clases vacías son indirección sin beneficio (speculative generality).
- **(d) Gatillo:** "si entra un segundo formato real (Excel confirmado, no 'quizás'), refactorizo a Strategy + una Factory que construya el exportador desde el string." Ahí el smell existe.

### 2 — El cliente de LLM en 8 sitios → **ADAPTER**
- **(b) Smell:** *presente*. (i) Acoplamiento a un tercero esparcido en 8 call sites (shotgun surgery latente); (ii) imposibilidad de testear sin gastar tokens (la dependencia concreta no se puede sustituir).
- **(c) Trade-off:** *a favor*, dos fuerzas **reales y presentes**: testabilidad *hoy* (un fake del adapter en los tests) + migración *probable* el próximo trimestre. *En contra*, el costo de una capa de traducción —pero aquí se paga sola con la testabilidad inmediata.
- **(d) Gatillo:** no aplica (se decide abstraer ya). Nota: el Adapter es además la frontera para validar la salida del LLM (OWASP LLM05) y para meter caching de costo/latencia.

### 3 — `confirmar_pedido` que hace dos cosas fijas → **NINGUNO (Observer sería pattern-itis)**
- **(b) Smell:** *ausente o incipiente*. Hay solo dos reacciones (guardar + email) y **no crecen** ni pertenecen a actores distintos en conflicto. El *divergent change* que justifica Observer aún no aparece.
- **(c) Trade-off:** *a favor* del Observer está el desacople; *en contra*, su costo específico —**control de flujo invisible**: leer `confirmar_pedido` dejaría de decirte qué pasa, y debuggear se vuelve "¿quién está suscrito?". Para dos líneas explícitas, ese costo no se paga.
- **(d) Gatillo:** "si llega una **tercera** reacción pedida por **otro equipo** (growth quiere analytics, bodega quiere descontar stock), y la lista empieza a crecer, *ahí* introduzco Observer." El smell será real entonces.

### 4 — El acceso a la tabla `users` → **REPOSITORY**
- **(b) Smell:** *presente*. *Duplicated code* + *persistencia mezclada con el negocio*: tres funciones repiten SQL crudo de `users`; cualquier cambio de esquema es shotgun surgery.
- **(c) Trade-off:** *a favor*, fuerzas reales y presentes: duplicación *hoy* + testabilidad del negocio sin Postgres + más queries *en el roadmap*. *En contra*, el costo de la abstracción —pero no es un passthrough trivial: hay lógica de consulta de dominio que merece nombre (`listar_activos`, etc.).
- **(d) Gatillo:** no aplica. Aviso: si fuera **una sola** query trivial sin testabilidad ganada, el Repository sería el non-example de la sección 4.3 (passthrough YAGNI).

## Cómo distinguir competente de excelente
- **Competente:** acierta los dos "ninguno" (1, 3) en vez de abstraer por reflejo, y nombra smell + trade-off + gatillo en cada uno.
- **Excelente:** enuncia la **regla general** ("cuento fuerzas reales y presentes; una especulativa no basta") y la aplica de forma consistente; conecta cada "en contra" con el costo específico del patrón (Observer→flujo invisible, Repository passthrough→indirección vacía).

## Errores a marcar (resumen)
- Abstraer en 1 o 3 "porque es buena práctica" = pattern-itis.
- Tratar el 2 o el 4 como especulativos cuando tienen testabilidad **presente**.
- Confundir patrones (Factory↔Adapter, Strategy↔Observer): el smell los distingue.
- Decisiones de "no" sin gatillo observable.
