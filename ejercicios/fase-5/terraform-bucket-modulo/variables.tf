# variables.tf — entradas configurables (COMPLETO).

variable "bucket_name" {
  description = "Nombre global y único del bucket S3"
  type        = string
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod", "test"], var.environment)
    error_message = "environment debe ser dev, staging, prod o test."
  }
}

variable "enable_versioning" {
  description = "Si true, activa el versioning del bucket"
  type        = bool
  default     = true
}
