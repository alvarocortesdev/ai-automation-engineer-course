# Ejercicio 3.13c — Audita una configuración insegura (mapéala a OWASP)

> **Modalidad: a mano (razonamiento y diseño, sin IA, sin código que correr).** Entrena la mirada que un revisor senior aplica a un PR: leer un arranque de backend y detectar, nombrar y priorizar las fallas de seguridad antes de que lleguen a producción. No escribes código: escribes una auditoría que cualquiera podría accionar.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.13` OWASP Top 10 web hands-on
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Auditar `config_vulnerable.py` (un FastAPI plagado de errores reales) y producir `auditoria.md` que demuestre que sabes (1) **detectar** cada falla, (2) **clasificarla** en su categoría del OWASP Top 10, (3) **explicar** el riesgo, y (4) **proponer** un fix concreto. Sin esta mirada, "sé de seguridad" se queda en teoría: el valor está en cazar el bug en código ajeno.

## 📋 Contexto

El archivo "funciona" en una demo feliz. Pero combina varias de las fallas más comunes: CORS comodín con credenciales, modo debug en producción, secretos commiteados, inyección SQL, fuga de datos en la respuesta, un IDOR sin auth, ausencia de rate limit y un handler que filtra el detalle de los errores. Tu trabajo es separarlas, nombrarlas con su código OWASP (A01, A03, A05, A10…) y proponer la corrección. Es exactamente lo que harías en un code review de seguridad.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Lee el archivo línea a línea antes de escribir.
2. Solo entonces, consulta la **documentación oficial** (OWASP Top 10 2021; FastAPI: *CORS*, *Security*) y la lección (secciones 4.2 a 4.8) para validar tu clasificación.
3. **Solo al final**, usa IA para *revisar* tu auditoría — no para generarla.
4. Mañana, lista de memoria las categorías OWASP que cubriste y un fix de cada una.

## 🛠️ Qué entregar (deja este archivo en esta carpeta)

### `auditoria.md`

1. **Tabla de hallazgos** con **al menos 6** filas distintas. Columnas:

   | # | Hallazgo (qué línea/qué hace) | Categoría OWASP | Severidad | Por qué es un riesgo | Fix concreto |
   |---|---|---|---|---|---|

2. **Autenticación vs autorización:** señala explícitamente, en al menos un hallazgo, dónde el problema es de **autorización** (falta chequeo de dueño/permiso) y no de autenticación.
3. **Secrets management (sección aparte):** ¿qué comando de `gitleaks` correrías para detectar los secretos? Y si el escáner confirma que el secreto ya está en el **historial** de Git, ¿cuál es la acción correcta (no basta con borrarlo en un commit nuevo)?
4. **El peor de todos (1 línea):** elige el hallazgo más grave y justifica por qué lo pones primero.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla tiene **≥ 6** hallazgos distintos, cada uno con su categoría OWASP correcta y un fix accionable.
- [ ] Identificaste el CORS comodín + credenciales, la inyección por f-string, el secreto hardcodeado y la fuga de `password_hash`.
- [ ] Distinguiste autenticación de autorización en al menos un hallazgo.
- [ ] La sección de secrets management nombra el comando de gitleaks y la necesidad de **rotar** el secreto filtrado.
- [ ] Puedes defender **sin notas** por qué `allow_origins=["*"]` con `allow_credentials=True` es peor que cualquiera de los dos por separado.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- Hay al menos 8 problemas; los numeré con comentarios `(1)`…`(8)` en el archivo para que no se te escape ninguno.
- Mapa rápido: CORS comodín + credenciales → **A05**; f-string en SQL → **A03**; secreto hardcodeado → **A02/A05**; debug en prod y handler que filtra el error → **A05**; devolver `password_hash` → fuga de datos (**A01/A02**); `GET /usuarios/{id}` sin auth → **A01** (autorización); sin rate limit en login → **A05/A07** (fuerza bruta). El SSRF (**A10**) NO aparece aquí: anótalo como "ausente, pero a vigilar si se agrega un fetch saliente".
- `gitleaks git .` escanea el historial. Si el secreto ya está commiteado: **rótalo** (genera uno nuevo, invalida el viejo); borrarlo en un commit nuevo no lo saca del historial.

Repasa las secciones 4.2 a 4.8 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `auditoria.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/auditoria-owasp-config.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/auditoria-owasp-config.md` — no la mires antes de intentarlo.
