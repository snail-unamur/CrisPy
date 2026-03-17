import ast
from models.diagnostic import Diagnostic


class UseWithOpenRule(ast.NodeVisitor):
    RULE_ID = "PY024"

    def __init__(self):
        self.diagnostics = []
        self.parents = {}

    def visit(self, node):
        for child in ast.iter_child_nodes(node):
            self.parents[child] = node
        return super().visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            parent = self.parents.get(node)

            in_with = False
            current = node
            while current in self.parents:
                current = self.parents[current]
                if isinstance(current, ast.With):
                    in_with = True
                    break

            if not in_with:
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Ouverture de fichier sans gestionnaire de contexte détectée. "
                        "Utilisez 'with open(...) as f:' pour garantir la fermeture "
                        "du fichier même en cas d'exception."
                    ),
                    line=node.lineno,
                    column=node.col_offset,
                    end_line=node.end_lineno,
                    end_column=node.end_col_offset
                )

                self.diagnostics.append(diagnostic)

        self.generic_visit(node)