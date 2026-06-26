#!/usr/bin/env bash
#
# resolver.sh — Primero-Sin-IA.
#
# Contrato:
#   entrada: la ruta de un log web por argumento ($1). La IP es la primera columna.
#   salida:  las 3 IPs con MÁS peticiones, una por línea, en formato "CONTEO IP",
#            de mayor a menor. Solo el dato útil va a stdout.
#   errores: sin argumento -> mensaje de uso a stderr y código de salida != 0.
#
# Implementa el pipeline a mano, sin IA. NO cambies el nombre del archivo:
# los tests de tests/test_resolver.py invocan `bash resolver.sh <log>`.

set -euo pipefail

# TODO(estudiante): reemplaza estas dos líneas por tu solución.
echo "Sin implementar: completa resolver.sh (ver README.md)" >&2
exit 2
