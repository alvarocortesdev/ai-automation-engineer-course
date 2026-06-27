---
ejercicio_id: fase-5/desplegar-en-container-apps
fase: fase-5
sub_unidad: "5.5"
version: 1
---

# Rúbrica — Despliega el contenedor en un servicio managed (seguro)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Hay un test (`test_deploy.py`) que hace
> un **lint estático** del script: úsalo como piso objetivo, **no** como techo. El verde dice "tomó
> las decisiones de seguridad correctas"; la comprensión se evalúa con los comentarios y la defensa
> oral. Verde sin entender no es competente.

## Objetivos evaluados

- O1: Desplegar un contenedor en Azure Container Apps con ingress público y el puerto correcto.
- O2: Autenticar el pull con identidad administrada, sin admin user ni password de registry.
- O3: Asignar mínimo privilegio (solo `acrpull` sobre el registry), evitando Contributor/Owner.

## Criterios y niveles

### C1 — Corrección del despliegue (¿queda alcanzable y completo?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No crea recursos base (grupo/entorno) o no despliega; `pytest` rojo en varias verificaciones. |
| **en-progreso** | Despliega, pero falta `--ingress external` o `--target-port` (la app no sería alcanzable o apuntaría al puerto equivocado). |
| **competente** | Crea grupo + entorno + registry + build + app; ingress público y puerto correcto; `pytest` verde. |
| **excelente** | Además ordena los pasos por dependencias, parametriza por variables de entorno (12-factor) y comenta el *por qué* de cada uno. |

### C2 — Seguridad: identidad y secretos · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Usa `--admin-enabled true` o pasa `--registry-password`/`--registry-username` (secreto expuesto). |
| **en-progreso** | Crea la identidad pero no la usa para el pull (o deja credenciales como fallback). |
| **competente** | Pull autenticado por `--registry-identity`/`--user-assigned`; sin ningún secreto de registry en el script. |
| **excelente** | Explica en comentario por qué la managed identity elimina la clase de bug de "secreto filtrado" y por qué es estrictamente mejor que una password. |

### C3 — Mínimo privilegio (least privilege) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Asigna `Contributor`/`Owner`, o un scope amplio (suscripción/grupo) "para que funcione". |
| **en-progreso** | Usa `acrpull` pero con scope incorrecto (la suscripción en vez del registry), o asigna roles de más. |
| **competente** | Solo `acrpull`, con scope **el registry**; nada de Contributor/Owner. |
| **excelente** | Justifica por qué `acrpull` es el rol exacto y el registry el scope correcto (radio de daño mínimo). |

## Errores típicos a marcar

- `--admin-enabled true` o password de registry: el antipatrón central que el ejercicio busca erradicar.
- `--role Contributor`/`Owner` o scope la suscripción/grupo: viola mínimo privilegio.
- `--target-port` que no coincide con el puerto real de la app (la del 5.1) → 502/timeout en producción.
- Olvidar `--ingress external` (la app queda solo interna) o ponerlo cuando debía ser interno.
- Comentarios que dicen *qué* hace el comando (parafrasean el flag) en vez de *por qué*.
- Hardcodear nombres/valores en vez de leerlos del entorno (rompe 12-factor y reproducibilidad).

## Señales de dependencia-IA

- Script perfecto y verde pero **comentarios ausentes o genéricos**; no puede explicar qué flag hace pública la app.
- Usa `--registry-identity` correctamente pero no sabe explicar la diferencia con `--admin-enabled` (copió sin entender).
- Mete flags extra de un tutorial (escalado, secrets, dapr) que no se pidieron y no puede justificar.
- Asigna `acrpull` por imitación pero no puede decir por qué no `Contributor`.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest -q` y mira qué verificación falla: cada una apunta a una decisión de seguridad concreta. Empieza por la que menciona `identity` o `acrpull`."
- **Pregunta socrática (nivel 2):** "Si usas el admin user del registry y su password, ¿dónde vive esa password y quién podría leerla? ¿Qué cambia si en su lugar la nube le asigna una identidad a tu contenedor?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El pull debe ir por `--registry-identity \"$IDENTITY_ID\"` (sin password). El rol es `acrpull` con `--scope` el id del registry, no la suscripción. La app se expone con `--ingress external --target-port <puerto-de-tu-FastAPI>`. Revisa la sección 4.7 de la lección; el orden de pasos es el del Parsons de la sección 6."

## Conexión con el proyecto / capstone

- Es el **paso de deploy** del pipeline del [capstone F5](/fase-5-devops/proyecto/): tras build + gates de seguridad (5.4), este script publica la app. La identidad administrada y el `acrpull` mínimo son entregables del Definition of Done de seguridad de la fase.
