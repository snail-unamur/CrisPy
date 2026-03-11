import ast
from rules.PY001_numpy_array import NumpyArrayRule
from rules.PY002_string_concat_in_loop import StringConcatInLoopRule
from rules.PY003_exessive_global_variable import ExcessiveGlobalRule
from rules.PY006_list_slicing import ListSlicingRule
from rules.PY007_dict_items import DictItemsRule
from rules.PY008_dict_get import DictGetRule


def analyze_code(code: str):
    tree = ast.parse(code)

    rules = [
        NumpyArrayRule(),
        StringConcatInLoopRule(),
        ExcessiveGlobalRule(),
        ListSlicingRule(),
        DictItemsRule(),
        DictGetRule(),
    ]

    diagnostics = []

    for rule in rules:
        rule.visit(tree)
        diagnostics.extend(rule.diagnostics)

    return diagnostics