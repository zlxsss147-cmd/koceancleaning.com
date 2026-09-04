// Shared blog category helpers for the Knowledge Hub filter bar.

export const BLOG_CATEGORIES = [
  'Nonwoven Materials',
  'Buying Guides',
  'Applications',
  'OEM & Quality',
  'Industry & Sustainability',
] as const;

export function categorySlug(category: string): string {
  return category
    .toLowerCase()
    .replace(/\s+&\s+/g, '-')
    .replace(/\s+/g, '-');
}

export function categoryFromSlug(slug: string): string | undefined {
  return BLOG_CATEGORIES.find((c) => categorySlug(c) === slug);
}
