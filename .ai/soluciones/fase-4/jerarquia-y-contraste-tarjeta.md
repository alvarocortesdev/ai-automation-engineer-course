---
ejercicio_id: fase-4/jerarquia-y-contraste-tarjeta
fase: fase-4
sub_unidad: "4.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Ejercicio de **diseño**: no hay una
> única respuesta correcta. Esta es una **referencia ejemplar** + el criterio para juzgar otras. Otra
> paleta y otras escalas pueden ser igualmente `excelente` si la jerarquía funciona y el contraste pasa.

# Solución de referencia — Rediseña una tarjeta de IA

## Respuesta canónica (ejemplo de entrega "excelente")

### `estilos.css`

```css
:root {
  /* Escala de espaciado (base 4px) */
  --espacio-1: 0.25rem; /* 4px  */
  --espacio-2: 0.5rem;  /* 8px  */
  --espacio-3: 1rem;    /* 16px */
  --espacio-4: 1.5rem;  /* 24px */

  /* Escala tipográfica (base 16px, razón 1.25) */
  --texto-sm: 0.8rem;   /* ~13px metadata */
  --texto-base: 1rem;   /* 16px cuerpo    */
  --texto-lg: 1.25rem;  /* 20px título    */

  /* Paleta con roles — todos los pares pasan AA */
  --color-fondo: #ffffff;
  --color-texto: #1a1a1a;              /* ~17:1 sobre fondo */
  --color-texto-tenue: #595959;        /* ~7:1  sobre fondo */
  --color-acento: #1d4ed8;             /* ~6.7:1 sobre fondo (>=3 UI) */
  --color-texto-sobre-acento: #ffffff; /* ~6.7:1 sobre acento (>=4.5) */
}

.tarjeta {
  background: var(--color-fondo);
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: var(--espacio-4);
  max-width: 56ch; /* longitud de línea legible */
  display: flex;
  flex-direction: column;
}

.tarjeta__etiqueta {
  font-size: var(--texto-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-texto-tenue);
  margin: 0 0 var(--espacio-1); /* pegada al título: mismo grupo */
}

.tarjeta__titulo {
  font-size: var(--texto-lg);
  font-weight: 700;
  line-height: 1.2;
  color: var(--color-texto);
  margin: 0 0 var(--espacio-3);
}

.tarjeta__cuerpo {
  font-size: var(--texto-base);
  line-height: 1.5;
  color: var(--color-texto);
  margin: 0 0 var(--espacio-4); /* más espacio: nueva zona */
}

.tarjeta__meta {
  font-size: var(--texto-sm);
  color: var(--color-texto-tenue);
  margin: 0 0 var(--espacio-3);
}

.boton {
  align-self: flex-start;
  background: var(--color-acento);
  color: var(--color-texto-sobre-acento);
  border: none;
  border-radius: 6px;
  padding: var(--espacio-2) var(--espacio-3);
  font-size: var(--texto-base);
  font-weight: 600;
  cursor: pointer;
}
```

### `index.html` (esqueleto semántico)

```html
<article class="tarjeta">
  <p class="tarjeta__etiqueta">Acción detectada</p>
  <h3 class="tarjeta__titulo">Renegociar contrato de logística</h3>
  <p class="tarjeta__cuerpo">El análisis del reporte Q3 sugiere renegociar el transporte
    antes de Q1 por una caída de 2 puntos en el margen, concentrada en la región norte.</p>
  <p class="tarjeta__meta">Confianza 0.86 · fuente: reporte-q3.pdf · hace 3 min</p>
  <button class="boton">Aprobar acción</button>
</article>
```

### `decisiones.md` (ejemplo)

> Base de espaciado 4px porque permite ritmo fino sin improvisar números; uso 4/8/16/24 (proximidad:
> 4px entre etiqueta y título, 24px antes y después del cuerpo para separar zonas). Tipografía base 16px,
> razón 1.25 → tres tamaños (13/16/20). Jerarquía: título 20px/700, cuerpo 16px/400, metadata 13px tenue.
> Paleta: fondo blanco, texto #1a1a1a, tenue #595959 (verificado en WebAIM: ~7:1, pasa AA), acento #1d4ed8
> (blanco encima da ~6.7:1). No usé color para el único feedback de estado.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **Las escalas van primero.** Definir espaciado y tipografía como tokens evita el "número al azar". El
   ritmo nace de que todo es múltiplo de una base.
2. **Jerarquía = contraste relativo.** Tres niveles se logran subiendo el principal **y** bajando el
   secundario. La metadata tiene que ser pequeña y tenue a propósito.
3. **Proximidad agrupa.** Menos espacio dentro de un grupo (etiqueta+título), más entre grupos. No hacen
   falta cajas ni líneas.
4. **El contraste tiene piso AA.** "Tenue" es el gris más claro que aún da 4.5:1 (~#767676 sobre blanco es
   el límite). El acento debe ser lo bastante oscuro para texto blanco legible y para distinguirse del
   fondo (3:1).

## Puntos resbalosos (donde el corrector debe mirar)
- **Tenue por debajo de AA:** el alumno deja `--color-texto-tenue` en un gris que el test rechaza, o lo
  ajusta justo al límite sin entender por qué.
- **Test verde pero jerarquía floja:** los colores pasan, pero el squint test no distingue tres niveles
  (típico: metadata del mismo tamaño que el cuerpo).
- **Escala rota:** mete un valor fuera de la base (18px, 13px) entre los tokens.
- **Sin `max-width`:** la tarjeta se estira a todo el ancho disponible.
- **Acento sin función:** el botón no destaca como CTA, o el alumno mete varios acentos.

## Rango de soluciones aceptables
- Cualquier base de espaciado coherente (4px u 8px) y cualquier razón tipográfica (1.2–1.333) cuentan,
  mientras sean **consistentes**.
- Cualquier paleta cuenta si **los cuatro pares pasan** sus umbrales y los roles están bien asignados;
  no tiene que ser azul ni estos hex exactos.
- El HTML puede variar (otros elementos semánticos, otras clases) mientras la jerarquía sea correcta.
- `decisiones.md` puede ser breve; lo que importa es que **justifique** (por qué esta base, esta razón,
  estos colores, y cómo verificó el contraste), no que sea extenso.
