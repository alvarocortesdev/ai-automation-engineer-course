# Tests del capstone

Este capstone es de **diseño abierto**: tú defines el dominio y los nombres de los endpoints, así que
**no hay una suite rígida que venga escrita**. Tú escribes los tests —y los mides con **mutation score**,
no con % de coverage.

`test_aceptacion_plantilla.py` es una **guía**: muestra los *patrones* de test de contrato que tu API debe
tener, con `@pytest.mark.skip` y `TODO` para que los adaptes a tus rutas. No es una solución; es un molde.

## Qué tienes que cubrir (mínimo)

**Tests de contrato (con `TestClient`):**

- `422` cuando un body no pasa la validación pydantic (campo obligatorio faltante).
- `401` cuando llamas a un endpoint protegido sin token (o con token inválido/expirado).
- `404` con forma **RFC 9457** (`application/problem+json`) cuando el recurso no existe **y** cuando el recurso
  es de otro usuario (IDOR cerrado: el ajeno "no existe" para mí).
- **Idempotencia:** dos POST al endpoint sensible con el mismo `Idempotency-Key` → el efecto ocurre **una** vez
  y la segunda respuesta es la del primer intento.
- **SSRF:** el import con una URL interna (`http://169.254.169.254/`, `http://127.0.0.1:...`, una IP privada) →
  `400`, sin que la API haga la petición saliente.
- `429` cuando superas el rate limit de auth/import.

**Tests de dominio (puros, sin levantar Postgres):**

- Reglas de negocio probadas contra un **repo en memoria** que implementa el mismo puerto que el repo
  SQLAlchemy. (Aquí se nota si tu hexágono está bien hecho: si necesitas la base de datos para testear la
  lógica, el dominio está acoplado.)

## Cómo medir que sirven

```bash
uv run pytest            # todos en verde
uv run mutmut run        # mutation testing: mata mutantes, no persigas %
uv run mutmut results    # revisa los sobrevivientes: cada uno es una aserción que falta
```

Un test sin `assert` da coverage y no detecta nada. El mutation score es el que no miente.
