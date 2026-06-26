# Decisiones de diseño (mini-ADRs)

> Un **ADR** (Architecture Decision Record) es una nota corta que captura *una*
> decisión: el contexto, la opción elegida y por qué. No es burocracia: es lo que
> te deja entender, en seis meses, por qué tu yo del pasado hizo lo que hizo.
> Escribe **al menos dos**. Borra este bloque y el ejemplo al completar.

---

## ADR-001 — (título de la decisión, ej.: "Persistir en un archivo JSON")

- **Fecha:** YYYY-MM-DD
- **Contexto:** (¿qué problema te obligó a decidir? ¿qué opciones tenías?)
- **Decisión:** (qué elegiste)
- **Consecuencias:** (qué ganas, qué pierdes, qué se complica más adelante)

---

## ADR-002 — (ej.: "Validar con pydantic/zod en vez de ifs a mano")

- **Fecha:** YYYY-MM-DD
- **Contexto:** (…)
- **Decisión:** (…)
- **Consecuencias:** (…)

---

<!--
Ejemplo de referencia (borra al usar):

## ADR-000 — Separar PantryStore (dominio) de la capa HTTP
- Fecha: 2026-06-26
- Contexto: necesito testear la lógica de la despensa sin levantar un servidor ni
  tocar la red. Si mezclo HTTP y lógica, los tests se vuelven lentos y frágiles.
- Decisión: PantryStore no sabe nada de HTTP; recibe un path de archivo y expone
  add/list/get/remove. El servidor solo traduce HTTP <-> métodos del store.
- Consecuencias: + tests rápidos con archivo temporal; + reusable desde una CLI;
  - una capa más de indirección. Trade-off claramente a favor.
-->
