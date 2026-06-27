# Ejercicio 5.5 — Mapa de primitivos cloud + IAM de mínimo privilegio

> **Modalidad: a mano (de diseño, sin desplegar, sin IA).** Este ejercicio entrena el **criterio**:
> dado un sistema, saber qué primitivo cloud le corresponde a cada pieza y darle a cada una el
> mínimo permiso para su tarea. No se despliega nada: se **decide y se justifica**. Es la parte de
> la nube que una entrevista realmente evalúa.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.5` Cloud troncal
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Mapear cada componente de una app real a su **primitivo cloud** (compute, object storage, base de datos managed, secreto) y justificar el trade-off de cada elección.
- **O2** — Diseñar el acceso de la app con **identidades de mínimo privilegio** (least privilege), corrigiendo una asignación de rol sobre-privilegiada.
- **O3** — Trazar la frontera del **modelo de responsabilidad compartida** para el compute elegido, y justificar **región/zonas**.

## 📋 Contexto

Es el boceto de arquitectura de tu **API de producción** (capstone F3) cuando la lleves a la nube en
el capstone F5. Decidir bien aquí —antes de tocar un comando— es lo que separa "lo subí a clics"
de "diseñé dónde corre cada cosa y con qué permisos". El `iam.md` y el `mapa.md` son insumos
directos de tu capstone de fase.

## El sistema a mapear

Tu **API de producción** tiene:

- un **contenedor** con tu app FastAPI (ya tienes la imagen de la 5.1);
- una base de datos **PostgreSQL** con los datos de usuarios;
- usuarios que **suben su foto de perfil** (archivos);
- una **cadena de conexión** secreta para la base de datos;
- requisito: alcanzable **públicamente** por al menos **3 usuarios reales**.

## 📏 Primero-Sin-IA (en este orden, timebox 40 min)

1. Resuélvelo **solo**, a mano, en archivos markdown. Está bien dudar.
2. Solo entonces, consulta **documentación oficial** (la sección 9 de la lección tiene los enlaces).
3. **Solo al final**, usa IA para *revisar* tu razonamiento —no para generarlo.
4. Mañana, reconstruye el mapa de memoria. Si no puedes, no lo aprendiste todavía.

## 🛠️ Tu tarea — entrega estos archivos en esta carpeta

1. **`mapa.md`** — una tabla `componente → primitivo cloud → justificación (1 frase, incluye qué descartaste)`. Cubre los 4 componentes: compute, fotos, base de datos, secreto.
2. **`iam.md`** — el acceso de **mínimo privilegio** de la app: ¿qué permiso *exacto* necesita y sobre qué recurso? Te dan esta asignación "dejada andando" por un compañero; explica por qué está mal (radio de daño) y reescríbela como mínimo privilegio:
   ```bash
   az role assignment create --assignee "$APP_ID" --role Owner --scope "$SUBSCRIPTION_ID"
   ```
3. **`responsabilidad.md`** — para el modelo de compute que elegiste en `mapa.md`, una tabla con la **frontera de responsabilidad compartida**: "esto lo parcheo/respondo yo" vs. "esto el proveedor" (incluye explícitamente quién parchea el SO).
4. **`region.md`** — un párrafo: qué región eliges y por qué (latencia, residencia de datos, disponibilidad de servicios, costo), y si necesitas **multi-zona** para 3 usuarios. Justifica el "sí" o el "no".

Acompaña cada decisión grande con un **ADR de una línea**: `Decidí X · descarté Y · porque Z`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 4 archivos existen.
- [ ] `mapa.md` cubre los 4 componentes con primitivo **y** justificación con trade-off.
- [ ] `iam.md` nombra el problema del `Owner` (puede borrar/crear todo el daño posible) y propone el permiso **mínimo** real (no otro permiso amplio).
- [ ] `responsabilidad.md` ubica correctamente quién parchea el SO según tu modelo de compute.
- [ ] `region.md` justifica región **y** la decisión de zonas con criterio, no por defecto.
- [ ] Puedes **defender cada elección sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `mapa.md`: las fotos **no** van en el disco del contenedor (es efímero) —piensa qué primitivo
guarda archivos servidos por URL. Para `iam.md`: pregúntate "¿qué es lo *único* que el contenedor
necesita hacer en la nube por sí mismo?" (pista: leer su propia imagen). Para `responsabilidad.md`:
mientras más managed el compute, menos cosas parcheas tú —pero **tus datos y permisos siempre son
tuyos**. Para `region.md`: la región no es solo latencia; hay 3 factores más. Revisa la sección 4 de
la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/mapa-primitivos-cloud.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector evalúa tu **razonamiento y justificaciones**, no una redacción única: una elección
distinta pero bien argumentada es válida. La **solución de referencia** vive en
`.ai/soluciones/fase-5/mapa-primitivos-cloud.md` — no la mires antes de intentarlo de verdad.
