---
ejercicio_id: fase-0/descomponer-problema-cotidiano
fase: fase-0
sub_unidad: "0.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es un problema **abierto**: esto no es "la" respuesta, sino una entrega de nivel `excelente` que sirve de vara para medir las del alumno. Acepta cualquier descomposición sensata distinta.

# Solución de referencia — Descompón un problema cotidiano con las 4 herramientas

## Naturaleza del ejercicio
No hay respuesta única. El corrector evalúa **calidad de razonamiento**, no coincidencia con este texto. Abajo, una entrega modelo para el problema **"preparar y enviar 30 invitaciones de cumpleaños"**, más los criterios para juzgar entregas de los otros dos problemas.

## Entrega modelo (problema: 30 invitaciones)

### 1. Descomposición
- **A.** Definir la lista de los 30 invitados (nombre + canal de contacto).
- **B.** Diseñar/escribir el texto de la invitación. *(independiente de A)*
- **C.** Para cada invitado: personalizar la invitación con su nombre. *(depende de A y B)*
- **D.** Para cada invitado: enviarla por su canal. *(depende de C)*
- **E.** Registrar quién confirmó. *(depende de D)*

**Dependencias reales:** C necesita la lista (A) y el texto (B); no puedes enviar (D) lo que no personalizaste (C); el registro de confirmaciones (E) solo tiene sentido después de enviar (D). A y B son **independientes** entre sí: se pueden hacer en cualquier orden o en paralelo. Detectar esa independencia es señal de buen razonamiento.

### 2. Patrón
- "**Para cada invitado**: personaliza y envía" se repite 30 veces idéntico. Es el patrón *haz lo mismo para cada elemento de una colección* → en código sería un **bucle**. Reconocerlo convierte "30 tareas" en "1 tarea repetida".

### 3. Abstracción (qué ignoro y por qué)
| Detalle ignorado | Por qué no importa |
|---|---|
| El color/diseño gráfico de la invitación | No afecta a *si* la invitación llega ni a *quién* confirma; es estética, no lógica del proceso. |
| El orden en que envío a los 30 | El resultado (todos reciben) es el mismo sin importar el orden. |
| El medio exacto (WhatsApp vs. email) para el plan general | A nivel de algoritmo, "enviar por su canal" basta; el canal concreto es un detalle del paso D, no del diseño. |

### 4. Algoritmo
```text
1. Construir la lista de 30 invitados (nombre + canal).
2. Escribir el texto base de la invitación con un hueco para el nombre.
3. Para cada invitado en la lista:
     a. Crear la invitación reemplazando el hueco por su nombre.
     b. Enviarla por su canal.
     c. Marcar en la lista que fue enviada.
4. Esperar respuestas y marcar cada confirmación.
```

**Casos borde:**
- **Un invitado sin canal de contacto válido** → el algoritmo lo salta, lo anota en una lista de "pendientes de contacto" y sigue con el resto (no se detiene todo por uno).
- **Un invitado responde tarde / no responde** → no bloquea el cierre: tras una fecha límite, los no-confirmados cuentan como "no asisten".

## Cómo juzgar los otros dos problemas
- **Mudanza:** dependencia clave esperada = "no puedes armar cajas del cuarto antes de empaquetar" / "no puedes ordenar en el destino antes de transportar". Patrón = "empaca cada habitación igual". Casos borde reales: una caja excede el peso manejable; un mueble no pasa por la puerta.
- **Menú semanal:** dependencia = "no puedes hacer la lista de compras antes de decidir los platos". Patrón = "para cada día, elige proteína + carbo + verdura". Casos borde reales: un ingrediente no estaba disponible; un día se come fuera.

## Rango de soluciones aceptables
- **Competente:** cualquier descomposición de 4–7 partes con ≥1 dependencia real, un patrón nombrado, 3 detalles ignorados con porqué, algoritmo sin ambigüedad y 2 casos borde plausibles.
- **Excelente:** además detecta una dependencia o independencia *no obvia*, conecta el patrón con "esto sería un bucle", y elige casos borde que de verdad romperían el plan (no de relleno).
- **No penalizar:** una estructura distinta (árbol vs. lista), más o menos subproblemas dentro del rango, o un problema elegido distinto. **Sí** marcar: ausencia de dependencias, abstracción sin justificación, o pasos ambiguos.
