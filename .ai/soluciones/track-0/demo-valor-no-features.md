---
ejercicio_id: track-0/demo-valor-no-features
fase: track-0
sub_unidad: "T0.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de
> **diseño/razonamiento**: el guion de cada alumno será distinto. Lo que se mide es el **criterio de
> traducción** (cero jerga, honestidad de expectativas, manejo del scope creep), no la redacción exacta.

# Solución de referencia — Demo de valor para Marta

## 1. Guion de demo de referencia (cero jerga)

> *"Marta, mira: hoy, cuando alguien de tu equipo necesita un dato de una política o una ficha de
> producto, lo busca a mano en el Drive y tarda entre 15 y 20 minutos —y a veces no lo encuentra. Con
> esto, escribe la pregunta en lenguaje normal, como me la dirías a mí, y en un par de segundos recibe la
> respuesta **con el documento exacto de donde salió**, para que la pueda verificar. Probémoslo con un
> caso real: 'imagina que llega un cliente preguntando por la garantía del producto X'... aquí está la
> respuesta y aquí el link a la política. Lo que antes eran 20 minutos de búsqueda, ahora son segundos, y
> con la fuente a la vista para que confíes en ella."*

Por qué funciona: cero términos técnicos (ni "RAG", ni "embeddings", ni "p95"); abre con el **antes /
después** que Marta vive (15-20 min → segundos); usa un **caso concreto**; y traduce el grounding (cita a
la fuente) a su lenguaje ("para que la puedas verificar / confiar"), que es justo lo que ella mide
(errores por información desactualizada).

## 2. Qué hace / qué NO hace (referencia)

| ✅ Qué SÍ hace | ❌ Qué NO hace (o requiere un humano) |
|---|---|
| Responde preguntas en lenguaje normal sobre la documentación interna (políticas, manuales, fichas). | Puede no estar seguro: en ~1 de cada 8 consultas el dato es débil y conviene que un humano revise. |
| Muestra el documento fuente de cada respuesta, para verificar. | No reemplaza el criterio del equipo: la decisión final la toma la persona. |
| Encuentra la info aunque no uses las palabras exactas del documento. | No sabe de lo que no está en los documentos cargados (ni de cosas posteriores a la última carga). |
| Cuando no tiene base suficiente, dice "no encontré información" en vez de inventar. | No actualiza solo: si cambia una política, hay que volver a cargarla. |

> El "no hace" honesto **suma** confianza: decir "en ~1 de cada 8 casos te avisa que no está seguro y un
> humano mira" presenta el límite como una **salvaguarda**, no como un defecto. Vender perfección es lo
> que quema la relación al primer error.

## 3. Manejo del scope creep (referencia)

**Respuesta a Marta:** *"Me encanta la idea y tiene todo el sentido —pero responder correos
automáticamente es un proyecto distinto, con sus propios riesgos (mandar algo equivocado a un cliente
pesa mucho más que un dato interno mal). Lo dejo anotado como **fase 2** y lo estimamos juntos en cuanto
tengamos este buscador andando y midiendo. Prefiero entregarte bien lo que ya prometimos antes de abrir
un frente nuevo."*

**Cómo lo registro:** lo agrego al backlog/ADR del proyecto como "Fase 2 candidata: respuesta automática
a correos de clientes — pendiente de discovery y estimación; **no** entra en el MVP actual", y lo menciono
en el correo-resumen de la reunión para que quede constancia de qué entra y qué no.

Por qué: **reconocer** (validar la idea) + **acotar** (es fase 2, es otro riesgo) + **registrar** (backlog
+ correo). Ni "sí" reflejo (reventaría el plazo del MVP), ni "no" seco (dañaría la relación).

## 4. Línea de cierre (referencia)

*"Sub-prometer y sobre-entregar protege la relación porque la confianza se construye cumpliendo: si
prometo que la IA 'lo hace todo y nunca falla', el primer error la destruye; si prometo poco y entrego
más, cada entrega suma. Con IA, donde el error es inevitable a veces, ser honesto sobre los límites
**antes** es lo que hace que el cliente siga confiando **después**."*

## Puntos donde el corrector debe mirar
1. **Jerga residual.** Cualquier "RAG / embedding / reranking / vector / p95" en el guion = no tradujo.
2. **Vender perfección.** Si la tabla "no hace" evita el límite real de la IA (el ~13%/alucinación), el
   alumno está sobre-prometiendo.
3. **Scope creep.** Un "sí, de paso lo hago" mete la feature al plazo actual = error. Un "no" seco sin
   alternativa también. Lo correcto es reconocer + acotar + registrar.
4. **Registro.** Si maneja el scope creep solo de palabra, sin dejar constancia, falta la mitad.

## Rango de soluciones aceptables
- Cualquier antes/después es válido mientras hable de **outcome** (tiempo, confianza, errores), no de
  arquitectura, y no use jerga.
- La tabla puede listar "hace/no hace" distintos siempre que **incluya** un límite honesto de la IA
  (puede equivocarse / requiere revisión / no sabe lo que no está cargado).
- La respuesta al scope creep puede mandar la idea a fase 2 **o** pedir más discovery antes de
  comprometerse; lo no válido es aceptarla dentro del MVP o rechazarla en seco.
- Mencionar un número (precisión, % HITL, segundos vs. minutos) es bonus de Excelente, no obligatorio
  para Competente.
- Entregar en inglés suma el bonus del hilo; en español es aceptable.
