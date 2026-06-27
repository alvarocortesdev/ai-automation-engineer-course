---
ejercicio_id: fase-5/mapa-primitivos-cloud
fase: fase-5
sub_unidad: "5.5"
version: 1
---

# Rúbrica — Mapa de primitivos cloud + IAM de mínimo privilegio

> Rúbrica **analítica** atada a los `objetivos` del contrato. No hay test automático: se corrige por
> la **calidad del razonamiento y las justificaciones**, no por una redacción única. Una elección
> distinta pero bien argumentada (p. ej. App Service en vez de Container Apps) es válida si el alumno
> defiende el trade-off.

## Objetivos evaluados

- O1: Mapear los 4 componentes (compute, fotos, base de datos, secreto) al primitivo correcto, con trade-off.
- O2: Diseñar el acceso de mínimo privilegio y corregir la asignación `Owner` sobre la suscripción.
- O3: Trazar la frontera de responsabilidad compartida del compute elegido y justificar región/zonas.

## Criterios y niveles

### C1 — Mapa de primitivos correcto (¿cada pieza en su bloque?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan componentes o hay errores de categoría graves (p. ej. fotos en el disco del contenedor; Postgres "en el contenedor" sin reconocer la carga operacional). |
| **en-progreso** | Mapea los 4 pero con justificaciones débiles ("porque sí") o sin nombrar ningún trade-off descartado. |
| **competente** | Los 4 componentes al primitivo correcto (compute managed o equivalente, **object storage** para fotos, **DB managed**, secreto inyectado) con una justificación clara por cada uno. |
| **excelente** | Además distingue object vs. block storage con precisión, justifica el compute en el espectro control↔carga operacional, y deja un ADR de una línea por decisión. |

### C2 — IAM de mínimo privilegio (criterio de seguridad) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No detecta el problema del `Owner`, o lo "arregla" con otro permiso amplio (Contributor). |
| **en-progreso** | Dice que `Owner` es "demasiado" pero no explica el **radio de daño** ni acota al permiso/scope mínimo real. |
| **competente** | Nombra el riesgo (un compromiso de la app puede crear/borrar todo) y reduce a lo mínimo real (p. ej. `acrpull` sobre el registry; lectura de un secreto sobre ese secreto). |
| **excelente** | Razona principal/rol/scope por separado, propone **managed identity** para eliminar secretos, y acota el scope al recurso, no al grupo/suscripción. |

### C3 — Responsabilidad compartida + región/zonas (comprensión del modelo) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No traza la frontera, o pone "el proveedor es responsable de todo" / "yo de todo". |
| **en-progreso** | Traza la frontera pero ubica mal quién parchea el SO en su modelo, o elige región solo por latencia. |
| **competente** | Frontera correcta para su compute (incl. quién parchea el SO) + región justificada con varios de los 4 factores + decisión de zonas con criterio. |
| **excelente** | Reconoce que datos y permisos son siempre del cliente en los 3 modelos, y justifica **no** usar multi-zona para 3 usuarios como anti-sobre-ingeniería (con la condición que lo cambiaría). |

## Errores típicos a marcar

- Poner las fotos en el disco del contenedor (efímero) o en block storage en vez de object storage.
- "Arreglar" el `Owner` con `Contributor`: sigue siendo privilegio desproporcionado.
- Confundir **región** con **availability zone**, o elegir región solo por latencia (olvida residencia de datos / disponibilidad de servicios / costo).
- Decir que el proveedor es responsable de los permisos IAM o de los datos (nunca lo es).
- Administrar Postgres a mano "para ahorrar" sin reconocer la carga operacional (backups, parches, HA).
- (transversal) Falta de un solo trade-off defendible o ningún ADR cuando se pidió.

## Señales de dependencia-IA

- Tabla impecable y exhaustiva pero **sin un trade-off propio** ni mención del componente "fotos" como caso especial (señal de plantilla genérica).
- Usa términos correctos (least privilege, shared responsibility) pero no puede explicar **por qué** `Owner` es peor que `acrpull` en términos de radio de daño.
- Recomendaciones sofisticadas (multi-región, zone-redundant) para 3 usuarios, indefendibles para el nivel del proyecto.
- Justificaciones abstractas ("es buena práctica") en vez de referidas a *esta* app y *estos* componentes.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Revisa dos cosas: ¿dónde sobreviven las fotos si el contenedor escala a cero? y ¿qué es lo *único* que tu contenedor necesita hacer en IAM por sí mismo?"
- **Pregunta socrática (nivel 2):** "Si un atacante compromete tu contenedor, ¿qué puede hacer con `Owner` sobre la suscripción? ¿Y con `acrpull` sobre el registry? Esa diferencia es el radio de daño."
- **Dirección concreta (nivel 3, sólo tras intento real):** "El `Owner` permite crear/modificar/borrar cualquier recurso: si comprometen la app, pierdes todo. El contenedor solo necesita **leer su imagen** → rol `acrpull` con scope el registry, y autenticación por **managed identity** para no guardar secretos. Las fotos van a object storage (Blob), no al disco. Revisa la sección 4.5 de la lección."

## Conexión con el proyecto / capstone

- Es el boceto de arquitectura del [capstone F5](/fase-5-devops/proyecto/): define dónde corre el contenedor, dónde viven las fotos y la DB, qué secretos hay y con qué permisos mínimos opera la app. El `iam.md` es un entregable directo del Definition of Done de seguridad.
