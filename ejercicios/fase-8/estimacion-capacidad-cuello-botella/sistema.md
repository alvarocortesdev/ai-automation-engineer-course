# Sistema a analizar — Servicio de comentarios de un medio digital

> Este es el **input** del ejercicio. No lo edites: analízalo en `capacidad.md`.

Un diario digital tiene un servicio de comentarios donde los lectores leen y escriben comentarios
bajo cada noticia. Estos son los datos que te dieron (todo lo que sabes; lo demás lo estimas tú con
supuestos declarados).

## Números de producto

- **Usuarios registrados:** 4.000.000
- **Usuarios activos al día (DAU):** ~5% de los registrados
- **Uso por usuario activo y día:**
  - lee ~**80** hilos de comentarios (1 request cada uno)
  - publica ~**2** comentarios (1 request cada uno)
- **Objetivo de latencia:** p99 menor que 250 ms
- **Evento viral:** cuando una noticia explota, el tráfico del servicio se multiplica
  aproximadamente **×6** durante un par de horas.

## Arquitectura actual

- **1 load balancer** (capa 7) al frente.
- **2 servidores de app** stateless detrás del LB. Cada uno: 4 núcleos. Cada request consume, en
  promedio, **~40 ms** de trabajo de CPU en un núcleo.
- **1 base de datos PostgreSQL primaria**. **Sin réplicas. Sin caché.** Tanto las lecturas como las
  escrituras pegan a esta primaria.
- **Connection pool** de la app a Postgres: **30 conexiones** en total (entre los dos servidores).

## Lo que ya pasó una vez

La última noticia viral tumbó el servicio: los comentarios dejaron de cargar, aparecían errores 500
intermitentes, y el equipo "reinició todo" sin entender qué se había saturado. Quieren un análisis
para que no vuelva a pasar.
