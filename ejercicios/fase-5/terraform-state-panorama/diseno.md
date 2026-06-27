# ADR de IaC para el capstone — diseño

> Plantilla. Reemplaza cada `TODO` con tu diseño. Trabájalo **a mano primero**, sin IA.

## 1. El problema (¿por qué no clickear la consola?)

TODO (3–4 líneas): describe con un **ejemplo concreto** por qué desplegar el capstone a mano no es
reproducible ni auditable. Nombra **config drift** y **reproducibilidad**.

## 2. Declarativo vs imperativo

TODO (2–3 líneas): con el ejemplo de "correr `apply` dos veces seguidas", explica por qué Terraform
es declarativo e idempotente, y en qué se diferencia de un script de bash que crea recursos.

## 3. Diseño del state

**¿Dónde vive y cómo se comparte/bloquea?** TODO (2–3 líneas).

**Bloque `backend` que usaría:**

```hcl
terraform {
  backend "s3" {
    # TODO: bucket del state, key, region, encrypt, y el locking nativo (use_lockfile)
  }
}
```

**3 razones por las que el state NUNCA va a Git:**

1. TODO
2. TODO
3. TODO

## 4. Terraform vs OpenTofu

TODO (3–4 líneas): cuál eliges para el proyecto y **por qué**. Trade-off: licencia (BSL vs MPL),
compatibilidad de comandos, a quién le afecta de verdad la restricción.

## 5. Regla de oro

TODO (1 línea): sobre cambios manuales una vez que un recurso es gestionado por Terraform.
