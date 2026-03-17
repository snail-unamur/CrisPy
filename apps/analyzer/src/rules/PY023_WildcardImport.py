import ast
from models.diagnostic import Diagnostic


class WildcardImportRule(ast.NodeVisitor):
    RULE_ID = "PY023"

    def __init__(self):
        self.diagnostics = []

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            if alias.name == "*":
                module_name = node.module or "module inconnu"

                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        f"Évitez l'import générique depuis '{module_name}'. "
                        "Préférez un import explicite pour améliorer la lisibilité "
                        "et éviter les collisions de noms."
                    ),
                    line=node.lineno,
                    column=node.col_offset,
                    end_line=node.end_lineno,
                    end_column=node.end_col_offset
                )

                self.diagnostics.append(diagnostic)

        self.generic_visit(node)