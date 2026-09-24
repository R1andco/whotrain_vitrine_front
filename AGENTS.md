# Site vitrine Whotrain

Site statique Astro. Le contenu se modifie dans des fichiers, puis `npm run build` produit `dist/`.

Ne réécris pas le design des pages marketing. Elles sont dans `embeds/` et seront reprises plus tard. Le menu, le pied de page, le blog, les tutos, les pages légales et la bannière sont faits pour être tenus par un agent.

## Commandes

- `npm run dev` — aperçu local
- `npm run build` — vérifie le schéma de contenu et génère `dist/`

Sers `dist/` sur le VPS. L'application métier reste sur `app.whotrain.com`.

## Blog

Un article = un fichier `src/content/blog/<slug>.md`.

Copie `templates/article.md`. Garde ces champs :

- `title`, `description` (environ 160 caractères), `summary` (1 à 2 phrases citables)
- `date` au format `YYYY-MM-DD`
- `author`
- `category` : Formation, Administratif, RH, Office Hours, Tuto, Killing Me Soft Skills, ou une nouvelle catégorie en toutes lettres
- `draft: true` tant que l'article n'est pas publiable
- `cover` et `coverAlt` si une image est dans `public/images/blog/`
- `youtube` : identifiant YouTube seul, seulement si l'article contient une vidéo
- `faq` : liste `{ question, answer }` seulement pour de vraies questions. Elle alimente la page et les données structurées.

Le slug est le nom du fichier, sans `.md`. Pour un article déjà en ligne, ne change pas ce nom : l'URL est `https://whotrain.com/<slug>`.

Le corps suit le modèle : paragraphe autonome, puis `## Contexte`, `## Ce qu'il faut en retenir`, `## En pratique`.

Deux articles historiques sont encore du HTML dans `embeds/` (`embed:` dans le frontmatter). Ne les convertis pas sans demande.

## Vidéos

Un tuto = un fichier `src/content/videos/<slug>.md`, d'après `templates/video.md`.

- `youtubeId` est l'identifiant YouTube, pas l'URL complète.
- `audience` vaut `entreprises`, `intervenants` ou `tous`.
- L'URL publique est `/tutos/<slug>`.

La vidéo n'est pas hébergée ici.

## Pages légales

Fichiers dans `src/content/legal/`. Pour une CGU ou une CGV, modifie le markdown et la date `updated`. Ne invente pas une clause : parte de la version en vigueur.

## Bannière promo

`src/config/banner.json`

- `enabled` : `true` ou `false`
- `text` : le message
- `href` : lien, ou chaîne vide
- `until` : `YYYY-MM-DD` inclus, ou chaîne vide s'il n'y a pas de date de fin

## Faits, SEO, agents

`src/config/site.json` décrit l'organisation, le menu et le pied de page. Une modification ici se retrouve sur le site, sur `/facts.json` et sur `/llms.txt`.

Les prix ne se recopient pas dans `site.json`. La page à citer est `/tarifs` (`embeds/tarifs.html` tant que la page n'est pas réécrite).

`/pour-les-agents` est la page lisible pour un agent tiers. Les robots autorisent les crawlers de réponses (GPTBot, Perplexity, Google-Extended, Claude, Applebot-Extended).

## Images

- Blog : `public/images/blog/`
- Logos du cadre : `public/images/brand/`
- Images des pages embed : `public/images/embeds/`

## À ne pas faire

- Ne pas remettre le site sur le builder Hostinger.
- Ne pas changer les URLs des articles et des pages déjà publiées.
- Ne pas indexer `mon-resultat` : la page de résultat du quiz reste en `noindex`.
