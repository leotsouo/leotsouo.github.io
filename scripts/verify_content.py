#!/usr/bin/env python3
"""Validate collection content and public optional-field/empty-state behavior."""
from pathlib import Path
import subprocess, json
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
# Use the same Ruby/YAML parser as the build, avoiding an extra Python dependency.
ruby='''require 'yaml'; require 'json'; require 'date'; p=ARGV[0]; out={}; %w[profile projects paper_statuses].each{|n| out[n]=YAML.load_file("#{p}/_data/#{n}.yml")}; out['papers']=Dir["#{p}/_papers/*"].map{|f| [f,YAML.safe_load(File.read(f).split(/^---\\s*$/)[1],permitted_classes:[Date,Time])]}; puts JSON.generate(out)'''
data=json.loads(subprocess.check_output([__import__('shutil').which('ruby') or '/workspace/shared/leo-build-tools/ruby/bin/ruby','-e',ruby,str(root)]))
statuses=['待讀','略讀','精讀','已重現']
assert data['paper_statuses']==statuses
for file,paper in data['papers']:
 if paper.get('published') is False: continue
 for field in ['title','authors','year','original_url','status','updated']: assert paper.get(field),(file,field)
 assert paper['status'] in statuses,(file,'unsupported status')
 assert isinstance(paper['authors'],list) and paper['authors'],(file,'authors must be a nonempty list')
 assert str(paper['original_url']).startswith('https://'),(file,'original URL must be HTTPS')
 assert 1900<=int(paper['year'])<=2100,(file,'invalid year')
home=(root/'_site/index.html').read_text()
for project in data['projects']:
 assert project.get('cover') and project['cover'] in home,(project['id'],'missing genuine screenshot cover')
 for step in project.get('flow',[]): assert __import__('html').escape(step) in (root/'_site'/project['detail_url'].strip('/')/'index.html').read_text(),(project['id'],step,'missing project flow in case detail')
 assert (root/'_site'/project['detail_url'].strip('/')/'index.html').is_file()
 for shot in project.get('screenshots',[]):
  assert shot.get('alt') and shot.get('width') and shot.get('height')
  assert (root/shot['path'].lstrip('/')).is_file()
about=(root/'_site/about/index.html').read_text()
if not data['profile'].get('email'): assert 'mailto:' not in about
if not data['profile'].get('cv_url'): assert '履歷 / CV' not in about
if not data['profile'].get('education'): assert 'id="education"' not in about
papers=(root/'_site/papers/index.html').read_text()
if not [p for _,p in data['papers'] if p.get('published') is not False]: assert '目前還沒有公開的論文閱讀紀錄' in papers
assert not (root/'_site/authoring').exists(),'authoring templates leaked into generated site'
assert not (root/'_site/papers/paper-template').exists()
print('PASS: paper schema/statuses; project detail routes; optional contact/CV/education visibility; honest empty state; authoring exclusions')
