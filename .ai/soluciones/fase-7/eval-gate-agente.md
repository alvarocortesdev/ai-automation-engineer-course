---
ejercicio_id: fase-7/eval-gate-agente
fase: fase-7
sub_unidad: "7.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — El eval gate de un agente

## Respuesta canónica

```python
def evaluar(predicciones, esperado):
    n = len(predicciones)
    if n == 0:
        # verdad vacua: sin items, nada falló
        return {"accuracy_categoria": 1.0, "exactitud_campos": 1.0, "n": 0}

    cat_ok = 0
    campos_ok = 0
    campos_tot = 0
    _CENTINELA = object()
    for p in predicciones:
        e = esperado[p["input_id"]]
        if p["categoria"] == e["categoria"]:
            cat_ok += 1
        for clave, valor in e["campos"].items():
            campos_tot += 1
            if p["campos"].get(clave, _CENTINELA) == valor:   # clave faltante != acierto
                campos_ok += 1

    exactitud = 1.0 if campos_tot == 0 else campos_ok / campos_tot
    return {"accuracy_categoria": cat_ok / n, "exactitud_campos": exactitud, "n": n}


def gate(metricas, *, umbral_categoria=0.90, baseline=None):
    acc = metricas["accuracy_categoria"]
    if acc < umbral_categoria:
        return {"pasa": False, "motivo": f"bajo_umbral: {acc} < {umbral_categoria}"}
    if baseline is not None and acc < baseline["accuracy_categoria"]:
        return {"pasa": False,
                "motivo": f"regresion vs baseline: {acc} < {baseline['accuracy_categoria']}"}
    return {"pasa": True, "motivo": "ok"}
```

## Razonamiento paso a paso

1. **Lista vacía primero** (verdad vacua): sin items que evaluar, no hay errores → 1.0/1.0/0. Evita la división por cero y es la convención más defendible (un eval sin casos no debería *bloquear* un deploy por sí mismo).
2. **Accuracy de categoría** = aciertos / `n`. Métrica de routing/clasificación — la que importa para una automatización.
3. **Exactitud de campos GLOBAL**: numerador = total de pares (clave, valor) esperados que coinciden exactamente, sumando todos los inputs; denominador = total de campos esperados. **No** es un promedio de ratios por ítem (eso da números distintos en casos desbalanceados).
4. **Clave faltante ≠ acierto**: usar un centinela en `.get` evita que un `None` predicho coincida con un `None` esperado por accidente, y que una clave ausente cuente como correcta.
5. **`gate` separa dos chequeos** con motivos distintos: bajo umbral, y regresión (solo si hay `baseline`). La frontera `acc == umbral` **pasa** (no está por debajo). La regresión bloquea cuando `acc < baseline` (estrictamente menor): igualar o mejorar el baseline pasa.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Exactitud como promedio de promedios** (promediar el ratio de cada ítem) en vez de fracción global: rompe `test_evaluar_caso_mixto` (espera 0.75 = 3/4 global, no el promedio de 1.0, 0.0, 1.0 = 0.667).
2. **División por cero en lista vacía**: `test_evaluar_lista_vacia_no_revienta` lo caza.
3. **Gate que aplica regresión con `baseline=None`**: rompe `test_gate_pasa_sobre_umbral_sin_baseline`.
4. **Frontera mal**: tratar `acc == umbral` como bloqueo rompe `test_gate_frontera_igual_al_umbral_pasa`.
5. **Motivo que no distingue umbral de regresión**: los tests buscan `"umbral"` en un caso y `"regres"` en otro; un motivo genérico falla.
6. **Regresión con `>` en vez de `<`**: bloquear cuando `acc > baseline` invierte la lógica; debe bloquear cuando es estrictamente menor.

## Rango de soluciones aceptables

- La convención de lista vacía puede ser 0.0/0.0 **si** el alumno la justifica como "fail-safe" (mejor bloquear ante un eval vacío). **Pero** el contrato y los tests fijan 1.0/1.0; si el alumno eligió 0.0 los tests fallan. Anótalo como decisión defendible y pídele alinear con el contrato.
- `exactitud_campos` puede excluir inputs sin campos esperados del denominador (ya lo hace al sumar 0); la convención `campos_tot == 0 → 1.0` solo aplica cuando NINGÚN input tiene campos esperados.
- Devolver métricas extra (p. ej. matriz de confusión por categoría) es señal de `excelente`, no un requisito.
- Reportar ambos motivos cuando falla por umbral **y** regresión es válido y deseable.

## Vara para el `write-up.md`

- **(a)** Aceptable: para una automatización lo que importa es la tasa de **acción/decisión correcta** (routing, extracción), porque el agente *actúa* — una respuesta fluida pero mal ruteada ejecuta la acción equivocada. La fluidez es métrica de chatbot, no de agente de acción.
- **(b)** Aceptable: un umbral fijo no detecta que ayer estabas en 0.95 y hoy en 0.92 — ambos "pasan" el 0.90, pero es una **regresión** que debería bloquear y disparar investigación. Escenario válido: 0.92 ≥ 0.90 (umbral) pero 0.92 < 0.95 (baseline) → bloquea por regresión. Excelente si nota que sin gate de regresión, las mejoras de prompt pueden esconder degradaciones silenciosas.
- **(c)** Aceptable: el golden set sale de **trazas de producción** anotadas (casos reales que el agente vio), no de ejemplos inventados (6.9). El eval offline es un gate fijo en CI; el monitoreo online detecta **deriva** y casos nuevos que el golden set no contiene — se necesitan ambos. Excelente: el golden set debe versionarse y crecer con los fallos que aparecen en prod (datasets desde trazas).
- **(d)** Aceptable: 1.0 (verdad vacua) porque un eval sin casos no encontró errores y no debería ser la razón para bloquear; 0.0 sería más seguro si "lista vacía" indica un **bug en el harness** (no cargó los casos) y prefieres fallar cerrado. Excelente si distingue "no hay casos por diseño" de "no hay casos por error".
