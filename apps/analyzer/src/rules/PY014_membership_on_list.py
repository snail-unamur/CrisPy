import ast
from models.diagnostic import Diagnostic


class MembershipOnListRule(ast.NodeVisitor):
    RULE_ID = "PY014"

    def __init__(self):
        self.diagnostics = []
        self.list_vars = set()

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.list_vars.add(target.id)

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, (ast.In, ast.NotIn)):
                if isinstance(comparator, ast.Name) and comparator.id in self.list_vars:
                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "Un test d'appartenance sur une liste est en O(n). "
                            "Si les recherches sont fréquentes, envisagez d'utiliser un set."
                        ),
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        end_column=node.end_col_offset,
                    )
                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)