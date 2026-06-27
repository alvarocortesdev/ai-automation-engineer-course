/**
 * Ejercicio 4.9 A — Reconstruye el motor de variantes (mini-cva).
 *
 * Implementa `variants(config)`: una versión mínima de lo que hace
 * `class-variance-authority` por debajo. Devuelve una FUNCIÓN que, dadas unas
 * props, retorna el string de clases correcto.
 *
 * Reglas del ejercicio:
 *   - La clase `base` aparece SIEMPRE y va PRIMERO.
 *   - Por cada eje de `variants`, usa la opción que indican las props; si la
 *     prop no viene (undefined) o trae una opción inexistente, cae al
 *     `defaultVariants` de ese eje.
 *   - Los ejes se concatenan en el ORDEN en que están declarados en `variants`.
 *   - El resultado son clases separadas por UN SOLO espacio, sin espacios extra
 *     al inicio/fin y sin `undefined` colado.
 *
 * No cambies las firmas exportadas: el corrector y los tests importan `variants`
 * (y opcionalmente los tipos).
 */

// Cada eje (p. ej. "variant", "size") mapea nombre-de-opción -> clases.
export type VariantDefs = Record<string, Record<string, string>>;

export interface VariantsConfig {
  base?: string;
  variants?: VariantDefs;
  defaultVariants?: Record<string, string>;
}

// Props al invocar: por cada eje, la opción elegida (o nada).
export type VariantProps = Record<string, string | undefined>;

export function variants(
  config: VariantsConfig,
): (props?: VariantProps) => string {
  // TODO: implementa el motor.
  //  1. Parte de un arreglo con la `base`.
  //  2. Recorre los ejes de `config.variants` (en orden).
  //  3. Para cada eje, elige la opción de props o, si no sirve, la de defaultVariants.
  //  4. Si esa opción existe en el eje, empuja sus clases.
  //  5. Devuelve el arreglo unido con " ", descartando vacíos (filter(Boolean)).
  return (_props = {}) => {
    return config.base ?? "";
  };
}
