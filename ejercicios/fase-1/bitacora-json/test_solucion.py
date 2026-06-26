"""Tests del ejercicio — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Usamos el fixture `tmp_path` de pytest: una carpeta temporal por test, así no
ensuciamos el repo ni dependemos de archivos previos. Cada test es independiente.
"""

import json

import pytest

from solucion import BitacoraCorrupta, agregar, cargar, resumen


def test_cargar_archivo_inexistente_devuelve_lista_vacia(tmp_path):
    ruta = tmp_path / "no_existe.json"
    assert cargar(ruta) == []


def test_agregar_y_recargar_round_trip(tmp_path):
    ruta = tmp_path / "bitacora.json"
    agregar(ruta, "hola")
    agregar(ruta, "chao")
    assert cargar(ruta) == [{"mensaje": "hola"}, {"mensaje": "chao"}]


def test_round_trip_preserva_acentos_y_enie(tmp_path):
    ruta = tmp_path / "bitacora.json"
    agregar(ruta, "el ñandú comió pan")
    registros = cargar(ruta)
    assert registros == [{"mensaje": "el ñandú comió pan"}]
    # El archivo en disco debe tener los caracteres legibles, no escapes \uXXXX.
    crudo = ruta.read_text(encoding="utf-8")
    assert "ñandú" in crudo


def test_cargar_json_corrupto_lanza_bitacora_corrupta(tmp_path):
    ruta = tmp_path / "rota.json"
    ruta.write_text("{esto no es json", encoding="utf-8")
    with pytest.raises(BitacoraCorrupta):
        cargar(ruta)


def test_cargar_json_valido_existente(tmp_path):
    ruta = tmp_path / "bitacora.json"
    ruta.write_text(json.dumps([{"mensaje": "x"}]), encoding="utf-8")
    assert cargar(ruta) == [{"mensaje": "x"}]


def test_resumen_cuenta_registros():
    assert resumen([]) == {"total": 0}
    assert resumen([{"mensaje": "a"}, {"mensaje": "b"}]) == {"total": 2}


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Idea: ¿qué pasa si agregas un mensaje vacío ""? ¿Y si agregas muchos seguidos?
# def test_mi_caso_borde(tmp_path):
#     ...
