import ast
from models.diagnostic import Diagnostic


class ListConcatInLoopRule(ast.NodeVisitor):
    RULE_ID = "PY021"

    def __init__(self):
        self.diagnostics = []

    def visit_For(self, node: ast.For):
        self._check_loop_body(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._check_loop_body(node)
        self.generic_visit(node)

    def _check_loop_body(self, node):

        for stmt in node.body:

            if isinstance(stmt, ast.Assign):

                if isinstance(stmt.value, ast.BinOp) and isinstance(stmt.value.op, ast.Add):

                    # Vérifier que la cible est une variable
                    if isinstance(stmt.targets[0], ast.Name):

                        left_var = stmt.targets[0].id

                        # Vérifier si la variable est utilisée dans l'opération +
                        if isinstance(stmt.value.left, ast.Name):

                            right_var = stmt.value.left.id

                            if left_var == right_var:

                                diagnostic = Diagnostic(
                                    rule_id=self.RULE_ID,
                                    message=(
                                        "Évitez de concaténer des listes avec '+' "
                                        "dans une boucle. Utilisez 'list.extend()' "
                                        "pour éviter une complexité O(n²)."
                                    ),
                                    line=stmt.lineno,
                                    column=stmt.col_offset,
                                    end_line=stmt.end_lineno,
                                    end_column=stmt.end_col_offset
                                )

                                self.diagnostics.append(diagnostic)