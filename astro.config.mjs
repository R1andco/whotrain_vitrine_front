import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://whotrain.com',
  trailingSlash: 'never',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/mon-resultat'),
    }),
  ],
});
