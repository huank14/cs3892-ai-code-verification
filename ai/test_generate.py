"""Integration checks for sample retention, resume, provenance, and failed outputs."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import tempfile
from threading import Thread
from types import SimpleNamespace
import unittest

from generate import extract, run
from summarize import summarize


class RunnerTest(unittest.TestCase):
    def test_retention_resume_errors_and_definition_change(self):
        calls = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                calls.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                if len(calls) == 3:
                    self.send_response(429)
                    self.end_headers()
                    self.wfile.write(b'{"error":"rate_limit"}')
                    return
                text = ('```python\ndef f(x: int) -> int:\n'
                        '    """post: __return__ == x"""\n    return x\n```') if len(calls) == 1 else 'invalid response'
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'model': 'fixture', 'choices': [{'message': {'content': text}, 'finish_reason': 'stop'}]}).encode())

        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root/'config.json').write_text(json.dumps({'model': 'fixture', 'base_url': f'http://127.0.0.1:{server.server_port}/v1'}))
                (root/'tasks.jsonl').write_text(json.dumps({'task_id': 'HumanEval/0', 'entry_point': 'f', 'prompt': 'test'})+'\n')
                (root/'prompt.txt').write_text('{task_prompt}')
                args = SimpleNamespace(config=root/'config.json', tasks=root/'tasks.jsonl', prompt=root/'prompt.txt',
                                       output=root/'out', repetitions=3, timeout=2)
                run(args)
                run(args)
                self.assertEqual(len(calls), 3)
                stats = summarize(root/'out')
                self.assertEqual(stats['attempts'], 3)
                self.assertEqual(stats['extraction_status'], {'extracted': 1, 'format_error': 1, 'no_response': 1})
                self.assertTrue((root/'out/HumanEval_0_3.error.txt').exists())
                self.assertTrue((root/'out/HumanEval_0_1.py').exists())
                (root/'prompt.txt').write_text('Changed {task_prompt}')
                with self.assertRaises(SystemExit):
                    run(args)
        finally:
            server.shutdown()
            server.server_close()

    def test_invalid_code_and_missing_contract(self):
        self.assertEqual(extract('```python\ndef f(:\n```', 'f')[0]['status'], 'syntax_error')
        self.assertEqual(extract('```python\ndef f():\n    return 1\n```', 'f')[0]['status'], 'missing_postcondition')


if __name__ == '__main__':
    unittest.main()
