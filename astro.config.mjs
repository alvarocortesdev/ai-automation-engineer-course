// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import mermaid from "astro-mermaid";

// https://astro.build/config
export default defineConfig({
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
