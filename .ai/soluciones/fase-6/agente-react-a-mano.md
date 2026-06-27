---
ejercicio_id: fase-6/agente-react-a-mano
fase: fase-6
sub_unidad: "6.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — El agent loop ReAct, a mano

## Respuesta canónica (implementación)

```python
def ejecutar_agente(pregunta: str, llamar_modelo) -> ResultadoAgente:
    mensajes = [{"rol": "user", "contenido": pregunta}]

    for paso in range(1, MAX_PASOS + 1):
        # 1. RAZONAR
        resp = llamar_modelo(mensajes)
        # 2. OBSERVAR: guardar el turno del modelo SIEMPRE, antes de decidir.
        mensajes.append({"rol": "assistant", "contenido": resp.content})

        # 3. ¿Terminó? -> no pidió tools: devolver el texto final.
        if resp.stop_reason != "tool_use":
            texto = next((b.texto for b in resp.content if b.tipo == "text"), "")
            return ResultadoAgente(respuesta=texto, pasos=paso, detenido_por="end_turn")

        # 4. GATE + ACTUAR, por cada tool pedida.
        resultados = []
        for b in resp.content:
            if b.tipo != "tool_use":
                continue
            if b.nombre not in HERRAMIENTAS_PERMITIDAS:        # permiso primero
                resultados.append({
                    "tipo": "tool_result", "tool_use_id": b.id,
                    "contenido": "herramienta no permitida", "es_error": True,
                })
                continue
            salida = invocar(b.nombre, b.input)                # ejecutar en tu código
            resultados.append({
                "tipo": "tool_result", "tool_use_id": b.id,
                "contenido": str(salida), "es_error": False,
            })

        # 5. Devolver observaciones y dejar que el for haga la siguiente vuelta.
        mensajes.append({"rol": "user", "contenido": resultados})

    # Techo alcanzado sin un end_turn.
    return ResultadoAgente(respuesta=None, pasos=MAX_PASOS, detenido_por="tope_pasos")
```

Verificado contra `test_agente.py`: **5 passed** (Python 3.12, pytest 9.x).

## Razonamiento paso a paso

El loop son cuatro piezas en un orden que importa:

1. **Razonar** — `llamar_modelo(mensajes)` deja que el modelo decida el siguiente paso.
2. **Observar** — el turno del modelo se añade a `mensajes` **siempre**, antes de
   ramificar. Esa lista es la memoria de corto plazo; si no guardas el turno del modelo,
   la siguiente vuelta pierde el `tool_use` que estás respondiendo y la API real
   rechazaría el `tool_result` huérfano.
3. **¿Terminó?** — `stop_reason != "tool_use"` significa que el modelo no pidió nada más:
   devuelves su texto. Es la única salida "normal" del loop.
4. **Gate + actuar** — `nombre not in HERRAMIENTAS_PERMITIDAS` va **antes** de ejecutar:
   una tool no permitida se rechaza con un `tool_result` de error y **nunca corre**. Solo
   las permitidas pasan a `invocar(...)`.

El **techo** es el propio `range(MAX_PASOS)`: si el `for` se agota sin un `end_turn`,
devuelves `detenido_por="tope_pasos"`. Es lo que separa un agente de un loop infinito.

El punto pedagógico que el corrector debe verificar que el alumno **entiende**: un agente
es el tool use de 6.4 repetido. La vuelta extra de ReAct (3 vueltas para 2 tools) es el
turno final en el que el modelo, con ambas observaciones ya en su memoria, razona y
responde sin pedir más.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Orden dentro de la vuelta.** El error #1 es ejecutar la tool antes del chequeo de
   allowlist, o devolver el texto final sin antes guardar `resp.content` en `mensajes`.
   El orden correcto es razonar → guardar → ¿terminó? → gate → actuar → observaciones.
2. **Conteo de `pasos`.** En el caso de 2 tools, `pasos == 3` (la última vuelta es el
   `end_turn`). Si el alumno cuenta 2, probablemente está devolviendo desde dentro del
   bloque de tools en vez de dejar que el loop vuelva a llamar al modelo.
3. **Techo off-by-one.** Con `MAX_PASOS = 5`, el modelo se llama **exactamente** 5 veces
   en el caso terco (`modelo.llamadas == MAX_PASOS`). Un `range(MAX_PASOS + 1)` o un
   `while True` mal cortado llama de más.
4. **Tool no permitida que igual ejecuta.** Si el `if nombre not in ...` va después de
   `invocar`, o no existe, la tool `borrar_todo` corre — fallo de seguridad aunque algún
   test pase por casualidad. El gate va primero, sin tocar la tool.
5. **`tool_result` sin `tool_use_id`.** Cada observación debe llevar el `tool_use_id` del
   bloque que la pidió; perderlo rompe la correlación (y la API real lo rechaza).

## Rango de soluciones aceptables

- **`for paso in range(1, MAX_PASOS + 1)` vs `range(MAX_PASOS)` con `paso + 1`**: ambos
  válidos mientras el conteo de `pasos` salga correcto y el modelo no se llame de más.
- **`ResultadoAgente` vs una tupla / dict**: el starter da el dataclass; respetarlo es lo
  limpio, pero cualquier retorno con `.respuesta`/`.pasos`/`.detenido_por` accesibles
  cuenta como `competente`.
- **Extraer el texto con `next((b.texto for b ... if b.tipo == "text"), "")` vs un bucle
  explícito**: equivalentes. Manejar el caso "no hay bloque text" con `""` es prolijo
  pero no obligatorio para los tests dados.
- **Procesar todos los bloques tool_use de un turno vs asumir uno solo**: la versión
  robusta itera todos (soporta tool use en paralelo); asumir uno funciona con estos tests
  pero es nivel `competente`, no `excelente`. Un test propio con dos tools en un turno lo
  evidencia.
- Para `verificacion.md`: cualquier texto que ligue el techo a **costo** (tokens por
  vuelta + rate limit) **y** a **seguridad** (cortar un agente descontrolado), y la
  allowlist a least privilege / Excessive Agency (LLM06), es válido; no se exige redacción
  concreta.
