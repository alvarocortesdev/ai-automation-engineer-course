# Ejercicio 4.8 B — ¿Dónde vive cada pieza de estado?

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.8` Estado global (Zustand)
**Ruta:** crítica · **Modalidad:** a mano (razonamiento / diseño) · **Timebox:** 30 min

> **Sin código.** Este ejercicio entrena el **criterio** de arquitectura de estado: la decisión que un revisor senior toma en segundos y que un junior posterga hasta que la app está llena de bugs. Es, en el fondo, un mini-ADR (Architecture Decision Record): decides dónde vive cada dato y **justificas por qué**.

## 🎯 Objetivo

Clasificar 8 piezas de estado de una app real en los **cuatro tipos** (local/`useState`, server state/TanStack Query, URL state, o global de cliente/Zustand) y defender cada decisión en una frase, incluyendo la decisión de **seguridad** sobre un dato sensible.

## 📋 La app: "ChatLab", un cliente de chat con IA

ChatLab es una SPA (Next.js sobre un backend FastAPI de la Fase 3). El usuario inicia sesión, ve sus conversaciones, abre una y chatea con un modelo de IA. Estas son las **8 piezas de estado** que aparecen en la app:

1. **El texto que el usuario está escribiendo** en el input del chat, antes de enviarlo.
2. **La lista de conversaciones del usuario**, que llega del backend desde `GET /api/conversaciones` y se refresca cada cierto tiempo.
3. **El id de la conversación abierta** ahora mismo; la URL es `/chat/abc123` y se puede compartir por link.
4. **El modelo de IA seleccionado** (`claude-haiku`, `gpt-4o-mini`, ...): lo leen el input, la cabecera y el panel de ajustes, y se puede cambiar desde varios sitios.
5. **Si la barra lateral está abierta o cerrada.**
6. **El tema claro/oscuro**, que lo lee toda la app y debe **sobrevivir a una recarga** del navegador.
7. **Los mensajes de la conversación abierta**, que llegan del backend desde `GET /api/conversaciones/:id/mensajes` y se actualizan al enviar uno nuevo.
8. **El token de sesión / API key** del usuario, que autentica cada llamada al backend.

## 🛠️ Tu tarea (en este orden — Primero-Sin-IA, timebox 30 min)

1. Para cada una de las 8 piezas, **decide su tipo** (local / server / URL / global de cliente) y escribe **una frase** de justificación: por qué ahí y no en otro cubo. Recorre la escalera de decisión de la sección 4.1 de la lección.
2. Responde las dos **preguntas trampa** (abajo).
3. Para al menos una pieza **ambigua**, explica el trade-off de tu elección.

Deja tu trabajo en `decision-estado.md` (hay una plantilla en esta carpeta).

### Preguntas trampa

- **T1.** Un compañero propone guardar **la lista de conversaciones (pieza 2)** en un store de Zustand "para tenerla disponible en toda la app". ¿Por qué es mala idea? Nombra el problema concreto que aparece.
- **T2.** ¿Guardarías **el token (pieza 8)** en el store con `persist` a `localStorage`? Justifica tu respuesta **desde la seguridad** y di dónde debería vivir.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las **8 piezas** clasificadas, cada una con su tipo y una justificación de una frase.
- [ ] Identificas la lista de conversaciones (2) y los mensajes (7) como **server state** (no global).
- [ ] Identificas el id de conversación abierta (3) como **URL state**.
- [ ] Respondes **T1** nombrando el problema de las dos fuentes de verdad / reimplementar cache.
- [ ] Respondes **T2** desde seguridad (XSS + `localStorage`) y propones la cookie httpOnly.
- [ ] Explicas el trade-off de al menos una pieza ambigua (típicamente la 5).
- [ ] Puedes **defender tus decisiones sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para cada pieza, pregúntate en orden: (1) ¿vino de una API? → server state (TanStack Query). (2) ¿define
qué pantalla veo / debería sobrevivir un refresh y ser compartible por link? → URL state. (3) ¿lo usa un
solo componente o su hijo directo? → `useState` local. (4) ¿lo comparten muchos componentes lejanos? →
store global (si casi nunca cambia, Context también vale). El token no es "estado de UI": es un secreto, y
eso convierte la pregunta de "dónde lo guardo" en una de seguridad. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/decidir-estado-global/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **razonamiento** (las justificaciones), no solo si pusiste la etiqueta correcta. La **solución de referencia** vive en `.ai/soluciones/fase-4/decidir-estado-global.md` — no la mires antes de intentarlo de verdad.
