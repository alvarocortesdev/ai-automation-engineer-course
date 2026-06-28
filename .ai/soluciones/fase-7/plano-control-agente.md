---
ejercicio_id: fase-7/plano-control-agente
fase: fase-7
sub_unidad: "7.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — El plano de control de un agente que actúa

## Respuesta canónica

```python
def decidir(propuesta, accion, costo_acumulado_usd, ids_procesados,
            *, techo_costo_usd=0.50):
    # 1) Idempotencia PRIMERO (7.2): ya actuamos sobre este input -> no repetir
    if propuesta["input_id"] in ids_procesados:
        return {"ruta": "DUPLICADO", "motivo": "input_ya_procesado"}

    # 2) Guardrail de I/O (OWASP LLM05): jamás actuar sobre salida no validada
    if not propuesta["valido"]:
        return {"ruta": "RECHAZO", "motivo": "schema_o_reglas_invalidas"}

    # 3) Techo de costo: circuit-breaker contra runaways (Unbounded Consumption)
    if costo_acumulado_usd > techo_costo_usd:
        return {"ruta": "RECHAZO", "motivo": "techo_costo"}

    # 4) Acción sensible -> SIEMPRE humano, sin importar la confianza (OWASP LLM06)
    if accion["sensible"]:
        return {"ruta": "HITL", "motivo": "accion_sensible"}

    # 5) Confianza bajo el umbral de esa acción -> humano; en otro caso -> auto
    if propuesta["confianza"] < accion["umbral_confianza"]:
        return {"ruta": "HITL", "motivo": "confianza_baja"}
    return {"ruta": "AUTO", "motivo": "ok"}
```

## Razonamiento paso a paso

1. **Cadena de `if` con `return` temprano.** Cada barrera retorna apenas aplica; la **primera** que se cumple decide la ruta. El orden ES el diseño de seguridad.
2. **Idempotencia primero** (la más barata y crítica): si el input ya se procesó, nada más importa — saltárselo significa cobrar/actuar dos veces (problema at-least-once de la 7.2).
3. **Guardrail de I/O segundo** (LLM05): si la salida del LLM no validó (`valido=False`), se rechaza antes de cualquier decisión de negocio. Validar no es opcional.
4. **Techo de costo tercero**: barrera de sistema (circuit-breaker), antes que las barreras de caso. Frena un loop que quema dinero.
5. **Acción sensible cuarto** (LLM06): siempre a HITL, **sin importar la confianza**. La confianza auto-reportada no está calibrada (no es probabilidad), así que no puede ser la puerta a una acción irreversible.
6. **Confianza al final**, solo para acciones no sensibles: `confianza < umbral` → HITL; en otro caso → AUTO. La frontera `confianza == umbral` es AUTO (no está por debajo).

## Puntos resbalosos (donde el corrector debe mirar)

1. **Confianza puesta como primer chequeo** (el agujero del 6.2 MODIFY): cortocircuita idempotencia, schema, costo y la regla de acción sensible. Es el error de seguridad más grave; rompe `test_accion_sensible_siempre_hitl_aunque_confianza_alta` y los tests de orden.
2. **Orden invertido idempotencia/schema**: `test_orden_duplicado_gana_sobre_schema_invalido` lo caza — un duplicado con schema inválido debe ser `DUPLICADO`.
3. **`techo_costo_usd` ignorado**: `test_rechazo_por_techo_de_costo` falla. El parámetro debe usarse.
4. **`>` vs `>=` en el techo y en la confianza**: el techo rechaza con `costo > techo` (estrictamente mayor); la confianza es HITL con `confianza < umbral` (estrictamente menor). `test_confianza_justo_en_el_umbral_es_auto` fija la frontera de la confianza en AUTO.
5. **Combinar barreras en un solo `if ... and ...`**: pierde el `motivo` específico; el corrector debe verificar que cada motivo identifique la barrera correcta.

## Rango de soluciones aceptables

- Los strings de `motivo` pueden variar (el test no fija su texto exacto, salvo que `techo_costo` aparezca como motivo del rechazo por costo y que el motivo de HITL por confianza **no** sea `accion_sensible`). Lo que importa es que el `motivo` distinga las barreras.
- Usar constantes/enum para las rutas en vez de strings es válido si los valores devueltos siguen siendo `"AUTO"/"HITL"/"RECHAZO"/"DUPLICADO"`.
- Mandar el exceso de costo a `HITL` (frenar y que un humano decida si seguir gastando) en vez de `RECHAZO` es una decisión defendible en producción, **pero** rompe `test_rechazo_por_techo_de_costo`; para este ejercicio el contrato pide `RECHAZO`. Si el alumno lo cambió a HITL y lo justifica bien en el write-up, es señal de comprensión madura — anótalo, pero el contrato del ejercicio es RECHAZO.

## Vara para el `write-up.md`

- **(a)** Aceptable: una acción sensible va a HITL siempre porque la confianza auto-reportada no está calibrada (no es probabilidad) y porque darle al agente autonomía sobre lo irreversible es **Excessive Agency (LLM06)**. Excelente si nombra que el daño de un solo error (o de una prompt injection) en una acción irreversible no se puede deshacer, así que el costo asimétrico justifica el humano.
- **(b)** Aceptable: idempotencia primero porque si ya actuamos, todo lo demás es irrelevante (y validar el schema de un duplicado es trabajo desperdiciado). Incompleto si no conecta con at-least-once de la 7.2.
- **(c)** Aceptable: el schema garantiza la **forma** (tipos, enums), no la **verdad** (que el monto/categoría sean correctos). Ejemplo: `{"categoria": "reembolso", "monto_clp": 999999999}` valida contra el schema y es absurdo. Excelente: el guardrail de schema es la primera barrera, no la única — encima van reglas de negocio + verificación + HITL (defensa en profundidad).
