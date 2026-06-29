---
ejercicio_id: track-0/auditoria-repo-limpio
fase: track-0
sub_unidad: "T0.6"
version: 1
---

# Rúbrica — Audita y limpia un repo de portafolio

> Rúbrica **analítica** para un ejercicio de **diagnóstico**. Hay un núcleo no negociable (el secreto
> filtrado es 🔴 crítico y su fix empieza por **rotar la key**; la falta de `LICENSE` tiene una
> consecuencia legal) y un margen de criterio (qué otros problemas prioriza, cómo reescribe los
> commits). Lo que separa una auditoría profesional de una superficial es que **prioriza por gravedad
> real** —seguridad y legal primero, señal después— y que los fixes son **accionables**, no vaguedades.

## Objetivos evaluados
> Copiados del contrato. Cada criterio mapea a uno o más.

- **O1** — Auditar un repositorio y detectar problemas de seguridad, legales y de señal.
- **O2** — Proponer el fix concreto de cada problema, con el orden de pasos correcto ante un secreto
  filtrado.
- **O3** — Reescribir mensajes de commit ruido a Conventional Commits bien formados.

## Criterios y niveles

### C1 — Detección y clasificación por gravedad · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 5 problemas, o no clasifica por gravedad, o se pierde el secreto filtrado. |
| **en-progreso** | Detecta varios problemas pero mezcla gravedades (trata el README vacío igual que la key filtrada) o no marca el secreto como crítico. |
| **competente** | ≥5 problemas; el secreto filtrado y (el password en DATABASE_URL) marcados 🔴; README/commits/licencia priorizados correctamente como 🟡; basura (notebook) como ⚪. |
| **excelente** | Distingue además matices: la key **hardcodeada en `main.py`** (no solo en `.env`) agrava el caso; nota que no hay `.gitignore` como causa raíz del leak. |

### C2 — Fix del secreto: orden correcto · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El fix es "borrar el .env" o "hacer el repo privado", sin rotar la key. |
| **en-progreso** | Menciona rotar la key pero después de otros pasos, o no aborda que el secreto vive en el **historial**. |
| **competente** | Orden correcto: **1) rotar/revocar la key YA** (asumir comprometida) → 2) `.env` al `.gitignore` + `.env.example` → 3) limpiar historial (filter-repo/BFG) o repo nuevo. Reconoce que borrar el archivo no basta. |
| **excelente** | Añade que un escáner de secretos (gitleaks/trufflehog) en CI lo habría atrapado antes, y rota también el password de la DB. |

### C3 — Licencia y consecuencia legal · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona la falta de `LICENSE`. |
| **en-progreso** | Dice "falta licencia" sin explicar la consecuencia. |
| **competente** | Identifica que sin `LICENSE` el repo es "all rights reserved" por defecto (nadie puede usarlo legalmente) y propone una (MIT). |
| **excelente** | Conecta con que un portafolio OSS necesita licencia explícita para cumplir su propósito (que otros lo usen/lean). |

### C4 — Reescritura a Conventional Commits · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No reescribe, o los "Conventional Commits" no siguen el formato `tipo: descripción`. |
| **en-progreso** | Formato correcto pero el tipo elegido no calza con el cambio (p. ej. `feat:` para un arreglo) o no justifica. |
| **competente** | 3 commits con formato `tipo(scope): descripción` válido y tipo apropiado, con una frase que justifica cada tipo. |
| **excelente** | Distingue `feat`/`fix`/`refactor`/`docs`/`chore` con criterio, y nota que el commit "add openai key" jamás debió existir (el fix no es renombrarlo, es que el secreto no se commitea). |

## Errores típicos a marcar
- **Subestimar el secreto:** tratar la key filtrada como problema menor o proponer "borrar el archivo" como fix completo.
- **Olvidar el historial:** creer que borrar `.env` hoy elimina el secreto (sigue en commits anteriores).
- **No rotar:** "lo muevo a variables de entorno" sin revocar la key ya comprometida.
- **Ignorar la licencia:** no detectar `LICENSE` faltante o no saber su consecuencia legal.
- **Conventional Commits mal:** poner `tipo` que no calza (todo `feat:`), o reescribir sin justificar.
- **Mezclar gravedades:** poner el README vacío al mismo nivel que la key filtrada.
- (transversales) no mencionar secret scanning en CI; no notar la key hardcodeada en `main.py` además del `.env`.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Lista exhaustiva y perfectamente formateada pero el orden de pasos del secreto está mal (recitó una lista sin entender por qué rotar va primero).
- Reescribe commits a Conventional Commits impecables pero no puede explicar la diferencia entre `fix` y `refactor`.
- **Verificación sugerida:** pregunta, sin notas, "si solo borras el `.env` y haces el repo privado, ¿por qué la key sigue en riesgo?". Si entendió, responde "porque ya estuvo público / sigue en el historial / hay que asumir que la copiaron".

## Feedback sugerido (graduado)
> Nunca reescribir la auditoría por el alumno.
- **Pista (nivel 1):** "Recorre el árbol y el log una vez más con ojos de atacante: ¿qué archivo nunca debería estar en un repo público, y qué commit lo delata?"
- **Pregunta socrática (nivel 2):** "Si borras el `.env` en un commit nuevo, ¿desaparece de los commits anteriores? ¿Qué guarda Git? Entonces, ¿cuál es el primer paso que de verdad reduce el daño?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu fix del secreto empieza por el repo; debe empezar por la **key**: rótala asumiendo que ya la robaron, *después* ordenas `.gitignore`, `.env.example` y limpieza de historial. Y marca la falta de `LICENSE`: sin ella tu portafolio es legalmente 'all rights reserved'."

## Conexión con el proyecto / capstone
- Esta auditoría es el filtro de calidad que aplicarás a TUS repos antes de pinearlos (T0.6) y de que un reclutador los abra tras el screening (T0.2). El reflejo de "secreto → rotar primero" y "secret scanning en CI" es el mismo que formalizas en los gates de seguridad de la Fase 5.
