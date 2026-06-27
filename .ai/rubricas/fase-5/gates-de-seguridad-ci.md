---
ejercicio_id: fase-5/gates-de-seguridad-ci
fase: fase-5
sub_unidad: "5.4"
version: 1
---

# Rúbrica — Endurece el pipeline de la 5.3 con gates de supply chain

> Rúbrica **analítica** atada a los `objetivos` del contrato. El test estructural (`test_seguridad.py`) da la señal objetiva del YAML; **la comprensión** (qué ataque cierra cada gate, por qué SHA y no tag) es lo que separa `competente` de `excelente` y se mide pidiendo al alumno que lo explique.

## Objetivos evaluados

- O1: Añadir gates de SCA y secret-scanning como jobs, explicando qué ataque previene cada uno.
- O2: Pinear todas las actions a un commit SHA y aplicar `permissions` mínimos.
- O3: Configurar Dependabot (`version: 2`) con `groups` para `github-actions` y `pip`, razonando el trade-off pin vs. estar al día.

## Criterios y niveles

### C1 — Corrección del pipeline (¿pasan los gates?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_seguridad.py` falla en varios asserts: falta un gate, no hay `permissions`, o las actions siguen con tag. |
| **en-progreso** | Pasa parcial: tiene SCA pero no secret-scan (o al revés), o pineó solo algunas actions, o el gitleaks no usa `fetch-depth: 0`. |
| **competente** | `test_seguridad.py` verde: permisos mínimos, **todas** las actions a SHA, gate de SCA, gate de secret-scan con historial completo, `dependabot.yml` válido con `groups`. |
| **excelente** | Lo anterior + `cooldown` en Dependabot, `concurrency`, permisos puntuales por job (p. ej. `security-events: write` solo donde toca), un job de SAST (CodeQL) o de SBOM añadido por iniciativa. |

### C2 — Seguridad / supply chain (el fondo, no la forma) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Deja actions a `@main`/tag, o pone un secreto en texto plano, o `permissions: write-all`. |
| **en-progreso** | Pinea pero no entiende por qué (no puede explicar el tag hijacking); o el gate existe pero bloquearía ante todo (sin criterio de severidad). |
| **competente** | SHA en todo lo ajeno, permisos mínimos, gates con umbral sensato (`fail-on-severity: high`). |
| **excelente** | Articula el modelo de las 4 superficies y conecta cada gate con su ataque; menciona la rotación de secretos y la `cooldown` como defensa contra malware recién publicado. |

### C3 — Comprensión demostrada (el "explícalo" calza con el YAML) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue SAST/SCA/secret-scanning; cree que el YAML por sí solo bloquea el merge. |
| **en-progreso** | Distingue los gates pero no el trade-off pin vs. parche, o no nombra el *required status check*. |
| **competente** | Explica qué ataque previene cada gate, por qué SHA y no tag, y que el gate de merge real es la branch protection (no el YAML). |
| **excelente** | Da un ejemplo concreto propio (p. ej. el incidente de Trivy) y razona la fatiga de alertas como motivo del umbral de severidad. |

## Errores típicos a marcar

- Pinear a tag (`@v4`) creyendo que es inmutable — es la misconception central; el tag es mutable (caso Trivy).
- Secreto en texto plano en el `env:` (debe ser `${{ secrets.X }}`), o no entender que un secreto filtrado hay que **rotarlo**.
- gitleaks sin `fetch-depth: 0` → solo escanea el último commit.
- Dependabot sin `groups` → 20 PRs que nadie revisa (fatiga de PRs); o creer que automergear PRs de Dependabot es seguro.
- Bloquear ante todo CVE (sin umbral de severidad) → fatiga de alertas.
- Confundir SBOM (inventario) con SCA (escaneo), o SAST (tu código) con SCA (código ajeno).
- (transversal) `permissions: write-all` o ausencia de `permissions` → privilegio excesivo del `GITHUB_TOKEN`.

## Señales de dependencia-IA

- YAML impecable con SHA perfectos pero no sabe explicar qué es un SHA ni por qué un tag es inseguro: lo generó, no lo entendió.
- Usa términos sofisticados (OIDC, SLSA, provenance attestation) que el YAML no implementa y no puede defender.
- "Sé qué hace cada gate" pero al pedir "¿qué ataque previene el secret-scanning que NO previene la SCA?" no puede responder.
- Pineó a SHA pero dejó un secreto en texto plano: copió el patrón sin entender el principio.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `uv run pytest test_seguridad.py` y atiende el primer assert que falla. Para cada action que el test rechaza, pregúntate: ¿esta referencia se puede *mover*?"
- **Pregunta socrática (nivel 2):** "El atacante de Trivy no tocó tu `.yml` y aun así corriste su malware. ¿Qué tuvo que cambiar él, y qué referencia tuya se lo permitió?" / "Tu gate de SCA marca 200 CVEs y bloquea todo. ¿Qué hará tu equipo el viernes a las 7 PM?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El pin va al **SHA del commit** (40 hex), no al tag; el tag es mutable. El secret-scan necesita `fetch-depth: 0`. El gate bloquea en `high`/`critical`, no ante todo. Y para que un PR rojo no se mergee, falta el *required status check* (branch protection), igual que en la 5.3. Revisa secciones 4.2–4.5 de la lección."

## Conexión con el proyecto / capstone

- Este es el punto del DoD del Capstone F5 ("secret-scanning + dependency-scanning en el pipeline") en miniatura: lo que armas aquí se copia tal cual al capstone, y la comprensión que demuestres evita arrastrar la creencia de que "tests verdes = seguro".
