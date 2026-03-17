import ast
from models.diagnostic import Diagnostic


class SetMembershipRule(ast.NodeVisitor):
    RULE_ID = "PY004"

    def __init__(self):
        self.diagnostics = []
        self.list_variables = set()

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.list_variables.add(target.id)

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        for op, comparator in zip(node.ops, node.comparators):

            if isinstance(op, (ast.In, ast.NotIn)):
                if isinstance(comparator, ast.Name) and comparator.id in self.list_variables:

                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=f"Préférez utiliser un set plutôt qu'une liste pour la recherche d'appartenance sur '{comparator.id}'.",
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=getattr(node, "end_lineno", node.lineno),
                        end_column=getattr(node, "end_col_offset", node.col_offset),
                    )

                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)