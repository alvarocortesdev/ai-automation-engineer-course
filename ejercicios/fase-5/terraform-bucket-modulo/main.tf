# main.tf — los recursos de la infraestructura.
# Implementa lo marcado con TODO. NO cambies los nombres locales de los recursos
# (aws_s3_bucket.this, aws_s3_bucket_versioning.this): el test los referencia.

resource "aws_s3_bucket" "this" {
  # TODO: usa var.bucket_name como nombre del bucket
  # TODO: agrega tags { Environment = var.environment, ManagedBy = "Terraform" }
}

resource "aws_s3_bucket_versioning" "this" {
  # TODO: referencia el bucket de arriba con aws_s3_bucket.this.id
  # TODO: bloque versioning_configuration con status = ...
  #       "Enabled" si var.enable_versioning, si no "Suspended" (usa el operador ternario)
}
