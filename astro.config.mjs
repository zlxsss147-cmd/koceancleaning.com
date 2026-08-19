import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://koceancleaning.com',
  compressHTML: true,
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
});
