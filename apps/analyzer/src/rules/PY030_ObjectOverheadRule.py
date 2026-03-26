import ast
from models.diagnostic import Diagnostic


class ObjectOverheadRule(ast.NodeVisitor):
    RULE_ID = "PY030"

    def __init__(self):
        self.diagnostics = []

    def visit_Assign(self, node: ast.Assign):

        # Vérifie si on assigne une liste
        if isinstance(node.value, ast.List):

            elements = node.value.elts

            # Vérifie que la liste contient uniquement des nombres
            if elements and all(
                isinstance(e, ast.Constant) and isinstance(e.value, (int, float))
                for e in elements
            ):

                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Liste de nombres détectée. En Python, chaque élément est un objet "
                        "avec un coût mémoire élevé. Pour des données numériques intensives, "
                        "préférez un tableau NumPy pour une meilleure efficacité mémoire."
                    ),
                    line=node.lineno,
                    column=node.col_offset,
                    end_line=node.end_lineno,
                    end_column=node.end_col_offset
                )

                self.diagnostics.append(diagnostic)

        self.generic_visit(node)