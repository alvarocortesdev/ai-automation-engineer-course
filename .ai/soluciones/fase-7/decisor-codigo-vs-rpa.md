---
ejercicio_id: fase-7/decisor-codigo-vs-rpa
fase: fase-7
sub_unidad: "7.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Decisor: ¿código, navegador o RPA?

## Respuesta canónica

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Caso:
    tiene_api: bool
    es_web: bool
    volumen_alto: bool
    critico: bool
    ui_cambia_seguido: bool


@dataclass(frozen=True)
class Recomendacion:
    estrategia: str
    motivo: str


def recomendar_automatizacion(caso: Caso) -> Recomendacion:
    # Escalón 1: si hay API, gana SIEMPRE (más estable, testeable, barata de mantener).
    if caso.tiene_api:
        return Recomendacion(
            "api",
            "Existe API/webhook: integra por el contrato (httpx/SDK). Estable, "
            "testeable e idempotente; es el escalón más alto de la escalera.",
        )
    # Sin API: toca automatizar una UI, que es frágil por naturaleza.
    # Escalón 0: si el proceso es crítico o de alto volumen, la UI-automation no es base.
    if caso.critico or caso.volumen_alto:
        return Recomendacion(
            "rediseñar-proceso",
            "Sin API y el proceso es crítico o de alto volumen: automatizar la UI es "
            "demasiado frágil/lento como base. Presiona por una API o un export/ETL; "
            "la UI-automation solo como puente temporal.",
        )
    # Escalón 2: web sin API y de bajo riesgo -> navegador con selectores semánticos.
    if caso.es_web:
        nota = (
            " La UI cambia seguido: presupuesta mantención y monitorea selectores."
            if caso.ui_cambia_seguido
            else ""
        )
        return Recomendacion(
            "navegador",
            "Sin API pero es web: navegador headless con selectores semánticos y "
            "esperas web-first; nada de coordenadas ni sleeps fijos." + nota,
        )
    # Escalón 3: ni API ni web -> RPA de UI como ÚLTIMO recurso.
    return Recomendacion(
        "rpa-ui",
        "Sin API y no es web (app de escritorio legacy): RPA de UI como último "
        "recurso, aislada, idempotente y observable, con la menor superficie posible.",
    )
```

## Razonamiento paso a paso

1. **El orden de los `if` ES la escalera.** Se devuelve apenas se encuentra el escalón más alto
   aplicable. Por eso `tiene_api` va primero: domina cualquier otra combinación de flags.
2. **El caso resbaloso va ANTES de elegir web vs escritorio.** Una vez descartada la API, estamos
   obligados a automatizar una UI (frágil). Si el proceso es `critico` o de `volumen_alto`, esa
   fragilidad no es aceptable como base → `rediseñar-proceso` (subir el problema). Solo si el riesgo
   es bajo elegimos navegador (web) o rpa-ui (escritorio).
3. **`ui_cambia_seguido` no cambia la estrategia, matiza el motivo.** Es una señal de costo de
   mantención, no de cambio de escalón. Modelarlo en el `motivo` (advertencia) es lo correcto;
   modelarlo como un quinto destino sería sobre-ingeniería.
4. **Función pura.** Sin I/O, sin estado: mismo `Caso` → misma `Recomendacion`. Eso la hace trivial
   de testear y de razonar.

## Puntos resbalosos / variantes

- **Orden invertido (bug típico):** chequear `es_web` antes que `tiene_api` haría que un sistema con
  API pero también web caiga en "navegador". La API debe ganar.
- **Olvidar el escalón 0:** recomendar `rpa-ui`/`navegador` para algo crítico sin API es el error
  conceptual que la lección combate.
- **Tratar `ui_cambia_seguido` como destino propio** (p. ej. "navegador-frágil"): aceptable si el
  alumno lo justifica y mantiene los 4 destinos del contrato, pero innecesario. No penalizar si los
  tests dados siguen pasando y la lógica es defendible.

## Rango de soluciones aceptables

- Cualquier implementación que pase los 12 tests y mantenga la **prioridad de la escalera** (API
  arriba; rediseñar antes que UI-automation en casos críticos/alto volumen) es **competente**.
- Redacciones distintas del `motivo` son válidas mientras nombren la **restricción dominante** (no
  basta repetir la estrategia).
- Variantes con un diccionario de reglas o tabla de decisión son aceptables si el alumno **puede
  explicarlas** y son legibles; para este tamaño, la cadena de `if` es lo más claro. **Excelente** =
  pura + legible + un test propio con un borde real (p. ej. `tiene_api=True` con todo lo demás en
  `True` sigue dando `api`).
