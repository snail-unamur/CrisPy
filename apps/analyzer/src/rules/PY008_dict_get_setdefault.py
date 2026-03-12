import ast
from models.diagnostic import Diagnostic


class DictGetSetdefaultRule(ast.NodeVisitor):
    RULE_ID = "PY008"

    def __init__(self):
        self.diagnostics = []

    def visit_If(self, node: ast.If):
        # detections of pattern: if key in d: val = d[key] else: val = default
        # or if key not in d: d[key] = default; ...
        # we'll warn only for membership followed by lookup in both branches
        test = node.test
        if (
            isinstance(test, ast.Compare)
            and len(test.ops) == 1
            and isinstance(test.ops[0], (ast.In, ast.NotIn))
            and isinstance(test.left, ast.Name)
            and len(test.comparators) == 1
            and isinstance(test.comparators[0], ast.Name)
        ):
            key_name = test.left.id
            dict_name = test.comparators[0].id
            # search for subscript usage inside both branches
            class Finder(ast.NodeVisitor):
                def __init__(self, dict_name, key_name):
                    self.dict_name = dict_name
                    self.key_name = key_name
                    self.found_lookup = False

                def visit_Subscript(self, sub: ast.Subscript):
                    if (
                        isinstance(sub.value, ast.Name)
                        and sub.value.id == self.dict_name
                        and isinstance(sub.slice, ast.Name)
                        and sub.slice.id == self.key_name
                    ):
                        self.found_lookup = True
                    self.generic_visit(sub)

            finder = Finder(dict_name, key_name)
            for stmt in node.body + node.orelse:
                finder.visit(stmt)

            if finder.found_lookup:
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Utilisez `dict.get()` ou `dict.setdefault()` plutôt qu'une vérification ``if key in dict`` suivie d'un accès."
                    ),
                    line=node.lineno,
                    column=node.col_offset,
                    end_line=node.end_lineno,  # type: ignore
                    end_column=node.end_col_offset,  # type: ignore
                )
                self.diagnostics.append(diagnostic)

        self.generic_visit(node)
