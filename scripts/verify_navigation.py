#!/usr/bin/env python3
"""Guard against cached page-dependent masthead and font-dependent arrow icons."""
from pathlib import Path
from html.parser import HTMLParser
class Navigation(HTMLParser):
    def __init__(self):
        super().__init__(); self.active=[]; self.icons=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and a.get('aria-current')=='page': self.active.append(a['href'])
        if tag=='svg' and a.get('class')=='direction-icon':
            assert a.get('aria-hidden')=='true' and a.get('focusable')=='false'
            self.icons+=1
expected={'index.html':['/'],'about/index.html':['/about/'],'projects/index.html':['/projects/'],'notes/index.html':['/notes/'],'notes/getting-started/index.html':['/notes/'],'papers/index.html':['/papers/'],'projects/questnote/index.html':['/projects/'],'projects/taste-compare/index.html':['/projects/'],'papers/reasoning-driven-captions/index.html':['/papers/'],'papers/asr-representations-noise-robust-ser/index.html':['/papers/'],'404.html':[]}
for route, active in expected.items():
    text=(Path('_site')/route).read_text(); p=Navigation();p.feed(text)
    assert p.active==active,(route,p.active,active)
    assert '↗' not in text and '→' not in text,(route,'font-dependent arrow remains')
    if route in ['index.html','about/index.html','projects/index.html','notes/index.html']: assert p.icons>0,route
print('PASS: eleven route-specific current-page states; decorative SVG semantics; no font-dependent arrow glyphs')
