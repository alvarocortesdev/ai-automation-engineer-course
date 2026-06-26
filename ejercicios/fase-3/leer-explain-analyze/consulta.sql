-- La query lenta a diagnosticar.
-- Tabla `pedidos` con ~1.500.000 filas. Buscamos los pedidos pendientes
-- de un cliente, del más nuevo al más antiguo.
-- La gran mayoría de los pedidos NO están 'pendiente' (ya se entregaron).

SELECT id, cliente_id, total, creado_en
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY creado_en DESC
LIMIT 20;
