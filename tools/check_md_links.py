#!/usr/bin/env python3
"""
Recorre el repo y comprueba enlaces Markdown relativos.
Genera reports/broken_links_report.md y lo imprime por pantalla.
"""
import os, re, sys
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MD_GLOB = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.lower().endswith('.md'):
            MD_GLOB.append(os.path.join(dirpath, fn))

link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

broken = []
notes = []

for md in sorted(MD_GLOB):
    rel_md = os.path.relpath(md, ROOT)
    try:
        with open(md, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        notes.append((rel_md, f'ERROR reading file: {e}'))
        continue
    for m in link_re.finditer(text):
        text_label, target = m.groups()
        target = target.strip()
        # ignore images like ![alt](path)? Our regex catches them too; skip if prefixed with '!' before [
        # crude check: see char before match
        start = m.start()
        if start>0 and text[start-1] == '!':
            continue
        # ignore external URLs and anchors and mailto and absolute urls
        if target.startswith('#'):
            continue
        parsed = urlparse(target)
        if parsed.scheme in ('http', 'https', 'mailto'):
            continue
        # remove anchor fragment
        target_path = target.split('#',1)[0]
        # remove query
        target_path = target_path.split('?',1)[0]
        if not target_path:
            continue
        # handle absolute paths starting with '/'
        if target_path.startswith('/'):
            cand = os.path.join(ROOT, target_path.lstrip('/'))
        else:
            cand = os.path.normpath(os.path.join(os.path.dirname(md), target_path))
        exists = os.path.exists(cand)
        if not exists:
            broken.append({
                'source': rel_md,
                'label': text_label,
                'target': target,
                'resolved': os.path.relpath(cand, ROOT),
            })

# write report
os.makedirs(os.path.join(ROOT, 'reports'), exist_ok=True)
report_path = os.path.join(ROOT, 'reports', 'broken_links_report.md')
with open(report_path, 'w', encoding='utf-8') as out:
    out.write('# Broken links report\n\n')
    out.write(f'Repository root: {ROOT}\n\n')
    out.write(f'Total markdown files scanned: {len(MD_GLOB)}\n\n')
    out.write(f'Total broken links found: {len(broken)}\n\n')
    if broken:
        out.write('## Details\n\n')
        for b in broken:
            out.write(f"- Source: `{b['source']}`  \n  Link text: `{b['label']}`  \n  Target: `{b['target']}`  \n  Resolved path: `{b['resolved']}`  \n\n")
    else:
        out.write('No broken links detected.\n')
    if notes:
        out.write('\n## Notes\n\n')
        for n in notes:
            out.write(f'- {n[0]}: {n[1]}\n')

print('Scanned', len(MD_GLOB), 'markdown files')
print('Broken links found:', len(broken))
print('Report saved to', report_path)
if broken:
    print('\nSample broken links:')
    for b in broken[:20]:
        print('-', b['source'], '->', b['target'], '(resolved', b['resolved'] + ')')

sys.exit(0)
