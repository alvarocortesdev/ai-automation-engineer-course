// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import mermaid from "astro-mermaid";

// Base path del project site en GitHub Pages. Fuente ÚNICA de verdad:
// se usa en `base` y en el rehype plugin de abajo. Cambiar aquí los arregla todos.
const SITE_BASE = "/ai-automation-engineer-course";

/**
 * Prefija con SITE_BASE los links internos root-relative (`href="/..."`).
 * Astro NO lo hace solo cuando `base` está configurado, así que sin esto los
 * ~1700 links del contenido dan 404 bajo /ai-automation-engineer-course/.
 * Idempotente y conservador: ignora externos (//), anclas, y los que ya
 * tienen el base. Solo toca `href` (no hay `src` absolutos en el contenido).
 */
function rehypeBasePrefix() {
  const shouldPrefix = (v) =>
    typeof v === "string" &&
    v.startsWith("/") &&
    !v.startsWith("//") &&
    v !== SITE_BASE &&
    !v.startsWith(SITE_BASE + "/");
  const prefix = (v) => (v === "/" ? SITE_BASE + "/" : SITE_BASE + v);
  const walk = (node) => {
    // Links markdown `[](/...)` -> nodos HAST <a> con properties.href
    if (node.type === "element" && node.properties && shouldPrefix(node.properties.href)) {
      node.properties.href = prefix(node.properties.href);
    }
    // Links `<a href="/...">` escritos como JSX en .mdx -> nodos MDX con attributes[]
    if (
      (node.type === "mdxJsxFlowElement" || node.type === "mdxJsxTextElement") &&
      Array.isArray(node.attributes)
    ) {
      for (const attr of node.attributes) {
        if (attr.type === "mdxJsxAttribute" && attr.name === "href" && shouldPrefix(attr.value)) {
          attr.value = prefix(attr.value);
        }
      }
    }
    if (node.children) for (const child of node.children) walk(child);
  };
  return (tree) => walk(tree);
}

// https://astro.build/config
export default defineConfig({
  // GitHub Pages (project site): se sirve bajo /ai-automation-engineer-course/
  site: "https://alvarocortesdev.github.io",
  base: SITE_BASE,
  // Reescribe links internos del contenido para que respeten el base (ver arriba).
  markdown: {
    rehypePlugins: [rehypeBasePrefix],
  },
  integrations: [
    // astro-mermaid debe ir ANTES de starlight: transforma los bloques
    // ```mermaid en diagramas renderizados client-side (sin browser/playwright).
    mermaid({
      theme: "default",
      autoTheme: true, // sigue el data-theme claro/oscuro de Starlight
    }),
    starlight({
      title: "AI / Automation Engineer — de cero a semi-senior",
      description:
        "Curso público autoguiado para llegar de cero real a AI / Automation Engineer semi-senior empleable: fundamentos, lenguajes, ingeniería, backend, frontend, DevOps, AI Engineering, automatización y system design.",
      defaultLocale: "es",
      locales: {
        root: { label: "Español", lang: "es" },
      },
      customCss: ["./src/styles/custom.css"],
      // Starlight 0.39+ exige envolver el autogenerate en `items` cuando el
      // grupo lleva `label`.
      sidebar: [
        {
          label: "Empezar aquí",
          items: [{ autogenerate: { directory: "empezar" } }],
        },
        {
          label: "Track 0 · Empleabilidad e inglés",
          items: [{ autogenerate: { directory: "track-0-empleabilidad" } }],
        },
        {
          label: "Fase 0 · Fundamentos y autonomía",
          items: [{ autogenerate: { directory: "fase-0-fundamentos" } }],
        },
        {
          label: "Fase 1 · Lenguajes núcleo",
          items: [{ autogenerate: { directory: "fase-1-lenguajes" } }],
        },
        {
          label: "Fase 2 · Ingeniería de software",
          items: [{ autogenerate: { directory: "fase-2-ingenieria" } }],
        },
        {
          label: "Fase 3 · Bases de datos y Backend",
          items: [{ autogenerate: { directory: "fase-3-backend" } }],
        },
        {
          label: "Fase 4 · Frontend",
          items: [{ autogenerate: { directory: "fase-4-frontend" } }],
        },
        {
          label: "Fase 5 · DevOps y Cloud",
          items: [{ autogenerate: { directory: "fase-5-devops" } }],
        },
        {
          label: "Fase 6 · AI Engineering ★",
          items: [{ autogenerate: { directory: "fase-6-ai-engineering" } }],
        },
        {
          label: "Fase 7 · Automatización ★",
          items: [{ autogenerate: { directory: "fase-7-automatizacion" } }],
        },
        {
          label: "Fase 8 · System Design",
          items: [{ autogenerate: { directory: "fase-8-system-design" } }],
        },
        {
          label: "Referencia",
          items: [{ autogenerate: { directory: "referencia" } }],
        },
      ],
    }),
  ],
});
