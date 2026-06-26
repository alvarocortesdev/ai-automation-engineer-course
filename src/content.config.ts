import { defineCollection } from "astro:content";
import { docsLoader } from "@astrojs/starlight/loaders";
import { docsSchema } from "@astrojs/starlight/schema";

// Content layer de Astro 5+: Starlight provee su propio loader y schema.
export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
};
