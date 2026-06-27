# Dockerfile de ejemplo para AUDITAR — tiene violaciones de 12-factor.
# No lo uses como plantilla. Identifica los problemas en auditoria.md.

FROM python:3.13

WORKDIR /app
COPY . .

# Dependencias sin versiones pinneadas y sin lockfile:
RUN pip install fastapi uvicorn psycopg2 stripe

# Secreto horneado en la imagen (queda en una capa, visible con `docker history`):
ENV STRIPE_API_KEY=sk_live_51Hxxxxxxxxxxxxxxxx_CLAVE_REAL

# Arranca ejecutando el script directamente:
CMD ["python", "app.py"]
