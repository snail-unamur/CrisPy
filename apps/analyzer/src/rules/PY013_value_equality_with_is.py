import ast
from models.diagnostic import Diagnostic


class IsForValueComparisonRule(ast.NodeVisitor):
    RULE_ID = "PY013"

    def __init__(self):
        self.diagnostics = []

    def visit_Compare(self, node: ast.Compare):
        operators = node.ops
        comparators = node.comparators

        for op, comparator in zip(operators, comparators):
            if isinstance(op, (ast.Is, ast.IsNot)):
                # Autoriser explicitement les comparaisons avec None
                if isinstance(comparator, ast.Constant) and comparator.value is None:
                    continue

                # Cas simples cohérents avec l'approche de tes autres règles
                if isinstance(comparator, (ast.Constant, ast.List, ast.Tuple, ast.Set, ast.Dict)):
                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "N'utilisez pas 'is' pour comparer des valeurs. "
                            "Utilisez '==' ou '!=' pour l'égalité de contenu."
                        ),
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        end_column=node.end_col_offset,
                    )
                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)