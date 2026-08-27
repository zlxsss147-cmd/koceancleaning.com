// Shared helpers for product display & URL generation.
// Used by both the product listing page and the product detail page so that
// every link to a product resolves to the same clean, title-based URL.

export interface ProductTitleData {
  title: string;
  sku?: string;
}

/** Title with the leading SKU/model code stripped (e.g. "EHC011 Chenille Car Wash Glove" -> "Chenille Car Wash Glove"). */
export function cleanProductTitle(data: ProductTitleData): string {
  const { title, sku } = data;
  if (sku && title.toUpperCase().startsWith(sku.toUpperCase())) {
    return title.slice(sku.length).replace(/^[\s\-_:./]+/, '');
  }
  return title;
}

/** URL-safe slug from any text (lowercase, non-alphanumerics become single hyphens). */
export function slugify(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

/** The title-based slug used for a product's detail page URL. */
export function productSlug(data: ProductTitleData): string {
  return slugify(cleanProductTitle(data));
}
