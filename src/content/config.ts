// Content collections for blog posts and products
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    category: z.enum([
      'Nonwoven Materials',
      'Buying Guides',
      'Applications',
      'OEM & Quality',
      'Industry & Sustainability',
    ]),
    tags: z.array(z.string()).optional(),
    draft: z.boolean().default(false),
  }),
});

const products = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum([
      'microfiber-cleaning',
      'mops',
      'sponges',
      'car-cleaning',
      'nonwovens',
      'wet-wipes',
      'home-series',
    ]),
    sku: z.string(),
    itemNo: z.string().optional(),
    material: z.string().optional(),
    size: z.string().optional(),
    weight: z.string().optional(),
    packing: z.string().optional(),
    images: z.array(z.string()).default([]),
    features: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { blog, products };
