import ast
from models.diagnostic import Diagnostic


class UnboundedGrowthRule(ast.NodeVisitor):
    RULE_ID = "PY036"

    def __init__(self):
        self.diagnostics = []
        self.list_vars = set()

    # Détecter les listes initialisées
    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.list_vars.add(target.id)

        self.generic_visit(node)

    # Détecter les boucles
    def visit_For(self, node: ast.For):
        self._check_loop(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._check_loop(node)
        self.generic_visit(node)

    def _check_loop(self, node):

        for stmt in node.body:

            # Détecter cache.append(...)
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):

                call = stmt.value

                if isinstance(call.func, ast.Attribute):

                    if call.func.attr == "append":

                        if isinstance(call.func.value, ast.Name):

                            var_name = call.func.value.id

                            # Vérifier si la variable était une liste
                            if var_name in self.list_vars:

                                diagnostic = Diagnostic(
                                    rule_id=self.RULE_ID,
                                    message=(
                                        "Croissance mémoire non contrôlée détectée. "
                                        "Cette structure de données grandit dans une boucle. "
                                        "Vérifiez si le stockage est nécessaire ou utilisez "
                                        "un traitement en flux (streaming)."
                                    ),
                                    line=stmt.lineno,
                                    column=stmt.col_offset,
                                    end_line=stmt.end_lineno,
                                    end_column=stmt.end_col_offset
                                )

                                self.diagnostics.append(diagnostic)