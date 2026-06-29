---
ejercicio_id: track-0/pipeline-postulacion-vivo
fase: track-0
sub_unidad: "T0.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Ojo: este ejercicio es de
> **diseño/estrategia**. No existe una única respuesta correcta —los 5 roles serán distintos para cada
> alumno—; esta es una **referencia ejemplar** + el criterio para juzgar otras entregas.

# Solución de referencia — Monta tu pipeline de postulación vivo

## Respuesta canónica (ejemplo de entrega "excelente")

### 1. Reencuadro
> *Postulo este ciclo para **calibrar mi candidatura con datos reales** y no para **que me contraten
> todavía**, porque cada mes que espero "hasta estar listo" es un mes de feedback del mercado que no
> recupero, y prefiero descubrir mis gaps al precio barato de un rechazo anónimo.*

### 2. Definición de stretch (ejemplo)
- **Criterio de % de match:** cuento los requisitos **duros** del aviso (lenguajes, frameworks, años de
  experiencia, nivel de inglés) y marco cuántos cumplo hoy. % = cumplidos / duros totales. Los
  "nice-to-have" no entran en el denominador.
- **Por qué ~50-70%:** por debajo de ~40% me rechazan por todo a la vez (señal falsa, no aprendo un gap
  puntual); por encima de ~80% es un rol seguro (probablemente me vaya bien y no descubra mi gap real).
  En la franja 50-70% cumplo más de la mitad pero faltan piezas **visibles e individualizables** —ahí
  el rechazo señala algo concreto.

### 3. Cinco roles stretch reales (forma esperada, no el contenido)
Cinco avisos **reales** con empresa + link + conteo. Ejemplo de una fila bien hecha:
> **AI Engineer Jr — Acme (GetOnBoard, link).** Cumplo: Python, Git, SQL básico (3). Faltan: Docker,
> "experiencia con LLMs/RAG", inglés B2 (3). **Match ≈ 50%.** → stretch.

### 4. Temario que dio el mercado (ejemplo)
Ordenado por frecuencia entre los 5 avisos:
1. Python (5/5)
2. Docker (4/5)
3. Inglés B2+ (4/5)
4. FastAPI (3/5)
5. Experiencia con LLMs/RAG (3/5)
6. SQL (3/5)

> Lectura: Docker e inglés aparecen en 4/5 y hoy son gaps → candidatos #1 a reordenar el plan.

### 5. Tabla instrumentada (ejemplo)
| Rol | Empresa | Fuente | Fecha | % match | Etapa actual | Gap detectado | Ajuste |
|---|---|---|---|---|---|---|---|
| AI Eng Jr | Acme | GetOnBoard | 2026-03-04 | 50% | Screening | piden Docker | adelantar intro Docker |
| Automation Eng | Beta | LinkedIn | 2026-03-06 | 60% | Rechazo screening | CV no dice "RAG" | reescribir CV (T0.7) |
| Python Dev | Gamma | GetOnBoard | 2026-03-07 | 65% | Respondieron | screening en inglés | practicar EN (T0.1) |
| ... | ... | ... | ... | ... | ... | ... | ... |

### 6. Loop de calibración (ejemplo)
> Reviso el funnel **en agregado** cada 2 semanas, no caso por caso. Si **0 de 5 pasan el screening**,
> el problema está **arriba del funnel** (CV, keywords, posicionamiento), no en mi skill técnico —porque
> nadie evaluó mi código aún—; ajusto CV y keywords (T0.7) antes de tocar el plan técnico. Si paso el
> screening pero caigo en la **técnica**, el problema es un **skill puntual**: tomo el gap que más se
> repite (Docker, RAG) y adelanto esa parte del roadmap. El ciclo vuelve al inicio con 5 roles nuevos.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **El reencuadro es la decisión #1.** Sin "calibrar, no conseguir", el primer silencio hunde al
   alumno. Con él, el silencio es el producto esperado del experimento.
2. **Stretch ~50-70% por diseño de señal.** Rol seguro = poca señal; rol imposible = señal falsa. La
   franja media es la que individualiza el gap.
3. **El mercado es el temario.** Leer 5 ofertas y contar frecuencias produce un syllabus más afilado que
   cualquier roadmap genérico. Es gratis y específico para su nicho.
4. **La tabla mide un funnel, no es una libreta.** La columna `Etapa actual` es la diferencia entre
   "sé a qué postulé" y "sé dónde y por qué se cae mi candidatura".
5. **El loop es agregado y cierra en el plan de estudio.** Se ajusta por lo que se **repite** (señal),
   no por un caso aislado (ruido), y la salida reordena una fase del roadmap. Ese cierre es lo que
   convierte postular temprano en aprendizaje, no en colección de "no".

## Puntos resbalosos (donde el corrector debe mirar)
- **Tabla-libreta** sin columna de etapa → no puede leerse en agregado. Es el error #1.
- **Roles seguros disfrazados de stretch** (cumple ~95% y lo llama stretch) → poca señal.
- **% de match inventado** sin conteo verificable de requisitos cumplidos vs faltantes.
- **Loop caso por caso** ("veré qué pasa con cada uno") en vez de tasa de conversión por etapa.
- **Reencuadro de fachada:** dice "calibrar" pero elige solo roles seguros o trata el rechazo como
  fracaso en el resto del documento (incoherencia).
- **Inglés ignorado** aunque aparezca en los avisos (pierde el bonus de Excelente y el hilo transversal).

## Rango de soluciones aceptables
- Cualquier conjunto de 5 roles reales cuenta, sin importar empresas/títulos, siempre que sean stretch
  con % calculado.
- El loop puede usar otra cadencia (semanal, cada 10 postulaciones) o herramienta (planilla, Notion,
  Teal/Huntr); lo que importa es la **lectura agregada del funnel** que cierra en el plan de estudio.
- La definición de stretch puede usar otro rango defendible (p. ej. 40-70%) si justifica el porqué de
  los bordes con el argumento de señal. Lo que **no** es válido: llamar stretch a un rol seguro o a uno
  imposible, o una tabla sin la etapa del funnel.
