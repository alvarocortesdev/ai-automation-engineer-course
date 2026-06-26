"""Ejercicio 1.9 — Excepciones de dominio en Python (Primero-Sin-IA).

Un parser de líneas de gastos con DOS niveles de manejo de error:

  - `parsear_linea`  → la UNIDAD: su contrato es "una línea válida o nada".
                       Ante una línea mala, LANZA `LineaInvalida` (excepción de dominio).
  - `parsear_archivo`→ el LOTE: su contrato es "procesa todo lo que puedas y repórtame
                       qué falló". NO se cae en la primera línea mala: junta los `Gasto`
                       válidos por un lado y los errores (como DATOS) por otro.

Formato de cada línea:  comercio;monto;categoria      (ej. "Lider;12990;supermercado")

Modos de fallo de una línea (esto es tu spec; los tests lo fijan):
    - campos != 3
    - monto no es entero
    - monto <= 0
    - comercio o categoria vacíos (tras strip)

Pistas de diseño (no la solución):
  - Define `LineaInvalida(Exception)` (subclase de Exception, NO de BaseException).
  - EAFP para el monto: `try: int(monto_raw) except ValueError as e: raise LineaInvalida(...) from e`.
  - El `from e` ENCADENA: conserva la causa original (exc.__cause__) para la stack trace.
  - En `parsear_archivo`, un try/except por línea que ACUMULA un ErrorLinea en vez de relanzar.

Corre los tests:  uv run pytest        (o:  pytest)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Gasto:
    comercio: str
    monto: int
    categoria: str


@dataclass(frozen=True)
class ErrorLinea:
    numero: int       # número de línea (1-based, contando las líneas en blanco)
    contenido: str    # la línea original tal cual
    motivo: str       # mensaje del error (str de la excepción)


class LineaInvalida(Exception):
    """La línea no respeta el formato 'comercio;monto;categoria'."""


def parsear_linea(linea: str) -> Gasto:
    """Convierte UNA línea en un Gasto, o LANZA `LineaInvalida` si está mal.

    Cuando el monto no es entero, encadena el ValueError original con `from e`.
    """
    # TODO(estudiante): implementa los 4 modos de fallo con `raise LineaInvalida(...)`.
    raise NotImplementedError("Implementa parsear_linea")


def parsear_archivo(texto: str) -> tuple[list[Gasto], list[ErrorLinea]]:
    """Procesa muchas líneas SIN caerse: separa válidos y errores.

    - Ignora las líneas en blanco (no cuentan como error, pero sí ocupan número).
    - Por cada línea mala, acumula un ErrorLinea(numero, contenido, motivo).
    - Devuelve (lista_de_gastos_validos, lista_de_errores).
    """
    # TODO(estudiante): usa enumerate(..., start=1) y un try/except LineaInvalida por línea.
    raise NotImplementedError("Implementa parsear_archivo")
