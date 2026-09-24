import { getCollection, type CollectionEntry } from 'astro:content';

export function isPublicPost(entry: CollectionEntry<'blog'>) {
  return !entry.data.draft;
}

export async function publishedPosts() {
  const posts = await getCollection('blog');
  return posts.filter(isPublicPost).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export function readingMinutes(text: string) {
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}

export function isoDate(date: Date) {
  return date.toISOString().slice(0, 10);
}

export function formatDate(date: Date) {
  return new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }).format(date);
}
