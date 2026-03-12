import ast
from models.diagnostic import Diagnostic


class PreferForRangeRule(ast.NodeVisitor):
    RULE_ID = "PY022"

    def __init__(self):
        self.diagnostics = []

    def visit_While(self, node: ast.While):

        # Vérifier si la condition est une comparaison
        if isinstance(node.test, ast.Compare):

            left = node.test.left

            # Vérifier si la variable de la condition est un nom
            if isinstance(left, ast.Name):

                var_name = left.id

                # Chercher i += 1 dans le corps de la boucle
                for stmt in node.body:

                    if isinstance(stmt, ast.AugAssign):

                        if isinstance(stmt.target, ast.Name):

                            if stmt.target.id == var_name:

                                if isinstance(stmt.op, ast.Add):

                                    if isinstance(stmt.value, ast.Constant) and stmt.value.value == 1:

                                        diagnostic = Diagnostic(
                                            rule_id=self.RULE_ID,
                                            message=(
                                                "Boucle 'while' avec compteur manuel détectée. "
                                                "Préférez 'for i in range(...)' pour une boucle "
                                                "plus lisible et idiomatique en Python."
                                            ),
                                            line=node.lineno,
                                            column=node.col_offset,
                                            end_line=node.end_lineno,
                                            end_column=node.end_col_offset
                                        )

                                        self.diagnostics.append(diagnostic)

        self.generic_visit(node)