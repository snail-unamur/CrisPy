import ast
from models.diagnostic import Diagnostic


class ListComprehensionInsteadOfMapFilterRule(ast.NodeVisitor):
    RULE_ID = "PY032"

    def __init__(self):
        self.diagnostics = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {"map", "filter"}:
            if node.args:
                first_arg = node.args[0]

                if isinstance(first_arg, ast.Lambda):
                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            f"Utilisation de '{node.func.id}()' avec lambda détectée. "
                            "Préférez une compréhension de liste pour un code "
                            "plus lisible et plus idiomatique."
                        ),
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        end_column=node.end_col_offset
                    )

                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)