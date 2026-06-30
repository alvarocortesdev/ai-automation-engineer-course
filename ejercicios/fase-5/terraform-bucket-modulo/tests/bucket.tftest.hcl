# Tests nativos de Terraform. Corren SIN AWS ni credenciales: mock_provider simula
# al provider y permite afirmar sobre el 'plan'. Ejecuta desde la carpeta del ejercicio:
#   terraform init   # descarga el provider (necesita internet, NO creds de AWS)
#   terraform test

mock_provider "aws" {}

run "usa_el_nombre_y_los_tags" {
  command = plan

  variables {
    bucket_name       = "acme-iac-demo"
    environment       = "test"
    enable_versioning = true
  }

  assert {
    condition     = aws_s3_bucket.this.bucket == "acme-iac-demo"
    error_message = "El bucket debe usar el nombre de var.bucket_name"
  }

  assert {
    condition     = aws_s3_bucket.this.tags["Environment"] == "test"
    error_message = "El tag Environment debe venir de var.environment"
  }

  # TODO: agrega un assert que verifique que el versioning queda "Enabled"
  #       cuando enable_versioning = true.
  #       Pista: aws_s3_bucket_versioning.this.versioning_configuration[0].status
}

# TODO (tú): agrega al menos un 'run' propio.
# Sugerencia: variables { enable_versioning = false } y verifica que el status
# del versioning sea "Suspended".
