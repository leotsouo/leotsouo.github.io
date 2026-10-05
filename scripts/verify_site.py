#!/usr/bin/env python3
"""Check the built Jekyll site using only Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
DOMAIN = 'leotsouo.github.io'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=set(); self.links=[]; self.resources=[]; self.lang=None; self.title=False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag=='html': self.lang=a.get('lang')
        if tag=='title': self.title=True
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag in ('script','img','iframe','source') and 'src' in a: self.resources.append(a['src'])
        if tag=='link' and a.get('rel') in ('stylesheet','icon','preload'): self.resources.append(a.get('href',''))

assert ROOT.is_dir(), 'Run bundle exec jekyll build first'
pages={p:Page(p.read_text()) for p in ROOT.rglob('*.html')}
errors=[]; checked=0
for p, page in pages.items():
    if page.lang!='zh-TW': errors.append(f'{p}: missing zh-TW language')
    if not page.title: errors.append(f'{p}: missing title')
    for resource in page.resources:
        if urlsplit(resource).netloc: errors.append(f'{p}: external loaded resource {resource}')
    for href in page.links+page.resources:
        u=urlsplit(href)
        if u.scheme not in ('','https','http') or (u.netloc and u.netloc!=DOMAIN): continue
        if not u.path: target=p
        elif u.path.startswith('/'): target=ROOT/unquote(u.path.lstrip('/'))
        else: target=p.parent/unquote(u.path)
        if target.is_dir(): target=target/'index.html'
        checked+=1
        if not target.exists(): errors.append(f'{p.relative_to(ROOT)}: missing {href}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{p.relative_to(ROOT)}: missing anchor {href}')
for expected in ['index.html','about/index.html','projects/index.html','notes/index.html','notes/getting-started/index.html','404.html','sitemap.xml','feed.xml','assets/css/main.css']:
    if not (ROOT/expected).is_file(): errors.append(f'missing route/asset: {expected}')
for private in ['Gemfile','Gemfile.lock','README.md','CONTENT_REVIEW.md','VERIFICATION.md','.git/config','scripts/verify_site.py','reports/DESIGN_AUDIT.md']:
    if (ROOT/private).exists(): errors.append(f'build leaks source/private review file: {private}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; {checked} local links/assets and anchors; routes, metadata, source exclusions; no external loaded resources')
