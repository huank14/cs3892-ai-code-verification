"""Stdlib-only generation runner. Never executes model-generated Python."""
import argparse
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def write_json(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def extract(content, entry_point):
    blocks = re.findall(r'```(?:python|py)?\s*\n(.*?)```', content, re.S)
    if len(blocks) != 1:
        return {'status': 'format_error', 'detail': 'expected exactly one code block'}, None
    code = blocks[0]
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {'status': 'syntax_error', 'detail': str(e)}, code
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == entry_point]
    if len(functions) != 1:
        return {'status': 'missing_target'}, code
    doc = ast.get_docstring(functions[0]) or ''
    pre = re.findall(r'^\s*pre\s*:\s*(.*)', doc, re.M)
    post = re.findall(r'^\s*post(?:\[[^\]]*\])?\s*:\s*(.*)', doc, re.M)
    return {'status': 'extracted' if post else 'missing_postcondition',
            'preconditions': pre, 'postconditions': post,
            'note': 'AST extraction only; not execution, semantic validation, or CrossHair compatibility'}, code


def run(args):
    config = json.loads(Path(args.config).read_text())
    tasks = [json.loads(l) for l in Path(args.tasks).read_text().splitlines() if l.strip()]
    template = Path(args.prompt).read_text()
    key_env = config.get('api_key_env')
    key = os.environ.get(key_env, '') if key_env else ''
    if key_env and not key:
        raise SystemExit(f'Missing environment variable {key_env}; no requests made')
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {'config': config, 'tasks': tasks, 'prompt_template': template,
                'repetitions': args.repetitions, 'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    fingerprint = digest(manifest)
    manifest_path = out / 'manifest.json'
    if manifest_path.exists():
        if json.loads(manifest_path.read_text())['fingerprint'] != fingerprint:
            raise SystemExit('Run definition changed: use a different output directory')
    else:
        write_json(manifest_path, {'fingerprint': fingerprint, **manifest})
    for task in tasks:
        for repeat in range(args.repetitions):
            name = task['task_id'].replace('/', '_') + f'_{repeat + 1}'
            record_path = out / (name + '.json')
            if record_path.exists():
                continue  # Includes failures: never silently resample unsuccessful responses.
            prompt = template.replace('{task_prompt}', task['prompt'])
            payload = {'model': config['model'], 'messages': [{'role': 'user', 'content': prompt}],
                       'stream': False, **config.get('request_parameters', {})}
            headers = {'Content-Type': 'application/json'}
            if key:
                headers['Authorization'] = 'Bearer ' + key
            request = urllib.request.Request(config['base_url'].rstrip('/') + '/chat/completions',
                                             data=json.dumps(payload).encode(), headers=headers)
            start = time.monotonic()
            record = {'task_id': task['task_id'], 'entry_point': task['entry_point'],
                      'repeat': repeat + 1, 'fingerprint': fingerprint, 'request': payload,
                      'started_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
            try:
                with urllib.request.urlopen(request, timeout=args.timeout) as response:
                    raw = response.read()
                (out / (name + '.response.json')).write_bytes(raw)
                result = json.loads(raw)
                choice = result['choices'][0]
                content = choice['message'].get('content') or ''
                (out / (name + '.txt')).write_text(content)
                parsed, code = extract(content, task['entry_point'])
                record.update(response_model=result.get('model'), usage=result.get('usage'),
                              finish_reason=choice.get('finish_reason'), extraction=parsed,
                              status='response_received')
                if code is not None:
                    (out / (name + '.py')).write_text(code)
            except urllib.error.HTTPError as e:
                # Preserve API error body; credentials and request headers are never written.
                (out / (name + '.error.txt')).write_bytes(e.read())
                record.update(status='http_error', http_status=e.code)
            except Exception as e:
                record.update(status='request_or_response_error', error_type=type(e).__name__)
            record['elapsed_seconds'] = round(time.monotonic() - start, 3)
            write_json(record_path, record)
            print(name, record['status'], record.get('extraction', {}).get('status', ''), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True)
    p.add_argument('--tasks', default='ai/tasks/pilot.jsonl')
    p.add_argument('--prompt', default='ai/prompt.txt')
    p.add_argument('--output', required=True)
    p.add_argument('--repetitions', type=int, default=3)
    p.add_argument('--timeout', type=float, default=300)
    run(p.parse_args())
