"""Create a reviewed, credential-free handoff of the completed two-prompt pilot."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import zipfile


root = Path(__file__).resolve().parent
comparison = json.loads((root/'analysis/prompt_comparison.json').read_text())
assert all(v['attempts'] == 18 for v in comparison['versions'].values())
dest = root/'milestone-build/fm-handoff'
dest.mkdir(parents=True, exist_ok=True)
entries = []
for version, run_name, evidence_name in [('v1','qwen-pilot','qwen-complete'), ('v2','qwen-format-v2','qwen-format-v2')]:
    src = root/'runs'/run_name
    target = dest/'raw'/version
    shutil.copytree(src,target,dirs_exist_ok=True)
    evidence = root/'evidence'/evidence_name
    audited = {r['sample']:r for r in json.loads((evidence/'reviewed_pilot_audit.json').read_text())['rows']}
    copies = dest/'source'/version
    copies.mkdir(parents=True,exist_ok=True)
    for name,row in audited.items():
        original = evidence/'fence_only_copies'/(name+'.py')
        if original.exists():
            shutil.copy2(original,copies/original.name)
            try:
                tree=ast.parse(original.read_text())
                entry=json.loads((src/(name+'.json')).read_text())['entry_point']
                fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==entry)
                (copies/(name+'.contract.txt')).write_text((ast.get_docstring(fn) or '')+'\n')
            except SyntaxError:
                pass
        entries.append({'sample_id':version+'/'+name,'task_id':row.get('task_id'),
                        'source':str(Path('source')/version/(name+'.py')),
                        'raw_record':str(Path('raw')/version/(name+'.json')),
                        'repository_source':str(Path('ai/evidence')/evidence_name/'fence_only_copies'/(name+'.py')),
                        'repository_raw_record':str(Path('ai/runs')/run_name/(name+'.json')),
                        'strict_extraction_status':row.get('strict_extraction_status'),
                        'normalization':row.get('normalization'),
                        'contract_parser_status':row.get('contract_parser_status'),
                        'implementation_tests_pass':row.get('implementation_tests_pass')})
    # Keep all diagnostic inputs/results without large environment or generated tests.
    diag=dest/'analysis'/version
    diag.mkdir(parents=True,exist_ok=True)
    for filename in ['reviewed_pilot_audit.json','semantic_probes.json']:
        shutil.copy2(evidence/filename,diag/filename)
    shutil.copy2(src/'manifest.json',target/'manifest.json')

(root/'analysis/samples.json').write_text(json.dumps(entries,indent=2)+'\n')
for folder in ['configs','tasks','analysis','data']:
    shutil.copytree(root/folder,dest/folder,dirs_exist_ok=True)
for filename in ['prompt.txt','prompt-format-v2.txt','generate.py','summarize.py',
                 'audit_reviewed_pilot.py','probe_contracts.py','compare_prompts.py',
                 'check_contract_witnesses.py','test_generate.py','README.md','AI_PROGRESS.md','MILESTONE_AI.md',
                 'SPEAKER_NOTES.md','FM_HANDOFF.md']:
    source=root/filename
    if source.exists():shutil.copy2(source,dest/filename)
# Original diagnostic dependencies; never copy ~/.config or any environment file.
shutil.copy2(root/'evidence/qwen-pilot/crosshair-diagnostic-requirements.txt',dest/'diagnostic-requirements.txt')
shutil.copytree(root/'evidence/qwen-pilot/runtime',dest/'runtime',dirs_exist_ok=True)
(dest/'samples.json').write_text(json.dumps(entries,indent=2)+'\n')
(dest/'REPRODUCE.md').write_text('''# Reproduce from this standalone handoff

Run from the extracted `fm-handoff` directory with the supplied diagnostic
dependencies installed in an isolated Python environment. The original project
uses an `ai/` prefix; the standalone handoff commands below use its own layout.
No API key, server access, or new model generation is required.

```
python audit_reviewed_pilot.py --run raw/v1 --output analysis/v1 --dataset data/eval-only-human-eval-pilot.jsonl.gz
python audit_reviewed_pilot.py --run raw/v2 --output analysis/v2 --dataset data/eval-only-human-eval-pilot.jsonl.gz
python probe_contracts.py --audit-directory analysis/v1 --dataset data/eval-only-human-eval-pilot.jsonl.gz
python probe_contracts.py --audit-directory analysis/v2 --dataset data/eval-only-human-eval-pilot.jsonl.gz
python compare_prompts.py --root . --v1-run raw/v1 --v2-run raw/v2 --v1-evidence analysis/v1 --v2-evidence analysis/v2
```

All 36 source modules and six official test bodies were reviewed for this
handoff. This audit is not a sandbox for future unreviewed generations.
The original model request files and contract text remain unchanged.
See `FM_HANDOFF.md` for immediate FM tasks and the `source/` copies.
''')
hashes={str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
(dest/'SHA256SUMS.json').write_text(json.dumps(hashes,indent=2)+'\n')
archive=root/'milestone-output/AI-FM-handoff.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(dest.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(dest.parent))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any(n.endswith('.env') or '/.config/' in n or '/node_modules/' in n for n in z.namelist())
print(json.dumps({'archive':str(archive),'samples':len(entries),'files':len(hashes)},indent=2))
