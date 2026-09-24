import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    author: z.string().default('Erwan Le Verger'),
    category: z.string(),
    summary: z.string(),
    draft: z.boolean().default(false),
    cover: z.string().optional(),
    coverAlt: z.string().optional(),
    youtube: z.string().optional(),
    embed: z.string().optional(),
    faq: z.array(z.object({ question: z.string(), answer: z.string() })).default([]),
  }),
});

const legal = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/legal' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    updated: z.coerce.date(),
    summary: z.string(),
  }),
});

const videos = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/videos' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    youtubeId: z.string().regex(/^[A-Za-z0-9_-]{6,}$/),
    audience: z.enum(['entreprises', 'intervenants', 'tous']),
    summary: z.string(),
  }),
});

export const collections = { blog, legal, videos };
