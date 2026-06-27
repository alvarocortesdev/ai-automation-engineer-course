#!/usr/bin/env bash
#
# deploy.sh — despliega el contenedor de tu API en Azure Container Apps (de forma SEGURA).
#
# Completa los pasos marcados con TODO. Recuerda (lección 5.5, sección 4.7):
#   - ingress público + puerto correcto (para que sea alcanzable)
#   - identidad administrada para el pull (sin admin user, sin password de registry)
#   - mínimo privilegio: SOLO el rol de pull de imágenes SOBRE el registry (nunca Contributor/Owner)
#
# Los tests (test_deploy.py) revisan este archivo como TEXTO: no necesitas una cuenta de Azure
# para que pasen. Si tienes créditos gratis, puedes correrlo de verdad (requiere `az login`).
# Corre `pytest` y deja que las verificaciones en rojo te guíen: cada una apunta a un paso.

set -euo pipefail

# --- Configuración (12-factor: nada secreto hardcodeado; valores por variable de entorno) ---
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-api-produccion}"
LOCATION="${LOCATION:-brazilsouth}"
ENVIRONMENT="${ENVIRONMENT:-env-api-produccion}"
APP_NAME="${APP_NAME:-api-produccion}"
ACR_NAME="${ACR_NAME:?define ACR_NAME (nombre único global de tu Azure Container Registry)}"
IMAGE_TAG="${IMAGE_TAG:-api-produccion:latest}"
IDENTITY="${IDENTITY:-id-api-produccion}"
TARGET_PORT="${TARGET_PORT:-8000}"   # debe COINCIDIR con el puerto que escucha tu FastAPI (5.1)

# 0. Extensión de Container Apps y providers que usa
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# 1. TODO: crea el grupo de recursos (la "carpeta" que agrupa todo). Necesita un nombre y --location.

# 2. TODO: crea el Container Registry (sku Basic) y construye la imagen EN la nube
#    (build de ACR, termina con el "." del contexto). Sin Docker local.

# 3. TODO: crea la identidad administrada de usuario y captura, con `--query ... -o tsv`:
#      - su id          -> IDENTITY_ID
#      - su principalId  -> PRINCIPAL
#      - el id del registry (consulta el registry) -> ACR_ID

# 4. TODO: mínimo privilegio. Asigna a esa identidad SOLO el rol de pull de imágenes
#    (el que empieza con "acr"), con --scope el registry. NO uses Contributor/Owner.

# 5. TODO: crea el entorno de Container Apps (trae Log Analytics para observabilidad, 5.10).

# 6. TODO: crea y despliega la app. Debe quedar PÚBLICA, en el puerto correcto, y hacer el pull
#    CON la identidad administrada (sin password). Imprime el FQDN al final.
