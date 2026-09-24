#!/usr/bin/env python3
"""Extract published Whotrain embeds, blog posts and legal pages."""

import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "YbNvo1RyN4HNJraO"

EMBEDS = {
    "entreprises": "https://whotrain.com/entreprises",
    "intervenants": "https://whotrain.com/intervenants",
    "portage-qualiopi": "https://whotrain.com/portage-qualiopi",
    "portage-salarial-formateur": "https://whotrain.com/portage-salarial-formateur",
    "pourquoi-whotrain": "https://whotrain.com/pourquoi-whotrain",
    "tarifs": "https://whotrain.com/tarifs",
    "w-club-ressources": "https://whotrain.com/w-club-ressources",
    "accueil": "https://whotrain.com/",
    "guide-financement-opco": "https://whotrain.com/le-guide-complet-du-financement-opco",
    "quatre-profils-de-formateur": "https://whotrain.com/les-quatre-profils-de-formateur",
    "quel-formateur-etes-vous": "https://whotrain.com/quel-formateur-etes-vous",
    "mon-resultat": "https://whotrain.com/mon-resultat",
    "cookies-tableau": "https://whotrain.com/politique-de-cookies",
}

BLOG = [
    "https://whotrain.com/le-guide-complet-du-financement-opco",
    "https://whotrain.com/competences-numeriques-de-vos-salaries-5-questions-cles-a-vous-poser",
    "https://whotrain.com/preferences-vak-confort-ou-efficacite-",
    "https://whotrain.com/upskilling-et-reskilling-les-vrais-enjeux",
    "https://whotrain.com/les-quatre-profils-de-formateur",
    "https://whotrain.com/le-feedback-sandwich-nest-pas-fait-pour-celui-qui-lavale",
    "https://whotrain.com/la-regle-de-mehrabian-ce-que-7-38-55-na-jamais-mesure",
    "https://whotrain.com/connectez-entreprises-et-formateurs-professionnels-avec-whotrain-pour-des-missions-russies",
    "https://whotrain.com/faut-il-partager-les-evaluations-de-competences-avec-lentreprise",
    "https://whotrain.com/redressement-judiciaire-dun-leader-de-la-formation-professionnelle-un-signal-faible-ou-un-signal-dalarme-",
    "https://whotrain.com/tutoriel-pour-linscription-des-intervenants-sur-whotraincom",
    "https://whotrain.com/introduction-a-la-nomenclature-des-formations-cnis",
    "https://whotrain.com/office-hours-whotrain-ce-que-les-formateurs-disent-vraiment-de-lia",
    "https://whotrain.com/les-defis-rh-en-formation-intra-entreprise",
    "https://whotrain.com/on-ne-motive-pas-on-arrete-dempecher",
]

LEGAL = {
    "mentions-legales-whotrain": "https://whotrain.com/mentions-legales-whotrain",
    "accessibilite": "https://whotrain.com/accessibilite",
    "politique-de-confidentialite": "https://whotrain.com/politique-de-confidentialite",
    "politique-de-cookies": "https://whotrain.com/politique-de-cookies",
    "conditions-generales-dutilisation": "https://whotrain.com/conditions-generales-dutilisation",
    "conditions-generales-de-vente": "https://whotrain.com/conditions-generales-de-vente",
}

EMBED_BLOG = {
    "le-guide-complet-du-financement-opco": "guide-financement-opco.html",
    "les-quatre-profils-de-formateur": "quatre-profils-de-formateur.html",
}


class Props(HTMLParser):
    def __init__(self):
        super().__init__()
        self.props = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if self.props is None and "pageData" in data.get("props", ""):
            self.props = data["props"]


def unwrap(value, depth=0):
    if depth > 80:
        return value
    if isinstance(value, list) and len(value) == 2 and isinstance(value[0], int):
        if value[0] == 1 and isinstance(value[1], list):
            return [unwrap(item, depth + 1) for item in value[1]]
        if value[0] == 0:
            return unwrap(value[1], depth + 1)
    if isinstance(value, dict):
        return {key: unwrap(item, depth + 1) for key, item in value.items()}
    if isinstance(value, list):
        return [unwrap(item, depth + 1) for item in value]
    return value


def fetch(url):
    raw = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
        timeout=40,
    ).read().decode("utf-8", "replace")
    parser = Props()
    parser.feed(raw)
    root = unwrap(json.loads(parser.props)["pageData"])
    title_match = re.search(r"<title>(.*?)</title>", raw, re.I | re.S)
    title = ""
    if title_match:
        title = html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
    return root, title


def custom_blocks(root):
    found = []

    def walk(value):
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str) and len(value) > 200 and "<style" in value:
            if any(token in value for token in (":root", "DM Sans", "wt-", "Poppins")):
                found.append(value)

    walk(root)
    return sorted(set(found), key=len, reverse=True)


def yq(value):
    text = re.sub(r"\s+", " ", str(value)).strip()
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def clip(value, limit):
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut + "…"


def html_to_md(source):
    text = re.sub(r"<style[\s\S]*?</style>", "", source, flags=re.I)
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</(p|div|h1|h2|h3|h4|li|tr|blockquote)>", "</\\1>\n", text, flags=re.I)

    def repl_a(match):
        href = html.unescape(match.group(1))
        label = re.sub(r"<[^>]+>", "", match.group(2))
        label = html.unescape(re.sub(r"\s+", " ", label)).strip()
        if not label:
            return href
        return f"[{label}]({href})"

    text = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>', repl_a, text, flags=re.I)
    text = re.sub(r"<h1[^>]*>", "\n# ", text, flags=re.I)
    text = re.sub(r"<h2[^>]*>", "\n## ", text, flags=re.I)
    text = re.sub(r"<h3[^>]*>", "\n### ", text, flags=re.I)
    text = re.sub(r"<h4[^>]*>", "\n#### ", text, flags=re.I)
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.I)
    text = re.sub(r"<(strong|b)[^>]*>", "**", text, flags=re.I)
    text = re.sub(r"</(strong|b)>", "**", text, flags=re.I)
    text = re.sub(r"<(em|i)[^>]*>", "*", text, flags=re.I)
    text = re.sub(r"</(em|i)>", "*", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\r", "")
    lines = [re.sub(r"[ \t]{2,}", " ", line).strip() for line in text.split("\n")]
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def download(path, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 500:
        return
    url = f"https://assets.zyrosite.com/{SITE}/{path}"
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=40,
        ).read()
    except Exception as error:
        print("IMG FAIL", url, error)
        return
    dest.write_bytes(data)
    print("img", dest.name, len(data))


def content_parts(root):
    page = root["pages"][root["currentPageId"]]
    parts = []
    for block_id in page.get("blocks") or []:
        block = root["blocks"].get(block_id)
        if not block or block.get("type") != "BlockLayout":
            continue
        components = []
        for component_id in block.get("components") or []:
            element = root["elements"].get(component_id)
            if not element:
                continue
            top = (element.get("desktop") or {}).get("top") or 0
            components.append((top, element))
        blob = " ".join((element.get("content") or "") for _, element in components)
        if "All rights reserved" in blob or "Organisme de formation partenaire" in blob:
            continue
        components.sort(key=lambda item: item[0])
        for _, element in components:
            kind = element.get("type")
            if kind == "GridTextBox" and element.get("content"):
                parts.append(("html", element["content"]))
            elif kind == "GridImage":
                settings = element.get("settings") or {}
                if settings.get("path"):
                    parts.append(("img", settings.get("alt") or "", settings["path"]))
            elif kind == "GridVideo":
                parts.append(("video", json.dumps(element)[:4000]))
            elif kind == "GridEmbed" and element.get("content"):
                parts.append(("embed", element["content"]))
    return page, parts


def main():
    embed_dir = ROOT / "embeds"
    blog_dir = ROOT / "src" / "content" / "blog"
    legal_dir = ROOT / "src" / "content" / "legal"
    video_dir = ROOT / "src" / "content" / "videos"
    image_dir = ROOT / "public" / "images" / "blog"
    brand_dir = ROOT / "public" / "images" / "brand"
    for directory in (embed_dir, blog_dir, legal_dir, video_dir, image_dir, brand_dir):
        directory.mkdir(parents=True, exist_ok=True)

    for name, url in EMBEDS.items():
        root, _title = fetch(url)
        blocks = custom_blocks(root)
        if not blocks:
            print("NO EMBED", name)
            continue
        (embed_dir / f"{name}.html").write_text(blocks[0].strip() + "\n", encoding="utf-8")
        print("embed", name, len(blocks[0]))

    for url in BLOG:
        root, _title = fetch(url)
        page, parts = content_parts(root)
        categories = root.get("blogCategories") or {}
        names = []
        for category_id in page.get("categories") or []:
            category = categories.get(category_id) or {}
            if isinstance(category, dict) and category.get("name"):
                names.append(category["name"])
        category = names[0] if names else "Formation"
        meta = page.get("meta") or {}
        description = (meta.get("description") or "").strip()
        date = (page.get("date") or "2026-01-01")[:10]
        slug = page["slug"]
        author = (meta.get("authorName") or "Erwan Le Verger").strip()
        name = page.get("name") or slug
        youtube = ""
        markdown_parts = []
        for part in parts:
            if part[0] == "html":
                markdown_parts.append(html_to_md(part[1]))
            elif part[0] == "img":
                alt, path = part[1], part[2]
                extension = Path(path).suffix or ".png"
                download(path, image_dir / f"{slug}{extension}")
                markdown_parts.append(f"![{alt}](/images/blog/{slug}{extension})")
            elif part[0] == "video":
                match = re.search(r"(?:youtu\.be/|embed/|v=)([A-Za-z0-9_-]{6,})", part[1])
                if match:
                    youtube = match.group(1)
        cover_public = ""
        cover = page.get("coverImagePath") or ""
        if cover:
            extension = Path(cover).suffix or ".png"
            download(cover, image_dir / f"{slug}-cover{extension}")
            cover_public = f"/images/blog/{slug}-cover{extension}"
        body = "\n\n".join(part for part in markdown_parts if part.strip())
        body = re.sub(r"^# .+\n+", "", body).strip()
        embed = EMBED_BLOG.get(slug, "")
        draft = len(re.sub(r"\s+", " ", body)) < 400 and not embed and not youtube
        summary = clip(description or body or name, 220)
        description = clip(description or summary, 180)
        lines = [
            "---",
            f"title: {yq(name)}",
            f"description: {yq(description)}",
            f"date: {date}",
            f"author: {yq(author)}",
            f"category: {yq(category)}",
            f"summary: {yq(summary)}",
            f"draft: {'true' if draft else 'false'}",
        ]
        if cover_public:
            lines.append(f"cover: {yq(cover_public)}")
            lines.append(f"coverAlt: {yq(page.get('coverImageAlt') or name)}")
        if youtube:
            lines.append(f"youtube: {yq(youtube)}")
        if embed:
            lines.append(f"embed: {yq(embed)}")
        lines.append("---")
        (blog_dir / f"{slug}.md").write_text("\n".join(lines) + "\n\n" + body + "\n", encoding="utf-8")
        print("blog", slug, category, "draft" if draft else "live", "yt" if youtube else "", "embed" if embed else "")

    for slug, url in LEGAL.items():
        root, title = fetch(url)
        page, parts = content_parts(root)
        chunks = [html_to_md(part[1]) for part in parts if part[0] == "html"]
        body = "\n\n".join(chunk for chunk in chunks if chunk.strip())
        body = re.sub(r"^# .+\n+", "", body).strip()
        if slug == "politique-de-cookies":
            extra = (embed_dir / "cookies-tableau.html").read_text(encoding="utf-8")
            match = re.search(r'(<div class="container">[\s\S]*</div>)\s*$', extra)
            if match and "table" not in body.lower():
                body += "\n\n## Article 3 — Cookies utilisés\n\n" + match.group(1) + "\n"
        name = page.get("name") or title.split("|")[0].strip()
        description = clip(((page.get("meta") or {}).get("description") or name), 180)
        updated = (page.get("date") or "2026-09-23")[:10]
        if not re.match(r"20\d\d-\d\d-\d\d", updated):
            updated = "2026-09-23"
        frontmatter = "\n".join([
            "---",
            f"title: {yq(name)}",
            f"description: {yq(description)}",
            f"updated: {updated}",
            f"summary: {yq(description)}",
            "---",
            "",
        ])
        (legal_dir / f"{slug}.md").write_text(frontmatter + body + "\n", encoding="utf-8")
        print("legal", slug, len(body))

    root, _title = fetch("https://whotrain.com/")
    seen = set()
    for element in root["elements"].values():
        if element.get("type") != "GridImage":
            continue
        path = (element.get("settings") or {}).get("path")
        if path and path not in seen:
            seen.add(path)
            download(path, brand_dir / path)

    video = "\n".join([
        "---",
        'title: "Tutoriel d\'inscription des intervenants"',
        'description: "Créer un compte intervenant sur Whotrain : les étapes d\'inscription, en vidéo."',
        "date: 2026-01-01",
        'youtubeId: "CxUd-JFQW_g"',
        'audience: "intervenants"',
        'summary: "Vidéo pas à pas pour créer un compte formateur, coach ou conférencier sur Whotrain."',
        "---",
        "",
        "Comment créer un compte intervenant sur Whotrain et accéder aux annonces.",
        "",
    ])
    (video_dir / "inscription-intervenants.md").write_text(video, encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
