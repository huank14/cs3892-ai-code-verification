"""Run from fm/: .venv/Scripts/python -m unittest discover -s pipeline/tests -t ."""
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from pipeline.compose import ComposeError, compose, load_contract
from pipeline.crosshair_run import classify, run_check
from pipeline.run_matrix import WORKER, verdict

CONTRACT = textwrap.dedent('''\
    def _spec_is_max(r, a, b):
        return r in (a, b) and r >= a and r >= b

    def biggest(a: int, b: int) -> int:
        """
        Return the larger argument.

        pre: a >= 0 and b >= 0
        post: _spec_is_max(__return__, a, b)
        """
        raise NotImplementedError
    ''')
WRONG = textwrap.dedent('''\
    def biggest(a: int, b: int) -> int:
        """Original docstring that must be replaced."""
        return a + b
    ''')
RIGHT_NO_DOC = textwrap.dedent('''\
    def biggest(a: int, b: int) -> int:
        return a if a >= b else b
    ''')


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name, src in (('contract.py', CONTRACT), ('wrong.py', WRONG), ('right.py', RIGHT_NO_DOC)):
            (self.tmp / name).write_text(src)
        self.c = load_contract(self.tmp / 'contract.py', 'biggest', 'human', 'toy')

    def worker(self, *args):
        p = subprocess.run([sys.executable, '-I', str(WORKER), *map(str, args)], capture_output=True, text=True)
        return json.loads(p.stdout)

    def test_compose_copies_docstring_verbatim_and_helpers(self):
        out = compose(self.tmp / 'wrong.py', self.c)
        self.assertIn(self.c.docstring_src, out)
        self.assertNotIn('Original docstring', out)
        self.assertIn('def _spec_is_max', out)
        self.assertIn('return a + b', out)

    def test_compose_inserts_docstring_when_missing(self):
        self.assertIn('post: _spec_is_max', compose(self.tmp / 'right.py', self.c))

    def test_helper_name_clash_is_an_error(self):
        (self.tmp / 'clash.py').write_text(WRONG + '\ndef _spec_is_max():\n    pass\n')
        with self.assertRaises(ComposeError):
            compose(self.tmp / 'clash.py', self.c)

    def test_classify_messages(self):
        self.assertEqual(classify('Confirmed over all paths.')['status'], 'confirmed')
        self.assertEqual(classify('Not confirmed.')['status'], 'not_confirmed')
        cex = classify("false when calling f([0, 'a b'], x=1) (which returns (0, 0))")
        self.assertEqual((cex['status'], cex['call'], cex['crosshair_return']),
                         ('counterexample', "f([0, 'a b'], x=1)", '(0, 0)'))
        exc = classify('IndexError: list index out of range when calling f([])')
        self.assertEqual((exc['status'], exc['call']), ('exception', 'f([])'))

    def test_end_to_end_wrong_impl_is_rejected_and_replayed(self):
        mod = self.tmp / 'composed_wrong.py'
        mod.write_text(compose(self.tmp / 'wrong.py', self.c))
        conds = self.worker('conditions', mod, 'biggest')
        self.assertTrue(conds['ok'])
        ch = run_check(mod, 10)
        cex = [r for r in ch['reports'] if r['status'] == 'counterexample']
        self.assertTrue(cex, ch['stdout'])
        rp = self.worker('replay', mod, 'biggest', cex[0]['call'])
        self.assertTrue(rp['pre_holds'] and rp['violated_lines'])
        v, _ = verdict(conds, ch, [{'report': cex[0], 'replay': rp, 'confirmed': True}])
        self.assertEqual(v, 'REJECTED')

    def test_end_to_end_right_impl_is_not_rejected(self):
        mod = self.tmp / 'composed_right.py'
        mod.write_text(compose(self.tmp / 'right.py', self.c))
        conds = self.worker('conditions', mod, 'biggest')
        v, _ = verdict(conds, run_check(mod, 10), [])
        self.assertIn(v, ('ACCEPTED_PROVEN', 'INCONCLUSIVE'))


if __name__ == '__main__':
    unittest.main()
