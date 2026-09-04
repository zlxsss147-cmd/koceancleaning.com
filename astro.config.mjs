import { defineConfig } from 'astro/config';
import { readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

// Inline integration: generate sitemap.xml + sitemap-index.xml from the built
// static output after the build finishes. No third-party dependency.
function generateSitemap(dir) {
  const SITE = 'https://koceancleaning.com';
  const pages = [];
  const walk = (rel) => {
    const abs = join(dir, rel);
    for (const name of readdirSync(abs)) {
      const p = join(rel, name);
      const full = join(dir, p);
      if (statSync(full).isDirectory()) {
        walk(p);
      } else if (name === 'index.html') {
        // dir/index.html -> /dir/
        const relDir = rel.split(sep).join('/');
        pages.push(relDir === '' ? '/' : `/${relDir}/`);
      } else if (name.endsWith('.html')) {
        const relNoExt = p.slice(0, -'.html'.length).split(sep).join('/');
        pages.push(`/${relNoExt}/`);
      }
    }
  };
  walk('');

  const now = new Date().toISOString().split('T')[0];
  const urls = [...new Set(pages)]
    .filter((path) => !path.endsWith('/404/'))
    .sort()
    .map(
      (path) =>
        `  <url>\n    <loc>${SITE}${path === '/' ? '' : path}</loc>\n    <lastmod>${now}</lastmod>\n  </url>`
    )
    .join('\n');

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${urls}\n</urlset>\n`;

  const index = `<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <sitemap>\n    <loc>${SITE}/sitemap.xml</loc>\n    <lastmod>${now}</lastmod>\n  </sitemap>\n</sitemapindex>\n`;

  writeFileSync(join(dir, 'sitemap.xml'), sitemap, 'utf8');
  writeFileSync(join(dir, 'sitemap-index.xml'), index, 'utf8');
  console.log(`[sitemap] wrote ${pages.length} URLs (sitemap.xml + sitemap-index.xml)`);
}

// https://astro.build/config
export default defineConfig({
  site: 'https://koceancleaning.com',
  compressHTML: true,
  output: 'static',
  integrations: [
    {
      name: 'static-sitemap',
      hooks: {
        'astro:build:done': ({ dir }) => {
          generateSitemap(fileURLToPath(dir));
        },
      },
    },
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
});
