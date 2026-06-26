#!/usr/bin/env bash
#
# backup.sh — Primero-Sin-IA.
#
# Contrato:
#   uso:     backup.sh <directorio>
#   éxito:   crea un .tar.gz con el CONTENIDO de <directorio>, nombrado con timestamp,
#            dentro de "$BACKUP_DIR" (por defecto "."), y escribe SOLO su ruta a stdout.
#   errores: sin argumento -> uso a stderr y exit 1.
#            directorio inexistente -> error a stderr y exit 1.
#   regla:   diagnósticos/mensajes informativos van a stderr (>&2), no a stdout.
#
# Implementa a mano, sin IA. NO cambies el nombre del archivo: los tests
# (tests/test_backup.py) invocan `bash backup.sh ...`.

set -euo pipefail

# TODO(estudiante): reemplaza estas dos líneas por tu solución.
echo "Sin implementar: completa backup.sh (ver README.md)" >&2
exit 2
