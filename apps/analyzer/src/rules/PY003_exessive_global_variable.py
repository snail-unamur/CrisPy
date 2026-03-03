import ast
from models.diagnostic import Diagnostic


class ExcessiveGlobalRule(ast.NodeVisitor):
    RULE_ID = "PY003"

    def __init__(self):
        self.diagnostics = []
        self.function_stack = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.function_stack.append(node)
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_Global(self, node: ast.Global):
        if self.function_stack:  
            diagnostic = Diagnostic(
                rule_id=self.RULE_ID,
                message=(
                    "Évitez l'utilisation excessive de variables globales."
                    "Utilisez plutôt des variables comme paramètres."
                ),
                line=node.lineno,
                column=node.col_offset,
                end_line=node.end_lineno,
                end_column=node.end_col_offset,
            )

            self.diagnostics.append(diagnostic)

        self.generic_visit(node)