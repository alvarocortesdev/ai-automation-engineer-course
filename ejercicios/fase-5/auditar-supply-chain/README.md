# auditar-supply-chain — Auditoría de supply chain de un workflow real

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.4` Gates de seguridad y supply chain en CI
**Ruta:** crítica · **Timebox:** 40–45 min · **Modalidad:** a-mano (auditoría + write-up)

## 🎯 Objetivo

Auditar `workflow-a-auditar.yml` —un pipeline que "funciona" pero está lleno de hoyos
de cadena de suministro— **como lo haría un ingeniero de seguridad**: encontrar las
fallas, clasificarlas (gate + OWASP CICD-SEC), asignarles severidad, proponer el
arreglo, y **priorizar por impacto**.

## 📋 Contexto

Esta es la habilidad examinable de verdad: no "sé poner un job de Trivy", sino **"sé
mirar un pipeline y ver dónde está el riesgo"**. Es el criterio que separa copiar un
YAML de entender la superficie de ataque. Alimenta directo el Capstone F5: tu propio
pipeline no debe tener ninguna de estas fallas.

## 📏 Primero-Sin-IA

1. Audita **solo**, a mano (timebox arriba). Recorre el YAML **línea por línea con una pregunta por línea**.
2. Solo entonces, consulta **documentación oficial** (OWASP CICD-SEC Top 10, hardening de GitHub Actions).
3. **Solo al final**, usa IA para *revisar tu auditoría* — no para *generar los hallazgos*.
4. Mañana, vuelve a auditarlo de memoria. Si no reconoces el PPE sin notas, repasa la sección 6.1 de la lección.

## 🛠️ Instrucciones

1. Lee `workflow-a-auditar.yml`. **No lo corras** (vive en la raíz a propósito, no en `.github/workflows/`).
2. Completa `hallazgos.md`. Para **cada** problema (hay al menos 6), llena los 5 campos:
   - **Qué** (la línea concreta).
   - **Por qué** es peligroso (qué haría un atacante).
   - **Clasificación**: gate/concepto (SAST / SCA / secret / pin / permisos / PPE) + categoría OWASP
     CICD-SEC si puedes (p. ej. CICD-SEC-03 *Dependency Chain Abuse*, CICD-SEC-04 *Poisoned Pipeline Execution*).
   - **Severidad** (alta/media/baja) con una frase que la justifique.
   - **Arreglo** concreto.
3. Cierra con la **priorización**: ¿qué arreglarías primero y por qué?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Encontraste **al menos 6** fallas distintas (no 6 variantes de la misma).
- [ ] Cada hallazgo tiene los 5 campos completos.
- [ ] Identificaste el **Poisoned Pipeline Execution** (`pull_request_target` + checkout del PR + secrets)
      y lo marcaste como **el de mayor severidad**.
- [ ] Distingues un **secreto en texto plano** (filtración) de una **action sin pinear** (supply chain): no los mezclas.
- [ ] Tu priorización pesa **impacto real**, no orden de aparición.
- [ ] Puedes defender cada hallazgo en voz alta, sin notas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Una pregunta por línea, de arriba abajo: ¿este evento (`on:`) expone secrets a PRs de forks?
¿qué permisos pide (`permissions:`)? ¿esta action está pineada a SHA, o a un tag/rama? ¿de quién es
la action —oficial o de un desconocido? ¿hay algún valor que **parezca** un secreto literal? ¿se
ejecuta código que viene **del PR** o **de internet** (`curl | bash`)? ¿algún `${{ ... }}` mete
texto controlable por un atacante dentro de un `run:`? El hallazgo más grave casi siempre **combina
acceso a secrets con ejecución de código no confiable** — busca esa combinación primero.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu IA:

- tu `hallazgos.md`,
- la **rúbrica**: `.ai/rubricas/fase-5/auditar-supply-chain.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/auditar-supply-chain.md`
— no la mires antes de hacer tu propia auditoría.
