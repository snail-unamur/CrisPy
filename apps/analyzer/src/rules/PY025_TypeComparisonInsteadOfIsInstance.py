import ast
from models.diagnostic import Diagnostic


class IsInstanceRule(ast.NodeVisitor):
    RULE_ID = "PY025"

    def __init__(self):
        self.diagnostics = []

    def visit_Compare(self, node: ast.Compare):
        left = node.left

        if isinstance(left, ast.Call):
            if isinstance(left.func, ast.Name) and left.func.id == "type":
                for op in node.ops:
                    if isinstance(op, (ast.Is, ast.IsNot, ast.Eq, ast.NotEq)):
                        diagnostic = Diagnostic(
                            rule_id=self.RULE_ID,
                            message=(
                                "Comparaison de type avec 'type(...)' détectée. "
                                "Préférez 'isinstance(...)' pour une vérification "
                                "plus pythonique et compatible avec l'héritage."
                            ),
                            line=node.lineno,
                            column=node.col_offset,
                            end_line=node.end_lineno,
                            end_column=node.end_col_offset
                        )

                        self.diagnostics.append(diagnostic)
                        break

        self.generic_visit(node)