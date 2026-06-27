---
ejercicio_id: fase-5/plan-de-despliegue
fase: fase-5
sub_unidad: "5.9"
version: 1
---

# Rúbrica — Plan de despliegue de la app completa

> Rúbrica **analítica** para un ejercicio de **razonamiento/diseño**. Lo que se evalúa es el **criterio**: ¿elige por restricciones y defiende el trade-off, o copia "lo que se hace siempre"? No hay un único plan correcto —hay planes **bien justificados** y planes que ignoran una restricción. El corrector mide la justificación, no el formato de la tabla.

## Objetivos evaluados
- **O1** — Asignar cada pieza a una opción de despliegue justificando el trade-off.
- **O2** — Determinar la fuente correcta del certificado HTTPS por pieza.
- **O3** — Diseñar variables por ambiente (público vs. secreto) y argumentar por restricciones el "no Kubernetes".

> Plan de referencia razonable (no el único): **frontend Next.js → Vercel**; **backend FastAPI → homelab + Cloudflare Tunnel** (dado el presupuesto ~$0 y el homelab tras CGNAT) o **VPS + Caddy** (si hubiera IP pública); **Postgres → managed o contenedor en el mismo host del backend**. El corrector lo conoce; **no se lo dicta al alumno**: evalúa que el suyo esté defendido.

## Criterios y niveles

### C1 — Asignación y trade-offs (¿elige por restricciones?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `plan.md`, o asigna piezas sin justificar (o "todo a Kubernetes/todo a un cloud" sin razón). |
| **en-progreso** | Asigna las 3 piezas pero la justificación es genérica ("es lo mejor") o ignora una restricción dura (presupuesto, CGNAT). |
| **competente** | Cada pieza tiene opción + justificación que **nombra la restricción** que manda; menciona el trade-off descartado. |
| **excelente** | Además contrasta dos opciones viables para una pieza (p. ej. VPS+Caddy vs. túnel) y elige por una restricción concreta; ADRs de una línea por decisión. |

### C2 — Estrategia de HTTPS por pieza · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `https.md`, o dice "pongo HTTPS" sin fuente del certificado. |
| **en-progreso** | Acierta una pieza pero confunde otra (p. ej. cree que el homelab por túnel necesita Let's Encrypt en el origen). |
| **competente** | Identifica bien la fuente del cert por pieza: Vercel/Cloudflare (edge) vs. Caddy+Let's Encrypt (origen). |
| **excelente** | Explica **dónde se termina el TLS** en cada camino y cuándo usaría DNS-01 en vez de HTTP-01 (wildcard / sin puerto 80). |

### C3 — Variables por ambiente: público vs. secreto · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `entornos.md`, o no distingue ambientes. |
| **en-progreso** | Tabla por ambiente, pero clasifica mal público/secreto (o no explica `NEXT_PUBLIC_`). |
| **competente** | Marca correctamente público vs. secreto, dónde vive cada variable, y explica que `NEXT_PUBLIC_` se incrusta en el bundle del navegador. |
| **excelente** | Además ubica los secretos solo en el servidor y nombra el riesgo concreto de un secreto en `NEXT_PUBLIC_` (queda público en DevTools). |

### C4 — Argumento "no Kubernetes" (dimensionar) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `no-kubernetes.md`, o argumenta "porque es difícil / no sé". |
| **en-progreso** | Rechaza k8s por gusto, sin nombrar qué resuelve k8s ni por qué no aplica. |
| **competente** | Dice qué resuelve k8s (orquestar muchos servicios, auto-escalar, self-healing) y por qué 3 usuarios no crean esa restricción (YAGNI). |
| **excelente** | Nombra el **punto de quiebre**: a qué escala/condición k8s o un managed cloud empezarían a ganar. |

## Errores típicos a marcar
- **Asignar por moda, no por restricción** ("Kubernetes porque es profesional"): el antipatrón central de la lección.
- **Abrir el puerto del router** como plan para el homelab (ignora CGNAT, expone la IP de casa) en vez de un túnel.
- **Creer que el homelab por túnel necesita Let's Encrypt en el origen**: el TLS se termina en el edge de Cloudflare.
- **Poner un secreto en `NEXT_PUBLIC_`** o no entender que ese prefijo lo hace público.
- **Commitear el `.env`** o no separar `.env.example`.
- (transversales) falta de un solo trade-off defendible; ningún ADR; no nombrar costo cuando el presupuesto es una restricción dura.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Plan "perfecto" con stack sofisticado (k8s + service mesh + IaC) que **contradice** el presupuesto y los 3 usuarios: suena a respuesta de IA sin leer las restricciones.
- `https.md` correcto en general pero que no puede explicar **por qué** el túnel no necesita cert en el origen.
- Vocabulario por encima del resto del trabajo sin poder defenderlo.
- **Verificación sugerida:** pídele que cambie una restricción (ahora SÍ hay IP pública / ahora son 50.000 usuarios) y rehaga la decisión. Si razonó de verdad, ajusta; si copió, se traba.

## Feedback sugerido (graduado)
> Nunca entregar el plan resuelto antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada pieza, escribe primero la **restricción que más manda** (tipo de app, ¿hay IP pública?, presupuesto). La decisión cae casi sola después."
- **Pregunta socrática (nivel 2):** "Tu homelab está tras CGNAT. Si abres el puerto 443 del router, ¿qué pasa exactamente? ¿Y de dónde sale el certificado si usas un túnel?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Revisa el árbol de decisión (4.1) y la sección de HTTPS (4.6): el camino sin IP pública es túnel + TLS en el edge; el VPS público es reverse proxy + Let's Encrypt en el origen. Reescribe `plan.md` y `https.md` marcando esa diferencia."

## Conexión con el proyecto / capstone
- Este plan **es** el boceto de producción del [Capstone F5](/fase-5-devops/proyecto/): define dónde vive cada pieza, cómo consigue HTTPS y dominio, y demuestra que sabes dimensionar (no sobre-ingeniar) — el criterio que el capstone evalúa.
