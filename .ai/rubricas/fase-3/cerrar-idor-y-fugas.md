---
ejercicio_id: fase-3/cerrar-idor-y-fugas
fase: fase-3
sub_unidad: "3.13"
version: 1
---

# Rúbrica — Cierra el IDOR y la fuga de datos

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `app.py` + `bitacora.md` con
> `test_app.py` en verde. El test prueba que las fallas están cerradas; la `bitacora.md`
> prueba que el alumno entiende **por qué** (404 vs 403, autenticación vs autorización).

## Objetivos evaluados
- **O1** — Cerrar el Broken Access Control (IDOR) con chequeo de propiedad en cada operación (GET, DELETE, listado).
- **O2** — Devolver 404 (no 403) para el recurso ajeno y explicar por qué eso no filtra su existencia.
- **O3** — Evitar la fuga con `response_model` y distinguir autenticación de autorización.

## Criterios y niveles

### C1 — Corrección del control de acceso · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Algún endpoint sigue devolviendo recursos ajenos (200) o el listado muestra notas de otros; varios tests en rojo. |
| **en-progreso** | Cierra el `GET` pero olvida el `DELETE` o el listado; o usa 403 donde el test pide 404. |
| **competente** | Todos los tests en **verde**: 404 en GET/DELETE ajeno (sin borrar), listado acotado, dueño puede leer/borrar. |
| **excelente** | Verde + centraliza el "trae el recurso del usuario o 404" en una dependencia reutilizable, en vez de repetir el `if` en cada endpoint. |

### C2 — Fuga de datos (response_model) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | La respuesta incluye `nota_privada_interna` (devuelve el dict crudo sin `response_model`). |
| **en-progreso** | Agrega `response_model` solo en algún endpoint; otro sigue filtrando. |
| **competente** | `response_model=NotaPublica` en los endpoints que devuelven notas; ni `nota_privada_interna` ni `owner_id` viajan. |
| **excelente** | Explica que el `response_model` es una barrera de seguridad (no solo documentación) y que nunca se devuelve el modelo de DB crudo. |

### C3 — Comprensión demostrada (bitácora) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay bitácora, o no distingue autenticación de autorización. |
| **en-progreso** | Explica una de las tres preguntas; las otras quedan vagas. |
| **competente** | Responde por qué 404 y no 403, por qué el chequeo va en cada operación, y la diferencia auth vs autorización. |
| **excelente** | Conecta el patrón con el capstone (dependencia de autorización) y nota que 403 filtraría la existencia del recurso (vector de enumeración). |

## Errores típicos a marcar
- **Usar 403 en vez de 404** para el recurso ajeno: "pasa" la idea de bloquear, pero filtra que el recurso existe. El test exige 404.
- **Proteger el `GET` y olvidar el `DELETE`** (o el listado): la falla más común; el test lo caza.
- **Devolver el dict crudo sin `response_model`**: filtra `nota_privada_interna`. Validar la entrada no protege la salida.
- **Filtrar el listado en el cliente / frontend** en vez de en el backend: el backend debe devolver solo lo autorizado (un atacante no usa tu frontend).
- **Confundir autenticación con autorización**: el token válido (header presente) no autoriza a ver recursos ajenos.
- (transversal seguridad) no notar que el mismo patrón se centraliza mejor en una dependencia.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución que mete RBAC, scopes OAuth2 o un middleware de policy completo (material de `3.12`/avanzado) para un chequeo de propiedad simple: sobre-ingeniería impropia del nivel.
- `bitacora.md` que repite "es más seguro" sin poder explicar por qué 404 y no 403.
- No sabe decir qué información filtra un 403 ni por qué el chequeo debe repetirse por operación.
- **Verificación sugerida:** pídele que prediga el status si beto pide la nota de ana (debe ser 404) y que explique qué aprendería un atacante si fuese 403.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo del chequeo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Corre `test_idor_get_de_nota_ajena_da_404`. ¿Beto recibe 404 o 200? Si es 200, ¿qué comprueba tu endpoint además de que la nota exista?"
- **Pregunta socrática (nivel 2):** "Tu token dice quién eres. ¿Dónde, en el código, compruebas que ESE recurso es tuyo? ¿Y por qué devolver 404 en vez de 403 le da menos información a un atacante?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Agrega a la condición `or nota['owner_id'] != usuario.id` y lanza 404; repite el chequeo en `DELETE`; filtra el listado por `owner_id`; declara `response_model=NotaPublica`. Repasa 4.2 y 6.2."

## Conexión con el proyecto / capstone
- El capstone exige seguridad aplicada: cada recurso lleva su chequeo de autorización, idealmente en una dependencia reutilizable. Este ejercicio es ese patrón en miniatura, y el `response_model` como barrera anti-fuga es el mismo de `3.8`.
