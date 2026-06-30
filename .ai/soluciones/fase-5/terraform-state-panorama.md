---
ejercicio_id: fase-5/terraform-state-panorama
fase: fase-5
sub_unidad: "5.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una solución de referencia, no la
> única válida: la redacción y la elección Terraform/OpenTofu varían. Se evalúa el **criterio**, no
> que coincida palabra por palabra.

# Solución de referencia — ADR de IaC

## 1. El problema

Desplegué el capstone clickeando la consola: creé un bucket, una base de datos y un servicio a mano.
Dos meses después no recuerdo la región exacta ni la config del bucket (**no-reproducibilidad**: no
puedo recrear dev igual a prod ni reconstruir si se borra). Peor: un compañero entró a la consola y
cambió el tamaño de la instancia "para una prueba" y nadie lo registró (**config drift**: la realidad
ya no coincide con lo que cualquiera creería leyendo… nada, porque no hay artefacto que leer). IaC
convierte todo eso en archivos versionados, revisables en un diff y recreables con un comando.

## 2. Declarativo vs imperativo

Un script de bash sería imperativo: `aws s3 mb ...; if no existe la tabla; entonces créala`. Yo
escribo los pasos y manejo el "¿ya existe?". Terraform es declarativo: declaro "quiero que exista el
bucket X con versioning" y él compara con el state + la nube y calcula el diff mínimo. Por eso es
**idempotente**: si corro `apply` dos veces sin cambiar el código, la segunda dice "0 to add, 0 to
change, 0 to destroy" — el estado real ya es el deseado.

## 3. Diseño del state

**Dónde vive / cómo se comparte:** en un backend remoto central (un bucket S3), no en la laptop de
cada uno. El locking lo da el propio S3 con escrituras condicionales (`use_lockfile`), así dos `apply`
concurrentes no corrompen el state.

```hcl
terraform {
  backend "s3" {
    bucket       = "acme-tfstate"
    key          = "prod/capstone/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true # locking nativo S3 (Terraform 1.11+); ya NO necesita DynamoDB
  }
}
```

**3 razones por las que el state NUNCA va a Git:**

1. Contiene **secretos en texto plano** (passwords de DB, tokens): commitearlo es filtrarlos a todos.
2. Git **no provee locking**: dos personas con su copia local divergen y se pisan; el state se corrompe.
3. No es un artefacto revisable como el código: es estado vivo. Va en backend cifrado + `.gitignore`.
   (El que SÍ va a Git es el `.terraform.lock.hcl`, que fija el hash del provider.)

## 4. Terraform vs OpenTofu

Para este proyecto elijo **Terraform** por inercia del ecosistema (más módulos, más doc, lo que pide
la mayoría de las ofertas) — pero la decisión es **reversible**: OpenTofu es 100% compatible en
comandos. La razón es que la **BSL no me afecta**: solo corro `apply` contra mi propia infra, no
construyo un producto que revenda Terraform. Si el proyecto fuera un SaaS que envuelve Terraform, o si
una licencia OSI-aprobada (MPL) fuera requisito de procurement, elegiría **OpenTofu** sin dudar. (IBM
compró HashiCorp en 2025; OpenTofu está bajo la Linux Foundation/CNCF.)

## 5. Regla de oro

Una vez que un recurso es gestionado por Terraform, **se cambia SOLO por Terraform** — nunca a mano en
la consola, o aparece drift.

---

## Notas para el corrector

- Aceptar **OpenTofu** como elección si la justificación es defendible (procurement, MPL, divergencia de features).
- El bloque `backend` **debe** usar `use_lockfile` (o el equivalente del cloud elegido), no DynamoDB como única opción; aceptar DynamoDB solo si el alumno reconoce que está deprecado.
- Exigir las **3 razones** de C2 con al menos secretos + locking/colisión.
- El ejemplo del problema debe ser **concreto**, no genérico — es la señal de comprensión real.
