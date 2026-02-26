import ast
from models.diagnostic import Diagnostic

class NumpyArrayRule(ast.NodeVisitor):
    RULE_ID = "PY001"

    def __init__(self):
        self.diagnostics = []

    def visit_List(self, node: ast.List):
        if all(
            isinstance(el, ast.Constant) and isinstance(el.value, (int, float))
            for el in node.elts
        ):
            diagnostic = Diagnostic(
                rule_id=self.RULE_ID,
                message="Envisagez d'utiliser un tableau NumPy plutôt qu'une liste Python pour les opérations numériques.",
                line=node.lineno,
                column=node.col_offset,
                end_line=node.end_lineno,
                end_column=node.end_col_offset
            )

            self.diagnostics.append(diagnostic)

        self.generic_visit(node)
