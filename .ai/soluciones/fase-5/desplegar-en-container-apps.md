---
ejercicio_id: fase-5/desplegar-en-container-apps
fase: fase-5
sub_unidad: "5.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es el `deploy.sh` de referencia:
> úsalo para detectar qué le falta y graduar pistas, **nunca** para entregárselo. Los nombres de
> recursos y la región son ilustrativos; lo que importa es el patrón de seguridad.

# Solución de referencia — `deploy.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Configuración (12-factor: nada secreto hardcodeado) ---
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-api-produccion}"
LOCATION="${LOCATION:-brazilsouth}"
ENVIRONMENT="${ENVIRONMENT:-env-api-produccion}"
APP_NAME="${APP_NAME:-api-produccion}"
ACR_NAME="${ACR_NAME:?define ACR_NAME (nombre único global del registry)}"
IMAGE_TAG="${IMAGE_TAG:-api-produccion:latest}"
IDENTITY="${IDENTITY:-id-api-produccion}"
TARGET_PORT="${TARGET_PORT:-8000}"

# 0. Extensión + providers
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# 1. Grupo de recursos: agrupa y permite borrar todo de una al limpiar.
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# 2. Registry + build en la nube (no necesito Docker local; ACR construye).
az acr create --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --sku Basic --location "$LOCATION"
az acr build --registry "$ACR_NAME" --image "$IMAGE_TAG" .

# 3. Identidad administrada: credencial que rota sola y nunca veo (no hay secreto que filtrar).
az identity create --name "$IDENTITY" --resource-group "$RESOURCE_GROUP"
IDENTITY_ID=$(az identity show --name "$IDENTITY" --resource-group "$RESOURCE_GROUP" --query id -o tsv)
PRINCIPAL=$(az identity show --name "$IDENTITY" --resource-group "$RESOURCE_GROUP" --query principalId -o tsv)
ACR_ID=$(az acr show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query id -o tsv)

# 4. Mínimo privilegio: SOLO acrpull, SOLO sobre este registry (no Contributor, no la suscripción).
az role assignment create \
  --assignee "$PRINCIPAL" \
  --role acrpull \
  --scope "$ACR_ID"

# 5. Entorno de Container Apps: frontera segura + Log Analytics (gancho con observabilidad, 5.10).
az containerapp env create \
  --name "$ENVIRONMENT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION"

# 6. Despliegue: ingress público, puerto de la app, pull autenticado por identidad (sin password).
az containerapp create \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENVIRONMENT" \
  --image "$ACR_NAME.azurecr.io/$IMAGE_TAG" \
  --target-port "$TARGET_PORT" \
  --ingress external \
  --registry-server "$ACR_NAME.azurecr.io" \
  --user-assigned "$IDENTITY_ID" \
  --registry-identity "$IDENTITY_ID" \
  --query properties.configuration.ingress.fqdn -o tsv
```

## Por qué cada decisión (lo que el alumno debe poder defender)

- **`--ingress external`** → expone la app a internet. Sin esto solo es alcanzable dentro del entorno.
- **`--target-port`** → debe coincidir con el puerto que escucha FastAPI (el del `uvicorn`/`EXPOSE` de la 5.1). Si no coincide, el health check falla y la app no responde.
- **`--registry-identity` / `--user-assigned`** → el pull se autentica con la **managed identity**, no con password. Elimina la clase entera de bugs de "secreto filtrado".
- **`--role acrpull --scope "$ACR_ID"`** → mínimo privilegio: el contenedor solo puede *leer imágenes* de *ese* registry. Si lo comprometen, el daño está acotado.
- **Variables de entorno** → 12-factor: reproducible, sin secretos hardcodeados.

## Variante aceptable: `az containerapp up`

```bash
az containerapp up --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" \
  --image "$ACR_NAME.azurecr.io/$IMAGE_TAG" --ingress external --target-port "$TARGET_PORT"
```

Es válida para un primer deploy, pero **no** configura la identidad de pull ni el rol acrpull con el
mismo control. El test exige el patrón con identidad; si el alumno usa `up`, debe igualmente crear la
identidad y asignar `acrpull` para pasar las verificaciones de seguridad. El flujo paso a paso es el
preferido cuando importa el mínimo privilegio.

## Notas para el corrector

- El test (`test_deploy.py`) es el piso: verde = decisiones de seguridad correctas. Si está verde pero los **comentarios** faltan o son parafraseo del flag, no pasa de `competente` y el feedback va a la comprensión.
- Error grave a marcar siempre: `--admin-enabled true`, `--registry-password`, o `--role Contributor/Owner`.
- Si el `--target-port` está hardcodeado a un puerto que no es el de su app, señálalo: es un 502 esperando a pasar.
- Acepta nombres de recursos y región distintos; lo no negociable es: identidad administrada + acrpull + ingress/puerto.
