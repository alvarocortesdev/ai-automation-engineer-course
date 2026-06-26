---
ejercicio_id: fase-3/auditoria-owasp-config
fase: fase-3
sub_unidad: "3.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Audita una configuración insegura

> Ejercicio de razonamiento: no hay una única redacción correcta. Esta es la **tabla
> completa** de hallazgos esperados. Una entrega **competente** cubre ≥ 6 con la
> categoría correcta y un fix accionable; una **excelente** los cubre todos + nota que
> SSRF está ausente pero es el riesgo si se añade un fetch saliente.

## Tabla de hallazgos esperada

| # | Hallazgo (línea/qué hace) | OWASP | Severidad | Por qué es riesgo | Fix |
|---|---|---|---|---|---|
| 1 | `FastAPI(debug=True)` | A05 Security Misconfiguration | Media | En producción, los errores exponen stack traces, rutas y versiones internas | `debug=False` (o controlado por env); nunca debug en prod |
| 2 | `allow_origins=["*"]` + `allow_credentials=True` | A05 Security Misconfiguration | **Alta** | Cualquier sitio web puede llamar la API con las credenciales del usuario; la spec CORS prohíbe el combo | Lista **explícita** de orígenes; métodos/headers acotados |
| 3 | `JWT_SECRET`/`DATABASE_URL` hardcodeados y commiteados | A02/A05 (secretos) | **Crítica** | Secreto en el repo = filtrado para siempre en el historial; cualquiera con acceso firma tokens / entra a la DB | Mover a env vars (`pydantic-settings`), `.env` en `.gitignore`, **rotar** lo filtrado, gitleaks en CI |
| 4 | `text(f"... email = '{email}'")` en `/login` | A03 Injection | **Crítica** | Inyección SQL: `email` controla la estructura de la query (bypass de login, dump, DROP) | Parámetro enlazado: `text("... = :email")`, `{"email": email}` o el ORM |
| 5 | `fila.password_hash != password` | A02/A07 (auth débil) | **Alta** | Compara la contraseña en texto plano contra el hash (siempre falla o, peor, sugiere texto plano en DB); sin verificación de hash | Verificar con un hasher (`pwdlib`/`bcrypt`/`argon2`): `verify(password, fila.password_hash)` |
| 6 | `/login` sin límite de intentos | A05/A07 | Media | Fuerza bruta de credenciales sin coste | Rate limiting (slowapi: `@limiter.limit("5/minute")`) |
| 7 | `GET /usuarios/{id}` sin auth ni chequeo de dueño | A01 Broken Access Control | **Crítica** | Cualquiera lee cualquier usuario (problema de **autorización**, ni siquiera hay autenticación) | Exigir usuario autenticado (`Depends`) + comprobar permiso/propiedad; 404 para ajeno |
| 8 | Devuelve la fila CRUDA (incluye `password_hash`) | A01/A02 (fuga de datos) | **Alta** | Expone el hash de contraseña y campos internos al cliente | `response_model` público que excluya `password_hash` y datos internos |
| 9 | Handler `Exception` devuelve `str(exc)` + tipo | A05 Security Misconfiguration | Media | Filtra detalles internos (clase, mensaje, a veces datos) que ayudan a atacar | Loguear el detalle (observabilidad); responder genérico `{"error": "internal_error"}` |
| 10 | **Ausente:** ningún fetch saliente | A10 SSRF | — | Hoy no aplica, pero si se agrega una herramienta que pide URLs (p. ej. un agente de IA), hay que validar el destino | Anotar como riesgo a vigilar; aplicar guardia anti-SSRF cuando exista |

## El peor de todos (justificación esperada)
Empate entre **#3 (secreto hardcodeado)**, **#4 (SQLi)** y **#7 (acceso sin auth)**: los tres dan acceso total a los datos con explotación trivial. Una respuesta defendible prioriza el **secreto en el repo** (compromiso de todo el sistema, ya filtrado e irreversible sin rotación) o la **inyección SQL** (ejecución de SQL arbitrario). Cualquiera de las tres, bien argumentada por impacto×explotabilidad, es válida.

## Secrets management (respuesta esperada)
- **Detección:** `gitleaks git .` (escanea TODO el historial de commits); `gitleaks dir .` para los archivos actuales. En CI, falla el build si encuentra un patrón de secreto.
- **Si ya está en el historial:** borrarlo en un commit nuevo **no** lo elimina (sigue accesible en commits viejos). La acción correcta es **ROTAR** la credencial: generar una nueva, invalidar la vieja. Reescribir el historial (filter-repo/BFG) ayuda, pero se asume que la vieja ya está comprometida.
- **Prevención:** `.env` (en `.gitignore`) + `.env.example` con las claves sin valores + carga con `pydantic-settings` + scanner en el pipeline.

## Cómo calificar la cobertura
- **Competente:** ≥ 6 hallazgos con categoría correcta y fix accionable, incluyendo #2, #3, #4 y #8.
- **Excelente:** detecta #1–#9 y nota la ausencia de SSRF (#10) como pensamiento de superficie de ataque; severidades bien razonadas.
- **Marcar bajo:** menos de 4; clasificación errada (p. ej. CORS como injection); fixes vagos ("hacerlo seguro"); confundir el #7 con un problema de autenticación sin notar que es autorización/acceso; "borrar el secreto" sin rotar.

## Errores de clasificación frecuentes
- CORS (#2) y debug (#1) son **A05**, no A03.
- #7 es **A01** (control de acceso/autorización), no "falta de login" a secas — el punto es que el endpoint no autoriza.
- #8 (fuga de `password_hash`) cuenta como A01/A02; no es injection.
- SSRF (#10) NO está presente en el código — premiar a quien lo note como ausente, no a quien lo "encuentre" donde no está.
