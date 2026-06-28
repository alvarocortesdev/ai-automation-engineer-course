# Ejercicio 8.3b — Diseña los módulos de un monolito modular (+ ADR + primera costura)

> **Modalidad: a mano (diseño, sin IA).** Diseñas la estructura interna de un monolito modular: quién
> posee qué datos, cómo se hablan los módulos por su API (no por las tablas del vecino), y cuál sería la
> **primera costura** a extraer si el sistema creciera. Es el esqueleto exacto de los diagramas del
> capstone de la fase.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.3` Monolito modular vs microservicios
**Ruta:** opcional / profundización · **Timebox:** 40–45 min

## 🎯 Objetivo

- **O1** — Diseñar los **límites de módulo** de un monolito modular: qué datos posee cada módulo y qué
  funciones de su API interna exponen, sin que nadie lea las tablas de otro.
- **O2** — Defender la elección "monolito modular, no microservicios" en un **ADR** que nombre al menos
  una **renuncia real** (no solo ventajas).
- **O3** — Identificar la **primera costura** a extraer a un servicio y el **gatillo observable** que la
  dispararía, justificándola por su **bajo acoplamiento transaccional**.

## 📋 Contexto

Un monolito modular bien diseñado tiene dos virtudes que un big ball of mud no tiene: ownership claro de
datos y la **opción de extraer servicios después** sin reescribir todo. Este ejercicio entrena diseñar
esos límites y razonar la extracción futura — exactamente lo que el capstone de la Fase 8 (`8.P` Diseña 3
sistemas en papel) te pedirá para tres sistemas, con diagramas y ADRs.

## El sistema a diseñar

Una **plataforma de soporte con tickets**. Funcionalidad:

- **Recepción de tickets:** un cliente abre un ticket (asunto, descripción, prioridad). Se guarda y se le
  asigna un estado.
- **Clasificación:** cada ticket se etiqueta por categoría y se asigna a una cola/agente.
- **Base de conocimiento:** artículos de ayuda; al clasificar, se sugieren artículos relacionados.
- **Notificaciones:** al cliente y al agente cuando cambia el estado del ticket (email/push).
- **Reportes:** métricas agregadas (tickets por día, tiempo de resolución, categorías más frecuentes).

Equipo: **5 personas**. Tráfico: modesto, parejo. Stack único.

## 📏 Primero-Sin-IA

1. Diseña **solo**, a mano, dentro del timebox. Empieza por "¿de quién son los datos?".
2. Solo entonces consulta la lección (secciones 4.1, 4.5 y la práctica 6.3).
3. **Solo al final**, usa IA para *revisar* tu diseño — no para *generarlo*.
4. Mañana, redibuja el mapa de módulos de memoria.

## 🛠️ Instrucciones

Produce un único `diseno.md` (hay plantilla en este directorio) con **cuatro partes**:

1. **Mapa de módulos.** Lista los módulos y, para **cada uno**: qué **datos posee** (sus tablas) y **una o
   dos funciones** de su API interna que otros módulos llamarían (en vez de leer sus tablas).
2. **Diagrama Mermaid.** Un `flowchart` del monolito modular mostrando los módulos y **quién llama a la
   API de quién** (las flechas son llamadas a API internas, no accesos cruzados a datos).
3. **ADR corto** titulado "Monolito modular, no microservicios", con: contexto, decisión, alternativas
   consideradas, y un **trade-off honesto** que nombre qué **renuncias** al elegir monolito.
4. **Primera costura.** Qué módulo extraerías **primero** a un servicio si el sistema creciera, **qué
   evento/métrica** dispararía esa extracción, y por qué ese módulo es el candidato más fácil.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **Cada** módulo declara qué **datos posee**; el diseño establece explícitamente que ningún módulo
      lee las tablas de otro (solo su API).
- [ ] Cada módulo expone **al menos una función de API interna** con nombre de dominio (no un getter de
      tablas).
- [ ] El **diagrama Mermaid renderiza** y sus flechas representan **llamadas entre APIs**, no accesos
      cruzados a datos.
- [ ] El **ADR** nombra al menos **una renuncia real** del monolito modular (escala independiente,
      aislamiento de fallas, despliegue independiente), no solo sus ventajas.
- [ ] La **primera costura** justifica el candidato por su **bajo acoplamiento transaccional** con el
      resto y define un **gatillo observable** (no "cuando sea grande").
- [ ] Puedes **explicar el diseño sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-8/monolito-vs-microservicios-diseno/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará el **ownership de datos**, la **calidad de las APIs internas** (nombres de dominio
vs getters de tablas), la **honestidad del ADR** y el **razonamiento** de la primera costura — no una
solución única.
