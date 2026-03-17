import ast
from models.diagnostic import Diagnostic


class DictComprehensionRule(ast.NodeVisitor):
    RULE_ID = "PY026"

    def __init__(self):
        self.diagnostics = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "dict":
            if node.args:
                first_arg = node.args[0]

                if isinstance(first_arg, ast.ListComp):
                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "Initialisation de dictionnaire avec 'dict([...])' détectée. "
                            "Préférez une compréhension de dictionnaire "
                            "'{k: v for ...}' pour un code plus lisible."
                        ),
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        end_column=node.end_col_offset
                    )

                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)