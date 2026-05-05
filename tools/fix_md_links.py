#!/usr/bin/env python3
"""
Fix Markdown links that redundantly include the top-level folder name when the source file is inside that same folder.

Example: in `Automocion_V16_Ciber/README.md` a link to
`Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md` will be replaced
with `materiales/00_Guion_intro_30min.md`.

Backups of modified files are written as `file.md.bak`.
"""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

link_re = re.compile(r"(!?\[([^\]]+)\])\(([^)]+)\)")

modified = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if not fn.lower().endswith('.md'):
            continue
        path = os.path.join(dirpath, fn)
        rel = os.path.relpath(path, ROOT)
        parts = rel.split(os.sep)
        if len(parts) < 2:
            # file at repo root: skip transformations
            continue
        topdir = parts[0]
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        changed_flag = [False]
        def repl(m):
            full, label, target = m.group(1), m.group(2), m.group(3)
            # skip images (keep them) - image links start with '![' matched by group 1
            if full.startswith('!'):
                return m.group(0)
            t = target.strip()
            # ignore absolute urls and anchors and mailto
            if not t or t.startswith('#'):
                return m.group(0)
            if '://' in t or t.startswith('mailto:'):
                return m.group(0)
            # remove fragment/query for matching but keep original when replacing
            base = t.split('#',1)[0].split('?',1)[0]
            if base.startswith(topdir + '/'):
                new_base = base[len(topdir)+1:]
                # reconstruct target with fragment/query if present
                suffix = t[len(base):]
                new_target = new_base + suffix
                changed_flag[0] = True
                return f"[{label}]({new_target})"
            return m.group(0)

        new_text = link_re.sub(repl, text)
        if changed_flag[0]:
            bak = path + '.bak'
            # only create backup if not already exists
            if not os.path.exists(bak):
                with open(bak, 'w', encoding='utf-8') as bf:
                    bf.write(text)
            with open(path, 'w', encoding='utf-8') as wf:
                wf.write(new_text)
            modified.append(rel)

print('Modified files:', len(modified))
for m in modified:
    print('-', m)

if not modified:
    print('No changes necessary.')
