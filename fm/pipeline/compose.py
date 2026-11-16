"""Contract extraction and injection.

A *contract* is the docstring of the target function in a contract module
(PEP 316 ``pre:`` / ``post:`` blocks) plus that module's other top-level code
(imports and helper functions). An *implementation* is any module defining the
target function. ``compose`` copies the contract docstring verbatim (raw source
text, not a re-rendered string) into the implementation, replacing its own
docstring, and prepends the contract helpers. The implementation's code is not
otherwise changed.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


class ComposeError(Exception):
    pass


@dataclass
class Contract:
    contract_id: str
    task_id: str
    entry_point: str
    source_path: str
    docstring_src: str          # raw source literal, quotes included
    doc_indent: int             # body indentation in the contract module
    helpers_src: str            # other top-level code from the contract module
    helper_names: list[str]
    provenance: dict = field(default_factory=dict)


def _target(tree: ast.Module, name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    raise ComposeError(f"no top-level function {name!r}")


def _docstring_node(fn: ast.FunctionDef) -> ast.Expr | None:
    first = fn.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
            and isinstance(first.value.value, str):
        return first
    return None


def _is_main_guard(node: ast.stmt) -> bool:
    return isinstance(node, ast.If) and ast.unparse(node.test).replace('"', "'") == "__name__ == '__main__'"


def _stmt_lines(src_lines: list[str], node: ast.stmt) -> str:
    start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])])
    return ''.join(src_lines[start - 1:node.end_lineno])


def _defined_names(node: ast.stmt) -> list[str]:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return [node.name]
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return [n.id for t in targets for n in ast.walk(t) if isinstance(n, ast.Name)]
    return []


def load_contract(path: str | Path, entry_point: str, contract_id: str, task_id: str,
                  provenance: dict | None = None) -> Contract:
    src = Path(path).read_text(encoding='utf-8')
    tree = ast.parse(src)
    fn = _target(tree, entry_point)
    doc = _docstring_node(fn)
    if doc is None:
        raise ComposeError(f"{path}: {entry_point} has no docstring")
    lines = src.splitlines(keepends=True)
    helpers, names = [], []
    for node in tree.body:
        if node is fn or _is_main_guard(node):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue  # module docstring / bare string
        helpers.append(_stmt_lines(lines, node))
        names += _defined_names(node)
    return Contract(contract_id=contract_id, task_id=task_id, entry_point=entry_point,
                    source_path=str(path), docstring_src=ast.get_source_segment(src, doc.value),
                    doc_indent=fn.body[0].col_offset, helpers_src=''.join(helpers),
                    helper_names=names, provenance=provenance or {})


def _reindent(literal: str, old: int, new: int) -> str:
    if old == new:
        return literal
    out = [literal.splitlines()[0]]
    for line in literal.splitlines()[1:]:
        if line[:old].strip() == '':
            out.append(' ' * new + line[old:] if line.strip() else '')
        else:
            out.append(line)
    return '\n'.join(out)


def compose(impl_path: str | Path, contract: Contract) -> str:
    """Return module source: header + contract helpers + implementation with contract docstring."""
    src = Path(impl_path).read_text(encoding='utf-8')
    tree = ast.parse(src)
    fn = _target(tree, contract.entry_point)
    impl_names = {n for node in tree.body if node is not fn for n in _defined_names(node)}
    clash = impl_names & set(contract.helper_names)
    if clash:
        raise ComposeError(f"contract helper names also defined by implementation: {sorted(clash)}")
    lines = src.splitlines(keepends=True)
    body_indent = fn.body[0].col_offset
    new_doc = ' ' * body_indent + _reindent(contract.docstring_src, contract.doc_indent, body_indent) + '\n'
    doc = _docstring_node(fn)
    if doc is not None:
        if doc.lineno == fn.lineno or len(fn.body) > 1 and fn.body[1].lineno == doc.end_lineno:
            raise ComposeError('docstring shares a line with other code')
        lines[doc.lineno - 1:doc.end_lineno] = [new_doc]
    else:
        if fn.body[0].lineno == fn.lineno:
            raise ComposeError('one-line function body')
        lines.insert(fn.body[0].lineno - 1, new_doc)
    header = (f"# Composed by fm/pipeline. contract={contract.contract_id} "
              f"(from {Path(contract.source_path).as_posix()}), implementation={Path(impl_path).as_posix()}\n"
              "# The docstring below is copied verbatim from the contract source.\n")
    helpers = ''
    if contract.helpers_src.strip():
        helpers = '# --- contract helpers ---\n' + contract.helpers_src.rstrip() + '\n# --- implementation ---\n'
    return header + helpers + ''.join(lines)
