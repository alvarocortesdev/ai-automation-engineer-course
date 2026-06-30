from app import normaliza_email


def test_normaliza_quita_espacios_y_baja_a_minusculas():
    assert normaliza_email("  Ada@Example.COM ") == "ada@example.com"


def test_normaliza_ya_normalizado_no_cambia():
    assert normaliza_email("a@b.cl") == "a@b.cl"
