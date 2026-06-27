---
ejercicio_id: fase-5/cliente-azure-openai-v1
fase: fase-5
sub_unidad: "5.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno antes de un intento real. Úsalo para
> detectar qué le falta y graduar pistas, **nunca** para entregarle el código.

# Solución de referencia — Cliente v1 de Azure OpenAI

## Implementación

```python
import os

from openai import OpenAI


def build_client() -> OpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    return OpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        base_url=f"{endpoint}/openai/v1/",
    )


def responder(client: OpenAI, deployment: str, pregunta: str) -> str:
    respuesta = client.chat.completions.create(
        model=deployment,                       # nombre del DEPLOYMENT, no del modelo base
        messages=[{"role": "user", "content": pregunta}],
    )
    return respuesta.choices[0].message.content
```

## Por qué así (lo que el alumno debe poder defender)

- **Cliente `OpenAI()`, no `AzureOpenAI()`.** Desde la API v1 GA, Azure OpenAI se llama con el cliente
  estándar de OpenAI. El viejo `AzureOpenAI()` ya no hace falta (su única ventaja real, el auto-refresh
  del token, ahora también vive en `OpenAI()`).
- **`base_url` con `/openai/v1/`.** Esa ruta es la que activa la v1. El `.rstrip("/")` evita la `//`
  doble si el endpoint ya termina en `/`.
- **Sin `api_version`.** La v1 lo eliminó: te quedas siempre en la última versión sin tocar código cada mes.
- **`model=deployment`.** En Azure se llama al modelo por el nombre del **deployment** (la instancia que
  creaste en el portal), no por el nombre del modelo base. Equivocarse da `DeploymentNotFound`.
- **Config desde el entorno.** Endpoint y clave en variables de entorno (factor III). En prod, lo ideal
  es Managed Identity (variante en el bloque siguiente), que elimina la clave por completo.

## Variante de producción (Managed Identity — el "excelente")

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def build_client_mi() -> OpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )
    return OpenAI(base_url=f"{endpoint}/openai/v1/", api_key=token_provider)
```

`DefaultAzureCredential` usa la Managed Identity en el App Service y el `az login` en local: el mismo
código, cero claves que rotar o filtrar. A esa identidad se le asigna el rol `Cognitive Services
OpenAI User` (least privilege).

## Notas para el corrector

- El test es estructural + un check de `base_url` (omitido si `openai` no está instalado). Si pasa en
  verde, C1/C2 suelen estar en `competente`; sube a `excelente` solo si el alumno **explica** el porqué
  (model=deployment, qué era `api_version`, Managed Identity).
- Error frecuente válido como `en-progreso`: olvidar el `.rstrip("/")` y producir `//openai/v1/`. El
  test de `/openai/v1` igual pasa, pero señálalo.
- Si aparece `AzureOpenAI` o `api_version`, es `incompleto` en C1 aunque "funcione": el ejercicio mide
  justamente conocer la forma vigente.
