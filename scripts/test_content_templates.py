#!/usr/bin/env python3
"""Render synthetic content in an isolated temporary source, never the public build."""
from pathlib import Path
import os, shutil, subprocess, tempfile
root=Path(__file__).resolve().parents[1]
env=os.environ.copy()
if not shutil.which('bundle'): env['PATH']='/workspace/shared/leo-build-tools/ruby/bin:'+env['PATH']
with tempfile.TemporaryDirectory(prefix='leo-content-fixture-') as tmp:
 source=Path(tmp)/'source'; dest=Path(tmp)/'build'
 shutil.copytree(root,source,ignore=shutil.ignore_patterns('.git','_site','.sass-cache'))
 (source/'_papers').mkdir(exist_ok=True)
 for i,status in enumerate(['待讀','略讀','精讀','已重現']):
  (source/'_papers'/f'fixture-{i}.md').write_text(f'''---
title: "Synthetic fixture {i}"
authors: ["Fixture Author"]
year: 2020
venue: "Fixture Venue"
original_url: "https://example.com/paper-{i}"
status: {status}
updated: 2027-01-01
tags: ["Fixture Tag"]
excerpt: "Synthetic template test only"
---
## 方法與損失函數

Fixture understanding, never a real reading record.
''')
 (source/'_data/profile.yml').write_text('''links:
  - label: Fixture Profile
    url: https://example.com/profile
email: test@example.com
cv_url: /fixture-cv.pdf
education:
  - school: Fixture School
    degree: Fixture Degree
    period: Fixture Period
''')
 subprocess.run(['bundle','exec','jekyll','build','--strict_front_matter','--source',str(source),'--destination',str(dest)],cwd=source,env=env,check=True,stdout=subprocess.DEVNULL)
 index=(dest/'papers/index.html').read_text()
 assert '目前還沒有公開的論文閱讀紀錄' not in index
 assert 'Synthetic fixture' in (dest/'index.html').read_text(),'home reading link must fall back to full title when display_title absent'
 for i,status in enumerate(['待讀','略讀','精讀','已重現']):
  assert f'href="#status-{i+1}"' in index
  detail=(dest/'papers'/f'fixture-{i}'/'index.html').read_text()
  for expected in [status,'Fixture Author','Fixture Venue','Fixture Tag','方法與損失函數',f'https://example.com/paper-{i}','aria-current="page"']:
   assert expected in detail,expected
 about=(dest/'about/index.html').read_text()
 for expected in ['mailto:test@example.com','/fixture-cv.pdf','Fixture School','Fixture Degree','Fixture Period']: assert expected in about,expected
 assert not (dest/'authoring').exists()
 print('PASS: isolated fixture builds all four reading states, metadata/body, and approved optional profile fields; no fixtures written to production source')

 # Missing content is an actual tested state, not a source-string assertion.
 for p in (source/'_papers').glob('*.md'): p.unlink()
 for p in (source/'_posts').glob('*.md'): p.unlink()
 (source/'_data/profile.yml').write_text('links: []\nemail:\ncv_url:\neducation: []\n')
 subprocess.run(['bundle','exec','jekyll','build','--strict_front_matter','--source',str(source),'--destination',str(dest)],cwd=source,env=env,check=True,stdout=subprocess.DEVNULL)
 empty=(dest/'papers/index.html').read_text()
 assert '目前還沒有公開的論文閱讀紀錄' in empty
 assert '筆記還在整理中' in (dest/'notes/index.html').read_text()
 for route in ['index.html','about/index.html']:
  html=(dest/route).read_text()
  assert 'mailto:' not in html and 'Fixture School' not in html
 assert '回到首頁' in (dest/'404.html').read_text()
 print('PASS: empty paper/note collections; omitted private/unknown profile fields; recovery page')
