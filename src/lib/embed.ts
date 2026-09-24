import fs from 'node:fs';
import path from 'node:path';

export interface EmbedPart {
  links: string;
  styles: string;
  body: string;
  scripts: string[];
}

export function loadEmbed(file: string): EmbedPart {
  const raw = fs.readFileSync(path.join(process.cwd(), 'embeds', file), 'utf8');
  const links = [...raw.matchAll(/<link\b[^>]*>/gi)].map((match) => match[0]).join('\n');
  const styles = [...raw.matchAll(/<style\b[^>]*>[\s\S]*?<\/style>/gi)].map((match) => match[0]).join('\n');
  const scripts = [...raw.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map((match) => match[1]);
  const bodyMatch = raw.match(/<body\b[^>]*>([\s\S]*)<\/body>/i);
  let body = bodyMatch ? bodyMatch[1] : raw;
  body = body
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<link\b[^>]*>/gi, '')
    .replace(/<meta\b[^>]*>/gi, '')
    .replace(/<title\b[^>]*>[\s\S]*?<\/title>/gi, '');
  return { links, styles, body, scripts };
}
