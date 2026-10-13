import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { publishedPosts } from '../lib/content';
import site from '../config/site.json';

export const GET: APIRoute = async () => {
  const posts = await publishedPosts();
  const videos = await getCollection('videos');
  const lines = [
    `# ${site.name}`,
    '',
    `> ${site.description}`,
    '',
    'Les prix en vigueur sont uniquement sur https://whotrain.com/tarifs.',
    `Contact : ${site.email}. Fondateur : ${site.founder.name}.`,
    `Organisme de formation partenaire : ${site.partner.name} (${site.partner.url}), certification Qualiopi pour les ${site.partner.qualiopi.toLowerCase()}. Certificat : ${site.url}${site.partner.certificate}.`,
    '',
    '## Pages',
    `- [Accueil](${site.url}/): promesse et fonctionnement.`,
    `- [Entreprises](${site.url}/entreprises): publier un besoin et trouver un formateur.`,
    `- [Intervenants](${site.url}/intervenants): formateurs, coachs et conférenciers.`,
    `- [Former d'autres entreprises](${site.url}/portage-qualiopi): vendre une expertise interne sans créer d'organisme de formation.`,
    `- [Société de portage](${site.url}/portage-salarial-formateur): ajouter la formation à une offre de portage.`,
    `- [Pourquoi Whotrain](${site.url}/pourquoi-whotrain): origine et équipe.`,
    `- [Tarifs](${site.url}/tarifs): prix entreprises et commission intervenants.`,
    `- [Blog](${site.url}/blog): articles, dans Ressources.`,
    `- [Tutos](${site.url}/tutos): vidéos YouTube, dans Ressources.`,
    `- [W-Club](${site.url}/w-club-ressources): communauté et échanges, dans Ressources.`,
    `- [Pour les agents](${site.url}/pour-les-agents): faits citables.`,
    `- [Faits JSON](${site.url}/facts.json): même information, structurée.`,
    '',
    '## Articles',
    ...posts.map((post) => `- [${post.data.title}](${site.url}/${post.id}): ${post.data.summary}`),
    '',
    '## Vidéos',
    ...videos.map((video) => `- [${video.data.title}](${site.url}/tutos/${video.id}): ${video.data.summary}`),
    '',
  ];

  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
