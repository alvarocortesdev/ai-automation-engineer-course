# Diseño — Monolito modular de la plataforma de soporte

> Completa las cuatro partes **a mano y sin IA**. Empieza siempre por "¿de quién son los datos?".
> Regla de oro: ningún módulo lee las tablas de otro; se hablan solo por su API interna.

---

## Parte 1 — Mapa de módulos (ownership de datos + API interna)

Para cada módulo: qué tablas POSEE y qué funciones de API expone a los demás.

### Módulo: <nombre>
- **Datos que posee (tablas):**
- **API interna (funciones que otros llaman):**
  - `modulo.funcion(args) -> retorno`  // qué hace, en términos de dominio

### Módulo: <nombre>
- **Datos que posee (tablas):**
- **API interna:**

<!-- repite por cada módulo: recepcion/tickets, clasificacion, base-de-conocimiento, notificaciones, reportes -->

---

## Parte 2 — Diagrama (Mermaid)

```mermaid
flowchart TB
    %% Dibuja los módulos y las flechas = llamadas a la API interna de otro módulo.
    %% NO dibujes accesos cruzados a tablas: cada módulo toca solo sus propios datos.
```

---

## Parte 3 — ADR: "Monolito modular, no microservicios"

- **Contexto:** (equipo de 5, tráfico parejo, stack único, dominio...)
- **Decisión:**
- **Alternativas consideradas:** (microservicios desde el día 1; big ball of mud)
- **Trade-off honesto — qué RENUNCIO al elegir monolito modular:**
- **Consecuencias / cómo lo mantengo sano:** (regla de ownership, esquema por módulo, etc.)

---

## Parte 4 — Primera costura a extraer

- **Módulo candidato:**
- **Por qué es el más fácil (acoplamiento transaccional con el resto):**
- **Gatillo observable que dispararía la extracción:** (una métrica o evento concreto, no "cuando crezca")
- **Cómo lo extraería sin big-bang:** (1–2 líneas, Strangler Fig)
