"""Eval gate de un agente de automatización — Primero-Sin-IA.

Implementa `evaluar` y `gate` a mano, sin IA. NO cambies las firmas ni las claves
de los dicts que devuelves: `test_eval_gate.py` depende de ellas.

Idea: cambiaste el prompt o el modelo de tu agente. ¿Mejoró o empeoró? Para una
AUTOMATIZACIÓN la métrica que importa es la DECISIÓN correcta (¿categoriza y
extrae como el humano experto?), no la fluidez del texto. Mides contra un GOLDEN
SET y BLOQUEAS el deploy si cae bajo un umbral o si hay REGRESIÓN vs el baseline.
Esto corre en CI como los tests. Sin red: las predicciones y el golden set son
listas/dicts que tú controlas.

──────────────────────────────────────────────────────────────────────────────
CONTRATO

    evaluar(predicciones, esperado) -> dict
        predicciones: list[dict] con {"input_id", "categoria", "campos"}
                      (campos es un dict {clave: valor})
        esperado:     dict indexado por input_id -> {"categoria", "campos"}
        Devuelve:
            {
              "accuracy_categoria": float,  # fracción de inputs con categoria correcta
              "exactitud_campos":   float,  # del total de campos esperados (sumando
                                            # todos los inputs), fracción que coincide
                                            # exactamente (misma clave, mismo valor)
              "n": int,                     # cantidad de inputs evaluados
            }
        Lista vacía: NO debe dividir por cero. Convención fijada (verdad vacua):
        sin nada que evaluar, no hay errores -> accuracy_categoria = 1.0,
        exactitud_campos = 1.0, n = 0. En el write-up justificas por qué esta
        convención (y cuándo 0.0 sería más seguro).

    gate(metricas, *, umbral_categoria=0.90, baseline=None) -> dict
        metricas: el dict que devuelve evaluar()
        baseline: None, o un dict de métricas previas con "accuracy_categoria"
        Devuelve: {"pasa": bool, "motivo": str}
            pasa = True solo si:
                accuracy_categoria >= umbral_categoria
                Y (baseline is None  o  accuracy_categoria >= baseline["accuracy_categoria"])
        El "motivo" DEBE distinguir "bajo el umbral" de "regresión vs baseline".
"""


def evaluar(predicciones: list, esperado: dict) -> dict:
    """Calcula las métricas de decisión del agente. Ver el contrato arriba."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def gate(metricas: dict, *, umbral_categoria: float = 0.90, baseline: dict | None = None) -> dict:
    """Decide si el despliegue pasa o se bloquea. Ver el contrato arriba."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")
