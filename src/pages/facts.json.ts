import type { APIRoute } from 'astro';
import { publishedPosts } from '../lib/content';
import { getCollection } from 'astro:content';
import site from '../config/site.json';

export const GET: APIRoute = async () => {
  const posts = await publishedPosts();
  const videos = await getCollection('videos');
  const body = {
    name: site.name,
    url: site.url,
    description: site.description,
    email: site.email,
    founder: site.founder,
    partner: {
      name: site.partner.name,
      url: site.partner.url,
      qualiopiCategory: site.partner.qualiopi,
      certificate: `${site.url}${site.partner.certificate}`,
    },
    audiences: site.audiences,
    pricingUrl: `${site.url}/tarifs`,
    accounts: site.app,
    pages: [
      { name: 'Accueil', url: `${site.url}/` },
      { name: 'Entreprises', url: `${site.url}/entreprises` },
      { name: 'Intervenants', url: `${site.url}/intervenants` },
      { name: 'Portage Qualiopi', url: `${site.url}/portage-qualiopi` },
      { name: 'Portage salarial', url: `${site.url}/portage-salarial-formateur` },
      { name: 'Pourquoi Whotrain', url: `${site.url}/pourquoi-whotrain` },
      { name: 'Tarifs', url: `${site.url}/tarifs` },
      { name: 'Blog', url: `${site.url}/blog` },
      { name: 'Tutos', url: `${site.url}/tutos` },
      { name: 'W-Club', url: `${site.url}/w-club-ressources` },
    ],
    articles: posts.map((post) => ({
      title: post.data.title,
      url: `${site.url}/${post.id}`,
      date: post.data.date.toISOString().slice(0, 10),
      summary: post.data.summary,
      category: post.data.category,
    })),
    videos: videos.map((video) => ({
      title: video.data.title,
      url: `${site.url}/tutos/${video.id}`,
      youtubeId: video.data.youtubeId,
      audience: video.data.audience,
      summary: video.data.summary,
    })),
  };

  return new Response(JSON.stringify(body, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
