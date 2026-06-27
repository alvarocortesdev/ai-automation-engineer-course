"""Linter estático del Dockerfile — NO necesita Docker instalado.

Lee tu `Dockerfile` y tu `.dockerignore` y verifica las buenas prácticas de la
lección 5.1. Es un PISO, no la meta: un linter no entiende si tu razonamiento es
correcto, solo si los patrones están. Tu `notas.md` y el corrector hacen el resto.

Ejecuta:
    uv run pytest test_dockerfile.py     # recomendado
    pytest test_dockerfile.py            # si ya tienes pytest

Mientras el Dockerfile esté vacío, estos tests fallan (rojo). Eso es lo esperado:
impleméntalo a mano hasta ponerlos en verde.
"""

import re
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
DOCKERFILE = AQUI / "Dockerfile"
DOCKERIGNORE = AQUI / ".dockerignore"

MANIFIESTOS = ("requirements", "pyproject", "poetry.lock", "uv.lock", "pipfile")


def _instrucciones() -> list[tuple[str, str]]:
    """Devuelve [(INSTRUCCION, resto)] del Dockerfile, sin comentarios ni vacías.

    Une las continuaciones de línea (las que terminan en '\\').
    """
    assert DOCKERFILE.exists(), "Falta el archivo Dockerfile."
    crudas: list[str] = []
    buffer = ""
    for linea in DOCKERFILE.read_text(encoding="utf-8").splitlines():
        sin_pad = linea.strip()
        if not sin_pad or sin_pad.startswith("#"):
            continue
        if sin_pad.endswith("\\"):
            buffer += sin_pad[:-1] + " "
            continue
        buffer += sin_pad
        crudas.append(buffer)
        buffer = ""
    if buffer:
        crudas.append(buffer)

    instrucciones = []
    for linea in crudas:
        partes = linea.split(None, 1)
        instr = partes[0].upper()
        resto = partes[1] if len(partes) > 1 else ""
        instrucciones.append((instr, resto))
    return instrucciones


def _froms(instrucciones) -> list[str]:
    return [resto for instr, resto in instrucciones if instr == "FROM"]


def test_dockerfile_no_esta_vacio():
    instr = _instrucciones()
    assert instr, "El Dockerfile no tiene instrucciones todavía. Escríbelo a mano."


def test_es_multistage():
    instr = _instrucciones()
    froms = _froms(instr)
    assert len(froms) >= 2, (
        "Un Dockerfile multi-stage tiene al menos 2 instrucciones FROM "
        "(builder + runtime). Encontré %d." % len(froms)
    )
    tiene_alias = any(re.search(r"\bAS\s+\w+", f, re.IGNORECASE) for f in froms)
    assert tiene_alias, "Nombra al menos una etapa con 'AS', p. ej. 'FROM ... AS builder'."
    copia_desde_etapa = any(
        instr_ == "COPY" and "--from=" in resto for instr_, resto in instr
    )
    assert copia_desde_etapa, (
        "Falta un 'COPY --from=<etapa> ...': el runtime debe copiar lo construido "
        "en el builder. Sin eso no es realmente multi-stage."
    )


def test_base_pinneada_y_sin_latest():
    instr = _instrucciones()
    alias = set()
    for f in _froms(instr):
        tokens = f.split()
        imagen = tokens[0]
        # registra el alias de esta etapa para no exigirle tag a un FROM <etapa>
        m = re.search(r"\bAS\s+(\w+)", f, re.IGNORECASE)
        if imagen in alias:
            # FROM que referencia una etapa previa: no necesita tag
            if m:
                alias.add(m.group(1))
            continue
        assert ":" in imagen or "@sha256" in imagen, (
            f"La imagen base '{imagen}' no tiene tag. Fíjala (p. ej. python:3.13-slim)."
        )
        assert not imagen.endswith(":latest"), (
            f"'{imagen}' usa ':latest', que no es reproducible. Fija una versión."
        )
        if m:
            alias.add(m.group(1))


def test_corre_como_no_root():
    instr = _instrucciones()
    users = [resto.strip() for i, resto in instr if i == "USER"]
    assert users, (
        "Falta una instrucción USER: por defecto el contenedor corre como root. "
        "Crea un usuario de sistema y cambia a él antes del CMD."
    )
    ultimo = users[-1].split(":")[0].lower()
    assert ultimo not in ("root", "0"), (
        f"El último USER es '{users[-1]}'. Debe ser un usuario sin privilegios, no root."
    )


def test_tiene_healthcheck():
    instr = _instrucciones()
    assert any(i == "HEALTHCHECK" for i, _ in instr), (
        "Falta HEALTHCHECK. Agrega uno que golpee /health sin depender de curl."
    )


def test_healthcheck_no_usa_curl():
    instr = _instrucciones()
    for i, resto in instr:
        if i == "HEALTHCHECK":
            assert "curl" not in resto.lower(), (
                "La imagen slim no trae curl. Usa python -c con urllib (o wget si lo instalas) "
                "para el healthcheck."
            )


def test_orden_de_capas_aprovecha_cache():
    instr = _instrucciones()
    manifiesto_idxs: list[int] = []
    install_idxs: list[int] = []
    app_idxs: list[int] = []
    for n, (i, resto) in enumerate(instr):
        low = resto.lower()
        es_manifiesto = any(m in low for m in MANIFIESTOS)
        if i in ("COPY", "ADD") and "--from=" not in resto and es_manifiesto:
            manifiesto_idxs.append(n)
        # instalación de DEPENDENCIAS (no el bootstrap de la herramienta como 'pip install uv'):
        # debe referenciar el manifiesto, usar '-r', o ser un sync/install de lockfile.
        if i == "RUN" and any(k in low for k in ("pip install", "uv pip", "uv sync", "poetry install", "pip3 install")):
            if es_manifiesto or " -r" in (" " + low) or "uv sync" in low or "poetry install" in low:
                install_idxs.append(n)
        if i == "COPY" and "--from=" not in resto and not es_manifiesto:
            # copia del código de la app (./app, ., src, ...) — no el manifiesto, no --from
            if ("/app" in low) or (" app" in (" " + low)) or low.strip().startswith(".") or " src" in (" " + low):
                app_idxs.append(n)

    assert manifiesto_idxs, (
        "No veo que copies el manifiesto de dependencias (requirements.txt) por separado. "
        "Cópialo ANTES de instalar, para que un cambio de código no invalide la instalación. "
        "Un 'COPY . .' antes del install rompe la caché."
    )
    assert install_idxs, "No veo un RUN que instale las dependencias del manifiesto (pip/uv -r requirements.txt)."
    assert app_idxs, "No veo que copies el código de la app (p. ej. COPY ./app ./app)."

    idx_manifiesto = min(manifiesto_idxs)
    idx_app = min(app_idxs)
    assert idx_manifiesto < idx_app, (
        "Copias el código de la app antes que el manifiesto de dependencias: el orden está invertido."
    )
    assert any(idx_manifiesto < i < idx_app for i in install_idxs), (
        "Orden incorrecto. Debe ser: copiar requirements -> instalar deps -> copiar el código. "
        "La instalación de dependencias tiene que ocurrir ENTRE el COPY del manifiesto y el COPY del código, "
        "o cada cambio de código invalida la caché de dependencias."
    )


def test_no_hornea_secretos():
    """Ningún ENV/ARG con un secreto literal (debe entrar en runtime, no en build)."""
    instr = _instrucciones()
    patron = re.compile(
        r"(password|passwd|secret|token|api[_-]?key)\s*=\s*[\"']?[^\s\"'$]{3,}",
        re.IGNORECASE,
    )
    for i, resto in instr:
        if i in ("ENV", "ARG"):
            m = patron.search(resto)
            # permitido si el valor referencia una variable (${...}) en vez de un literal
            assert not m, (
                f"Posible secreto horneado en la imagen: '{i} {resto}'. "
                "Los secretos entran en runtime (variable de entorno), nunca en el Dockerfile."
            )


def test_tiene_cmd_o_entrypoint():
    instr = _instrucciones()
    assert any(i in ("CMD", "ENTRYPOINT") for i, _ in instr), (
        "Falta CMD o ENTRYPOINT: la imagen no sabría qué proceso arrancar."
    )


def test_dockerignore_excluye_lo_critico():
    assert DOCKERIGNORE.exists(), "Falta el archivo .dockerignore."
    texto = DOCKERIGNORE.read_text(encoding="utf-8")
    lineas = {l.strip() for l in texto.splitlines() if l.strip() and not l.strip().startswith("#")}
    contenido = " ".join(lineas).lower()
    assert lineas, ".dockerignore está vacío. Lista lo que NO debe entrar a la imagen."
    assert ".env" in contenido, "El .dockerignore DEBE excluir .env (nunca hornees secretos)."
    assert ".git" in contenido, "El .dockerignore debería excluir .git."
    assert "__pycache__" in contenido or "*.pyc" in contenido, (
        "El .dockerignore debería excluir __pycache__ / *.pyc."
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
