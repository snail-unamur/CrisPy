import ast
from models.diagnostic import Diagnostic


class MutableDefaultArgumentRule(ast.NodeVisitor):
    RULE_ID = "PY030"

    def __init__(self):
        self.diagnostics = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        defaults = node.args.defaults

        for default in defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Argument par défaut mutable détecté. "
                        "Utilisez plutôt 'None' puis initialisez la valeur "
                        "à l'intérieur de la fonction."
                    ),
                    line=default.lineno,
                    column=default.col_offset,
                    end_line=default.end_lineno,
                    end_column=default.end_col_offset
                )

                self.diagnostics.append(diagnostic)

        self.generic_visit(node)