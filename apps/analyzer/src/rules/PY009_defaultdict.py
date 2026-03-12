import ast
from models.diagnostic import Diagnostic


class DefaultDictRule(ast.NodeVisitor):
    RULE_ID = "PY009"

    def __init__(self):
        self.diagnostics = []

    def visit_For(self, node: ast.For):
        # we look for pattern inside loop body: if x not in d: d[x] = ...
        # followed by AugAssign on same subscript
        for idx, stmt in enumerate(node.body):
            if isinstance(stmt, ast.If):
                test = stmt.test
                if (
                    isinstance(test, ast.Compare)
                    and len(test.ops) == 1
                    and isinstance(test.ops[0], ast.NotIn)
                    and isinstance(test.left, ast.Name)
                    and len(test.comparators) == 1
                    and isinstance(test.comparators[0], ast.Name)
                ):
                    key_name = test.left.id
                    dict_name = test.comparators[0].id
                    # find assignment in body of if
                    assigns_default = False
                    for inner in stmt.body:
                        if (
                            isinstance(inner, ast.Assign)
                            and len(inner.targets) == 1
                            and isinstance(inner.targets[0], ast.Subscript)
                            and isinstance(inner.targets[0].value, ast.Name)
                            and inner.targets[0].value.id == dict_name
                            and isinstance(inner.targets[0].slice, ast.Name)
                            and inner.targets[0].slice.id == key_name
                        ):
                            assigns_default = True
                    # next stmt after the if should be AugAssign to same subscript
                    if assigns_default and idx + 1 < len(node.body):
                        nxt = node.body[idx + 1]
                        if (
                            isinstance(nxt, ast.AugAssign)
                            and isinstance(nxt.target, ast.Subscript)
                            and isinstance(nxt.target.value, ast.Name)
                            and nxt.target.value.id == dict_name
                            and isinstance(nxt.target.slice, ast.Name)
                            and nxt.target.slice.id == key_name
                        ):
                            diagnostic = Diagnostic(
                                rule_id=self.RULE_ID,
                                message=(
                                    "Utilisez `collections.defaultdict()` pour éviter l'initialisation manuelle d'une clé dans une boucle."
                                ),
                                line=stmt.lineno,
                                column=stmt.col_offset,
                                end_line=stmt.end_lineno,  # type: ignore
                                end_column=stmt.end_col_offset,  # type: ignore
                            )
                            self.diagnostics.append(diagnostic)
        self.generic_visit(node)
