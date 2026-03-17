import ast
from models.diagnostic import Diagnostic


class MemoryLocalityRule(ast.NodeVisitor):
    RULE_ID = "PY034"

    def __init__(self):
        self.diagnostics = []

    def visit_For(self, node: ast.For):
        self._check_nested_loop(node)
        self.generic_visit(node)

    def _check_nested_loop(self, outer_loop: ast.For):

        # Vérifie qu'il y a une boucle interne
        for inner in outer_loop.body:
            if isinstance(inner, ast.For):

                # Variables de boucle
                outer_var = self._get_loop_var(outer_loop)
                inner_var = self._get_loop_var(inner)

                if not outer_var or not inner_var:
                    continue

                # Chercher accès matrix[i][j]
                for stmt in inner.body:
                    for subnode in ast.walk(stmt):

                        if isinstance(subnode, ast.Subscript):

                            # Vérifier matrix[i][j]
                            if isinstance(subnode.value, ast.Subscript):

                                first_index = self._get_index(subnode.value)
                                second_index = self._get_index(subnode)

                                if first_index and second_index:

                                    # Mauvais ordre détecté
                                    if (
                                        first_index == inner_var and
                                        second_index == outer_var
                                    ):
                                        diagnostic = Diagnostic(
                                            rule_id=self.RULE_ID,
                                            message=(
                                                "Accès mémoire non contigu détecté (mauvaise localité mémoire). "
                                                "Parcourez les structures dans le même ordre que leur indexation "
                                                "(ligne puis colonne) pour optimiser le cache CPU."
                                            ),
                                            line=subnode.lineno,
                                            column=subnode.col_offset,
                                            end_line=subnode.end_lineno,
                                            end_column=subnode.end_col_offset
                                        )

                                        self.diagnostics.append(diagnostic)

    def _get_loop_var(self, node):
        if isinstance(node.target, ast.Name):
            return node.target.id
        return None

    def _get_index(self, node):
        if isinstance(node.slice, ast.Name):
            return node.slice.id
        elif isinstance(node.slice, ast.Index):  # compat ancienne version
            if isinstance(node.slice.value, ast.Name):
                return node.slice.value.id
        return None