import ast
from models.diagnostic import Diagnostic


class NestedLoopRule(ast.NodeVisitor):
    RULE_ID = "PY019"

    def __init__(self):
        self.diagnostics = []

    def visit_For(self, node: ast.For):
        self._check_nested_loop(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._check_nested_loop(node)
        self.generic_visit(node)

    def _check_nested_loop(self, node):

        for stmt in node.body:

            if isinstance(stmt, (ast.For, ast.While)):

                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Boucle imbriquée détectée. "
                        "Les boucles imbriquées peuvent entraîner une complexité O(n²). "
                        "Envisagez d'utiliser une structure plus efficace comme un 'set' "
                        "ou de repenser l'algorithme."
                    ),
                    line=stmt.lineno,
                    column=stmt.col_offset,
                    end_line=stmt.end_lineno,
                    end_column=stmt.end_col_offset
                )

                self.diagnostics.append(diagnostic)