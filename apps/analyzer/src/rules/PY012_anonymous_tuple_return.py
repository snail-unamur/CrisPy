import ast
from models.diagnostic import Diagnostic


class AnonymousTupleReturnRule(ast.NodeVisitor):
    RULE_ID = "PY012"

    def __init__(self):
        self.diagnostics = []

    def visit_Return(self, node: ast.Return):
        if isinstance(node.value, ast.Tuple) and len(node.value.elts) >= 2:
            diagnostic = Diagnostic(
                rule_id=self.RULE_ID,
                message=(
                    "Évitez de retourner un tuple anonyme pour plusieurs valeurs. "
                    "Préférez namedtuple ou dataclass pour nommer les champs."
                ),
                line=node.lineno,
                column=node.col_offset,
                end_line=node.end_lineno,
                end_column=node.end_col_offset,
            )
            self.diagnostics.append(diagnostic)

        self.generic_visit(node)