import ast
from rules.PY001_numpy_array import NumpyArrayRule
from rules.PY002_string_concat_in_loop import StringConcatInLoopRule


def analyze_code(code: str):
    tree = ast.parse(code)

    rules = [
        NumpyArrayRule(),
        StringConcatInLoopRule(),
    ]

    diagnostics = []

    for rule in rules:
        rule.visit(tree)
        diagnostics.extend(rule.diagnostics)

    return diagnostics