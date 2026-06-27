---
ejercicio_id: fase-5/terraform-bucket-modulo
fase: fase-5
sub_unidad: "5.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una implementación de referencia;
> hay variaciones válidas (formato, nombres del `run` propio). Úsala para graduar pistas y verificar
> que el verde de `terraform test` viene de una config limpia y parametrizada, no de un atajo.

# Solución de referencia — Módulo de bucket testeable

## `main.tf`

```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}
```

## `outputs.tf`

```hcl
output "bucket_id" {
  description = "ID (nombre) del bucket creado"
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "ARN del bucket creado"
  value       = aws_s3_bucket.this.arn
}
```

## `tests/bucket.tftest.hcl` (assert que faltaba + run propio)

```hcl
mock_provider "aws" {}

run "usa_el_nombre_y_los_tags" {
  command = plan

  variables {
    bucket_name       = "donpelusa-iac-demo"
    environment       = "test"
    enable_versioning = true
  }

  assert {
    condition     = aws_s3_bucket.this.bucket == "donpelusa-iac-demo"
    error_message = "El bucket debe usar el nombre de var.bucket_name"
  }

  assert {
    condition     = aws_s3_bucket.this.tags["Environment"] == "test"
    error_message = "El tag Environment debe venir de var.environment"
  }

  # assert que faltaba:
  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Enabled"
    error_message = "Con enable_versioning=true, el status debe ser Enabled"
  }
}

# run propio (lo que el alumno debe agregar): el camino contrario.
run "versioning_suspendido_cuando_es_false" {
  command = plan

  variables {
    bucket_name       = "donpelusa-iac-demo"
    environment       = "dev"
    enable_versioning = false
  }

  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Suspended"
    error_message = "Con enable_versioning=false, el status debe ser Suspended"
  }
}
```

## Puntos clave que el corrector debe verificar

1. **Parametrización real.** El nombre y los tags salen de variables; el status del versioning es el
   **ternario** `var.enable_versioning ? "Enabled" : "Suspended"`, no un literal fijo.
2. **Referencia correcta.** `aws_s3_bucket_versioning.this.bucket = aws_s3_bucket.this.id` (dependencia
   implícita: el versioning se crea después del bucket).
3. **Acceso al bloque.** El assert usa `versioning_configuration[0].status` — el `[0]` porque
   `versioning_configuration` es un bloque (se accede como lista).
4. **Cero secretos.** Ningún `access_key`/`secret_key` en los `.tf`; provider pineado intacto.
5. **`terraform test` verde** con los asserts dados + el del versioning + al menos un `run` propio que
   varíe la entrada (idealmente el caso `Suspended`).
6. **Entiende el mock.** `mock_provider "aws" {}` simula el provider: `command = plan` evalúa la config
   sin llamar a AWS ni necesitar credenciales. El verde no implica que se tocó la nube.

## Verificación rápida (corrector)

```bash
cd ejercicios/fase-5/terraform-bucket-modulo
terraform init && terraform test
# esperado: todos los run en verde, sin credenciales ni recursos reales
terraform fmt -check   # sin diferencias
```
