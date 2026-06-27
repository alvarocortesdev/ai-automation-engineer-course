---
ejercicio_id: fase-5/auditoria-finops
fase: fase-5
sub_unidad: "5.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una solución de referencia para
> graduar pistas y detectar qué se le escapó, **nunca** para entregarla. Las elecciones admiten
> criterio: un plan distinto bien argumentado (otro umbral, otra forma de servir los PDFs) es válido.

# Solución de referencia — Auditoría FinOps

## 1. `hallazgos.md` (de referencia, ORDENADO por impacto en USD)

| # | Trampa | Driver | USD | Por qué se disparó |
|---|---|---|---|---|
| 1 | Egress de PDFs (1.8 TB) | **Egress** | 153 | Servir 1.700 GB facturables (tras el tramo gratis de 100) × ~0,09. El costo no está en *guardar* los PDFs (0,92), está en *moverlos*. |
| 2 | Dos VMs encendidas 24/7 | **Compute** | 140 | 730 h/mes cada una, pase lo que pase. **Una de las dos (la "de pruebas") no aporta nada**: 70 USD de gasto cero-valor. |
| 3 | NAT Gateway | **Compute/red** | 71 | 33 base fijo (cobra aunque no pase tráfico) + 38 procesado, **encima** del egress. El cargo "¿de dónde salió esto?" clásico. |
| 4 | PostgreSQL managed | Compute | 14 | Legítimo: la app lo necesita. No es trampa, pero entra en el total. |
| 5 | Disco huérfano | Storage | 8 | Quedó de una VM borrada: "detener/borrar la VM" no borró su disco. **Cero-valor.** |
| 6 | Object storage (40 GB) | Storage | 0,92 | Ruido. **No tocar:** optimizarlo es barrer mientras se inunda el sótano. |

**Gasto cero-valor total: 78 USD** (2ª VM 70 + disco huérfano 8) que se eliminan **sin tocar la app**.

## 2. `plan-finops.md` (de referencia)

**Tags** (para que la próxima factura sea legible, no una sopa):

| Tag | Ejemplo | Para qué |
|---|---|---|
| `proyecto` | `resumidor-pdf` | Atribuir gasto a este proyecto vs. otros. |
| `entorno` | `prod` / `pruebas` | Habría delatado de inmediato la 2ª VM tag-eada `pruebas` encendida en producción. |
| `dueño` | `colega` | A quién preguntar antes de apagar algo. |

**Budget + alertas** (el freno que faltaba):
- Budget mensual del proyecto: **USD 50** (la expectativa real era ~20; 50 da margen sin tapar el problema).
- Alertas por **correo al 50%, 80% y 100%** del monto, **más una alerta de forecast** ("vas camino a pasarte").
- Con esto, el cargo de 387 habría disparado la alerta del 50% (USD 25) cerca del **día 5**, no a fin de mes.

**Qué apagar/borrar/redimensionar** (de mayor a menor retorno, sin romper la app):

| Acción | Ahorro/mes | Riesgo | ADR |
|---|---|---|---|
| Apagar/borrar la 2ª VM "de pruebas" | −70 | Ninguno (no la usa nada) | `Decidí borrar la VM de pruebas · descarté dejarla "por si acaso" · porque no sirve a la app y cuesta 70/mes.` |
| Borrar el disco huérfano | −8 | Ninguno (sin dueño) | `Decidí borrar el disco huérfano · descarté conservarlo · porque ninguna VM lo usa.` |
| Servir los PDFs por **CDN** (cachear cerca del usuario) | gran parte de los 153 | Bajo; mejora latencia | `Decidí poner un CDN delante del storage · descarté servir egress de origen · porque pagaba egress completo por cada descarga.` |
| Pasar la VM principal a **scale-to-zero** (contenedor managed) si el tráfico es bajo | parte de los 70 | Cold start | `Decidí scale-to-zero para el backend · descarté VM 24/7 · porque el tráfico es esporádico.` |
| Revisar si el backend **necesita** el NAT (endpoints/gateway endpoints, o IP pública con LB) | hasta 71 | Medio (cambio de red) | `Decidí evaluar quitar el NAT · porque cobra base fija + procesado encima del egress.` |

Quick-wins inmediatos sin riesgo (acciones 1 y 2): **−78 USD desde hoy**.

## 3. `estimacion.md` (de referencia, lo que se DEBIÓ estimar antes)

| Driver | Estimación previa | Supuesto |
|---|---|---|
| Compute (1 VM o scale-to-zero) | ~15–70 | "1 backend; ¿24/7 o scale-to-zero?" |
| PostgreSQL managed | ~14 | "instancia pequeña" |
| Storage (40 GB PDFs) | ~1 | "PDFs guardados, barato" |
| **Egress (servir PDFs)** | **el supuesto crítico** | **"¿cuántos GB sirvo al mes?" 1.8 TB × 0,09 = 153.** Escribir este supuesto habría encendido la alarma sola. |
| LLM (tokens) | a estimar | techo de costo explícito (puente a F6) |

**El supuesto que faltó:** nadie escribió "voy a servir ~1.8 TB de PDFs", ni "voy a dejar una VM de
pruebas encendida". Estimar **obliga** a hacer explícitos esos supuestos; ahí es donde el golpe se ve
venir. Total que se debió anticipar (con la VM de pruebas y sin CDN): ~300+; con CDN y scale-to-zero:
mucho menor. Un budget de 50 con alertas habría avisado en cualquier caso.

## Notas para el corrector

- Lo no negociable: el orden por impacto (egress y compute arriba, storage al fondo) y marcar el
  **gasto cero-valor** (2ª VM + disco huérfano = 78) como quick-win sin riesgo.
- Acepta otros umbrales de budget y otras tácticas de egress (CDN, comprimir PDFs, otra región) si
  están argumentadas.
- Error grave a marcar siempre: atacar el storage de 0,92 o proponer recortes que rompen la app (borrar
  la DB, apagar la VM principal sin alternativa).
- Premiar (excelente) que reconozca "detener ≠ borrar" en el disco huérfano y que conecte el budget con
  el techo de costo del LLM (F6).
