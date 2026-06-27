# Ejercicio 5.8 — Auditoría FinOps: una factura se disparó

> **Modalidad: a mano (de diseño/razonamiento, sin desplegar, sin IA).** Entrena el reflejo que una
> entrevista de cloud realmente evalúa: dada una factura sorpresa, encontrar el balde grande, proponer
> el freno que faltaba y rehacer la estimación que lo habría anticipado. No se toca ninguna consola:
> se **diagnostica y se decide**.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.8` Costos cloud
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Diagnosticar las trampas de costo de la arquitectura a partir de su factura, **ordenadas por impacto en dólares**.
- **O2** — Diseñar el control faltante: **tags** de atribución + **budget con umbrales de alerta** + qué **apagar/redimensionar**.
- **O3** — Rehacer la **estimación previa** que habría anticipado el golpe, conectando cada línea con su driver.

## 📋 El caso

Un colega desplegó una app de IA pequeña (un resumidor de documentos que llama a un LLM). Esperaba
"unos USD 20 al mes". Llegó la factura del primer mes: **USD 387**. La cuenta **no tiene tags ni
budget**. Esto es lo que hay desplegado:

| Recurso | Detalle | Línea en la factura |
|---|---|---|
| VM mediana (compute) | encendida 24/7 desde el día 1; corre el backend | USD 70 |
| **Segunda VM "de pruebas"** | la levantó para un experimento y **la dejó encendida** | USD 70 |
| NAT Gateway | el backend está en subred privada y sale a internet por aquí | USD 33 base + USD 38 procesado |
| Egress a internet | la app sirve PDFs procesados a los usuarios (~1.8 TB el mes) | USD 153 |
| Object storage | 40 GB de PDFs guardados | USD 0,92 |
| PostgreSQL managed | instancia pequeña | USD 14 |
| Disco huérfano | quedó de una VM que borró la semana pasada | USD 8 |
| **Total** | | **≈ USD 387** |

## 📏 Primero-Sin-IA (en este orden, timebox 40 min)

1. Resuélvelo **solo**, a mano, en archivos markdown. Está bien dudar de algún número.
2. Solo entonces, consulta **documentación oficial** (la sección 9 de la lección tiene los enlaces).
3. **Solo al final**, usa IA para *revisar* tu razonamiento —no para generarlo.
4. Mañana, reconstruye los hallazgos de memoria. Si no puedes, no lo aprendiste todavía.

## 🛠️ Tu tarea — entrega estos archivos en esta carpeta

1. **`hallazgos.md`** — las trampas de costo, **ordenadas de mayor a menor impacto en dólares** (no alfabético, no por orden de la tabla). Para cada una: qué driver es (compute / storage / egress / requests), por qué se disparó, y cuánto pesa. Marca explícitamente las que son **gasto cero-valor** (no aportan nada a la app).
2. **`plan-finops.md`** — el control que faltaba:
   - un esquema de **tags** (qué etiquetas pondrías y para qué sirven al leer la próxima factura);
   - un **budget con umbrales de alerta concretos** (monto + a qué % avisar, incluido forecast);
   - la lista de **qué apagar/borrar/redimensionar** y el ahorro estimado de cada acción, **sin romper la app** (ojo: hay cosas que sí sirven).
3. **`estimacion.md`** — la estimación que el colega **debió** hacer antes de desplegar: una tabla `driver → estimación → supuesto`, y el total que habría anticipado. Señala qué supuesto, de haberse escrito, habría encendido la alarma (pista: el egress de PDFs y el "experimento" que no se apaga).

Acompaña cada decisión grande con un **ADR de una línea**: `Decidí X · descarté Y · porque Z`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 3 archivos existen.
- [ ] `hallazgos.md` está **ordenado por impacto en dólares** e identifica el egress, las VMs always-on (incluida la inútil) y el NAT como los grandes; marca el disco huérfano y la 2ª VM como cero-valor.
- [ ] `plan-finops.md` tiene tags con propósito, un budget con **umbrales concretos** (p. ej. alerta al 50/80/100% de un monto), y recortes con ahorro estimado que **no dejan la app sin funcionar**.
- [ ] `estimacion.md` reconstruye una estimación por driver con supuestos explícitos y nombra el supuesto que habría disparado la alarma.
- [ ] Puedes **defender cada recorte sin notas** (check de dominio): qué pasa con la app si lo aplicas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No optimices el storage: son 92 centavos, es ruido. El dinero está en tres sitios y en este orden:
**egress** (servir 1.8 TB de PDFs), **compute encendido** (dos VMs 24/7, y una no hace nada) y el
**NAT** (base fija + procesado, encima del egress). Para el plan: ¿la segunda VM y el disco huérfano
aportan algo? (No → apágalos/bórralos, ahorro inmediato sin riesgo.) ¿La VM principal necesita estar
24/7 para tráfico bajo, o podría ser scale-to-zero? ¿Se puede servir los PDFs por un CDN para no pagar
egress de origen cada vez? El budget no es decorativo: un umbral al 50% habría avisado el día ~5.
Revisa las secciones 4 y 5 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/auditoria-finops.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector evalúa tu **razonamiento, el orden por impacto y la viabilidad de los recortes**, no una
redacción única: un plan distinto pero bien argumentado es válido. La **solución de referencia** vive
en `.ai/soluciones/fase-5/auditoria-finops.md` — no la mires antes de intentarlo de verdad.
