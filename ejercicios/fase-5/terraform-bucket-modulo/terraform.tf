# terraform.tf — versión de Terraform y providers (COMPLETO, no lo toques).
# No hay backend remoto aquí: en este ejercicio el state es local y el test usa
# mock_provider, así que 'terraform init' + 'terraform test' corren offline,
# sin credenciales de AWS. El bloque backend se enseña en la lección (sección 4.6).

terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Credenciales: del entorno (variables AWS_*), NUNCA en el código.
  # El test no las necesita: mock_provider simula al provider.
}
