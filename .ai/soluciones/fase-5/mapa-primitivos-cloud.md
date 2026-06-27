---
ejercicio_id: fase-5/mapa-primitivos-cloud
fase: fase-5
sub_unidad: "5.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una solución de referencia para
> graduar pistas y detectar qué se le escapó, **nunca** para entregarla. Las elecciones admiten
> criterio: una alternativa bien argumentada (App Service, otra región) es válida.

# Solución de referencia — Mapa de primitivos cloud + IAM

## 1. `mapa.md` (de referencia)

| Componente | Primitivo cloud | Servicio (Azure) | Justificación + trade-off descartado |
|---|---|---|---|
| App FastAPI (ya en imagen) | **Compute: contenedores managed** | Azure Container Apps | Ya tengo imagen; quiero escala-a-cero y no parchear SO. Descarté **VM** (carga operacional) y **Functions** (es un servidor HTTP de larga vida, no eventos cortos). |
| Fotos de perfil de usuario | **Object storage** | Azure Blob Storage | Archivos completos servidos por URL, duraderos, baratos; sobreviven al contenedor efímero. Descarté el **disco del contenedor** (efímero) y **block storage** (es para discos de VM/DB, no archivos). |
| Datos de usuarios | **Base de datos managed** | Azure Database for PostgreSQL Flexible Server | Backups, parches y HA los hace el proveedor. Descarté **Postgres en contenedor/VM** por la carga operacional (yo respondería por backups y CVEs). |
| Cadena de conexión | **Secreto inyectado** | Container Apps secrets / Key Vault + managed identity | Config en el entorno (12-factor); no se hornea en la imagen ni se commitea. Descarté ponerla como variable en texto plano en la imagen. |

ADR de ejemplo: `Decidí Container Apps · descarté VM · porque ya tengo imagen y quiero escala-a-cero sin administrar el SO.`

## 2. `iam.md` (de referencia)

**Qué está mal con `--role Owner --scope $SUBSCRIPTION_ID`:** le da a la app permiso para **crear,
modificar y borrar cualquier recurso de toda la suscripción** (incl. la base de datos, otras apps,
asignaciones de roles). Si alguien compromete el contenedor (un RCE, una dependencia maliciosa),
el **radio de daño** es total: puede exfiltrar datos, borrar todo o levantar mineros a tu nombre.
Es la causa #1 de brechas cloud.

**Reescritura de mínimo privilegio.** El contenedor, por sí mismo, solo necesita **leer su imagen**:

```bash
az role assignment create \
  --assignee "$IDENTITY_PRINCIPAL" \
  --role acrpull \
  --scope "$ACR_ID"        # scope = el registry, no la suscripción
```

- **Principal:** una **managed identity** (no un usuario con clave) → no hay secreto que filtrar.
- **Rol:** `acrpull` (solo pull de imágenes), no `Contributor`/`Owner`.
- **Scope:** el registry, no la suscripción ni el grupo.
- El acceso a las **fotos (Blob)** y al **secreto** se concede aparte, también acotado: rol de
  *Storage Blob Data Contributor* sobre **ese contenedor de blobs**, y lectura sobre **ese secreto**.
  Cada permiso, su recurso. Nada de comodines.

## 3. `responsabilidad.md` (de referencia, para Container Apps)

| Responsabilidad | ¿Quién? |
|---|---|
| Hardware, datacenter, red física, hipervisor | Proveedor |
| Sistema operativo del host + parches | **Proveedor** (es managed) |
| Runtime de contenedores, orquestador, escalado | Proveedor |
| **Mi imagen** (su contenido, sus CVEs, sus deps) | **Yo** |
| **Mis datos** (DB, blobs) | **Yo** |
| **Config de IAM / permisos / secretos** | **Yo (siempre)** |
| Config de red de mi app (ingress, reglas) | **Yo** |

Clave: cuanto más managed el compute, menos parcheo yo —pero **datos y permisos son míos en los
tres modelos**. En una **VM** yo sumaría: parchar el SO, el runtime y el auto-restart.

## 4. `region.md` (de referencia)

> Elijo **Brazil South**: es de las regiones más cercanas a usuarios en Chile (latencia razonable) y
> con disponibilidad amplia de servicios; el costo es aceptable. No tengo requisitos de residencia de
> datos estrictos para un proyecto de portafolio, pero verificaría que los servicios de IA que usaré
> en Fase 6 estén disponibles ahí. **No** uso multi-zona (zone-redundant): para 3 usuarios reales,
> pagar réplicas en varias zonas es sobre-ingeniería. Acepto el riesgo de una caída zonal a cambio de
> costo; **si esto creciera a usuarios pagos con SLA, activaría zone-redundancy** en el entorno y en la
> base de datos.

ADR: `Decidí single-zone en Brazil South · descarté multi-zona · porque 3 usuarios no justifican el costo de HA; condición de cambio: usuarios pagos / SLA.`

## Notas para el corrector

- Acepta **App Service** en vez de Container Apps si justifica el trade-off; acepta otra región cercana bien argumentada.
- El error grave a marcar siempre: **fotos en el disco del contenedor** y **"arreglar" el Owner con Contributor**.
- Si no propone managed identity (deja una clave/password), es a lo sumo `en-progreso` en C2 aunque acote el rol.
- Premiar (excelente) que reconozca que datos+permisos son del cliente en los 3 modelos y que **no** sobre-ingeniería con multi-zona para 3 usuarios.
