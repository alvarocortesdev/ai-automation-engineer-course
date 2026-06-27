# Tu Dockerfile de producción va aquí. Escríbelo a mano (reúsa el de `dockerizar-fastapi` y endurécelo).
#
# Requisitos (ver lección §4 paso 2 y §6 capa 1):
#   1. Multi-stage: etapa `builder` (instala deps desde el lockfile) + etapa `runtime` mínima.
#   2. Base pinneada y slim (p. ej. python:3.13-slim). NADA de :latest.
#   3. Orden de capas: instala dependencias ANTES de copiar el código de la app (mejor caché).
#   4. Usuario NO-root (crea un usuario de sistema y usa USER).
#   5. HEALTHCHECK que golpee /health (la imagen slim no trae curl: usa python o wget si está).
#   6. EXPOSE el puerto de la app y un CMD explícito.
#   7. La imagen de runtime NO incluye el gestor de paquetes ni el toolchain de build.
#
# Borra estos comentarios cuando termines.
#
# TODO: escribe tu Dockerfile multi-stage aquí.
