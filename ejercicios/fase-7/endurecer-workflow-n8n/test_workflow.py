"""Test ESTRUCTURAL de tu workflow de n8n endurecido.

No corre tu flujo en una instancia de n8n (no hace falta): parsea el JSON que
editaste en `workflow.json` y verifica que tenga la FORMA confiable que pide la
lección 7.1. Es tu "spec" del workflow — léelo: cada assert te dice exactamente
qué propiedad se espera y por qué.

Solo usa la librería estándar (json). Correr:
    uv run pytest test_workflow.py        # recomendado
    pytest test_workflow.py               # si ya tienes pytest
"""

import json
from pathlib import Path

WORKFLOW = Path(__file__).parent / "workflow.json"

# Nombre del nodo con el efecto secundario peligroso (crear la factura).
NODO_EFECTO = "Crear factura"


def cargar():
    assert WORKFLOW.exists(), f"No encuentro {WORKFLOW}."
    data = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "El JSON no es un objeto en el nivel superior."
    assert isinstance(data.get("nodes"), list) and data["nodes"], (
        "Falta la lista 'nodes'."
    )
    assert isinstance(data.get("connections"), dict), "Falta el objeto 'connections'."
    return data


def nodo_por_tipo(data, sufijo):
    """Devuelve el primer nodo cuyo 'type' termina en `sufijo` (case-insensitive)."""
    for n in data["nodes"]:
        tipo = (n.get("type") or "").lower()
        if tipo.endswith(sufijo.lower()):
            return n
    return None


def nodo_por_nombre(data, nombre):
    for n in data["nodes"]:
        if n.get("name") == nombre:
            return n
    return None


def primer_destino(data, nombre_origen):
    """Nombre del primer nodo destino de la primera salida 'main' de `nombre_origen`."""
    conexiones = data["connections"].get(nombre_origen)
    assert conexiones and conexiones.get("main"), (
        f"El nodo '{nombre_origen}' no tiene conexiones de salida 'main'."
    )
    salidas = conexiones["main"]
    assert salidas and salidas[0], f"'{nombre_origen}' no conecta con ningún nodo."
    return salidas[0][0]["node"]


def test_existe_nodo_dedup():
    data = cargar()
    dedup = nodo_por_tipo(data, "removeDuplicates")
    assert dedup is not None, (
        "Falta un nodo de tipo 'n8n-nodes-base.removeDuplicates' (la barrera de "
        "idempotencia). Insértalo entre el Webhook y 'Crear factura'."
    )


def test_webhook_conecta_primero_al_dedup():
    data = cargar()
    webhook = nodo_por_tipo(data, "webhook")
    dedup = nodo_por_tipo(data, "removeDuplicates")
    assert webhook and dedup, "Necesitas un Webhook y un nodo Remove Duplicates."
    destino = primer_destino(data, webhook["name"])
    assert destino == dedup["name"], (
        f"El Webhook conecta primero con '{destino}', pero la barrera de "
        "idempotencia debe ir ANTES del efecto secundario: el Webhook tiene que "
        f"fluir primero al nodo de dedup ('{dedup['name']}')."
    )


def test_dedup_conecta_al_efecto_secundario():
    data = cargar()
    dedup = nodo_por_tipo(data, "removeDuplicates")
    assert dedup is not None, "Falta el nodo Remove Duplicates."
    destino = primer_destino(data, dedup["name"])
    assert destino == NODO_EFECTO, (
        f"El dedup conecta con '{destino}', pero debe fluir hacia '{NODO_EFECTO}' "
        "(el nodo con el efecto secundario que la barrera protege)."
    )


def test_reintentos_en_efecto_secundario():
    data = cargar()
    nodo = nodo_por_nombre(data, NODO_EFECTO)
    assert nodo is not None, f"No encuentro el nodo '{NODO_EFECTO}'."
    assert nodo.get("retryOnFail") is True, (
        f"'{NODO_EFECTO}' debe tener 'retryOnFail': true (tolerar fallos transitorios)."
    )
    max_tries = nodo.get("maxTries")
    assert isinstance(max_tries, int) and 2 <= max_tries <= 5, (
        "'maxTries' debe ser un entero entre 2 y 5 (rango sano de reintentos)."
    )
    wait = nodo.get("waitBetweenTries")
    assert isinstance(wait, int) and wait > 0, (
        "'waitBetweenTries' debe ser mayor que 0 ms: reintentar sin espera "
        "martilla la API que justo está sobrecargada."
    )


def test_error_workflow_asociado():
    data = cargar()
    settings = data.get("settings")
    assert isinstance(settings, dict), "Falta el objeto 'settings'."
    ew = settings.get("errorWorkflow")
    assert isinstance(ew, str) and ew.strip(), (
        "Declara 'settings.errorWorkflow' con un id no vacío: sin error workflow, "
        "un fallo real muere en silencio."
    )
