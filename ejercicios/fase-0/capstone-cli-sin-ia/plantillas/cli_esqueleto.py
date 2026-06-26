#!/usr/bin/env python3
"""<mi-cli> — <una frase: qué hace tu herramienta>.

Esqueleto de arranque para el Capstone F0. Reemplaza los TODO con TU lógica.

NO es una solución: es solo la ceremonia de `argparse` + exit codes para que no
pierdas tiempo en el andamiaje. El diseño, la estructura y la lógica los piensas
tú —sin IA—, guiándote por tu `SPEC.md`. Una función por verbo; una rama por caso
borde.
"""
import argparse
import sys

# Convención de exit codes (ajústala en tu SPEC.md si tu caso lo pide).
EXIT_OK = 0      # éxito
EXIT_ERROR = 1   # error durante la ejecución (p. ej.: destino ocupado, archivo corrupto)
EXIT_USO = 2     # uso incorrecto (argumento faltante / inválido)


def cmd_ejemplo(args: argparse.Namespace) -> int:
    """TODO: implementa tu comando real. Devuelve un exit code honesto."""
    # El dato útil va a stdout (componible con pipes):
    print(f"(esqueleto) recibiste: {args.valor}")
    # Los diagnósticos y errores van a stderr, por ejemplo:
    #   print("error: la entrada es inválida", file=sys.stderr)
    #   return EXIT_USO
    return EXIT_OK


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mi-cli",
        description="TODO: describe tu herramienta en una línea.",
    )
    # `required=True` hace que llamar sin sub-comando falle con exit 2 (uso incorrecto).
    sub = parser.add_subparsers(dest="comando", required=True)

    # TODO: un sub-parser por cada verbo de tu SPEC.md.
    p = sub.add_parser("ejemplo", help="TODO: reemplaza por tu comando real")
    p.add_argument("valor", help="TODO: argumento de ejemplo")
    p.set_defaults(func=cmd_ejemplo)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    # Cada sub-comando registró su handler con set_defaults(func=...).
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
