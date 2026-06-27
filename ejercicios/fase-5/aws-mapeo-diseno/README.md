# AWS para tu capstone: mapea servicios y diseña el acceso con least privilege

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.7` AWS profundización
**Ruta:** opcional / profundización · **Timebox:** 35–45 min · **Modalidad:** a mano (diseño/razonamiento)

## 🎯 Objetivo

Planificar, **en papel**, cómo desplegarías el capstone de la fase (una API con archivos +
base de datos + una tarea por evento) en AWS, demostrando que (1) mapeas los servicios de AWS a
los **primitivos de cloud** de la lección 5.5 (Cloud troncal),
(2) aplicas **least privilege** en IAM, y (3) entiendes el **costo** real (free tier 2026).

## 📋 Contexto

El capstone de la Fase 5 se puede desplegar en cualquier cloud; lo que se evalúa es tu **criterio**,
no que uses AWS. Este ejercicio te obliga a tomar decisiones defendibles (qué servicio para qué
necesidad, por qué un role y no una access key) y a escribirlas como lo harías en un **ADR**. No
necesitas una cuenta de AWS ni desplegar nada: es 100% diseño en `diseno.md`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Diseña con lo que entendiste, aunque dudes.
2. Solo entonces, consulta **documentación oficial** (IAM best practices, AWS Free Tier).
3. **Solo al final**, usa IA para *revisar y explicar* tu diseño — no para *generarlo*.
4. Mañana, **redibuja la tabla de mapeo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Completa `diseno.md` (hay una plantilla en este directorio) con cinco secciones:

1. **Tabla de mapeo** (≥6 filas): para cada necesidad del capstone — correr la API, guardar
   archivos, base de datos, tarea disparada por subida de archivo, logs, secretos — indica el
   **primitivo** (5.5), el **servicio AWS** y su **equivalente en Azure**.
2. **Decisión de compute** (3–4 líneas): ¿EC2, ECS/Fargate/App Runner, o Lambda para la API?
   Justifica según el **patrón de carga**, no por preferencia.
3. **Diagrama** de la arquitectura (Mermaid en el `.md`, o a mano fotografiado): qué habla con qué.
4. **IAM**: escribe la **policy JSON de least privilege** para que la tarea por evento (Lambda)
   lea el bucket de uploads y escriba sus logs. Explica en 2 líneas por qué usas un **role** y no
   access keys.
5. **Costo/riesgo** (3 líneas): qué cambió en el **free tier 2026** y qué pondrías el día 1 para no
   llevarte una boleta sorpresa.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla mapea **≥6** necesidades a primitivo + AWS + Azure, sin errores de traducción.
- [ ] La decisión de compute tiene un **trade-off defendible** (carga → servicio), no un "porque sí".
- [ ] La policy IAM es **least privilege** real: acciones **enumeradas** (no `*`) y recurso acotado a
      **ARN** (no `*`).
- [ ] Explicas por qué un **role** (credenciales temporales) y no una access key de larga vida.
- [ ] Mencionas el cambio del **free tier 2026** y una medida concreta de control de costo.
- [ ] Puedes **explicar sin notas** el mapeo de los 5 servicios a sus primitivos.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para la tabla, **deriva** cada fila de una necesidad del capstone (no copies la de la lección
entera). Para el compute: una API con tráfico parejo no es el caso ideal de Lambda (cold start +
always-on caro) — piensa qué patrón favorece cada opción. Para la policy, enumera **solo** las
acciones que la Lambda invoca de verdad (`s3:GetObject`, `logs:CreateLogStream`, `logs:PutLogEvents`)
y acota el `Resource` al ARN del bucket y del log group. Para el costo, recuerda que el free tier
dejó de ser "12 meses gratis": ¿qué herramienta te avisa **antes** de gastar?

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (`diseno.md` en este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/aws-mapeo-diseno.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/aws-mapeo-diseno/` — no la mires antes
de intentarlo de verdad.
