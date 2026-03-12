import ast
from models.diagnostic import Diagnostic


class ListMembershipRule(ast.NodeVisitor):
    RULE_ID = "PY018"

    def __init__(self):
        self.diagnostics = []
        self.list_vars = set()

    # Détecter les variables initialisées comme listes
    def visit_Assign(self, node: ast.Assign):

        if isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.list_vars.add(target.id)

        self.generic_visit(node)

    # Détecter les comparaisons "x in ..."
    def visit_Compare(self, node: ast.Compare):

        if len(node.ops) == 1 and isinstance(node.ops[0], ast.In):

            comparator = node.comparators[0]

            if isinstance(comparator, ast.Name):

                var_name = comparator.id

                if var_name in self.list_vars:

                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "Utiliser une liste pour des tests d'appartenance fréquents peut être inefficace. "
                            "Les listes nécessitent une recherche linéaire O(n). "
                            "Utilisez un 'set' pour obtenir une recherche moyenne en O(1)."
                        ),
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        end_column=node.end_col_offset
                    )

                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)