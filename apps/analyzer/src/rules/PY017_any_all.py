import ast
from models.diagnostic import Diagnostic


class AnyAllRule(ast.NodeVisitor):
    RULE_ID = "PY017"

    def __init__(self):
        self.diagnostics = []
        self.bool_vars = {}

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, bool):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.bool_vars[target.id] = node.value.value

        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._check_loop(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._check_loop(node)
        self.generic_visit(node)

    def _check_loop(self, node):
        for stmt in node.body:
            if isinstance(stmt, ast.If):
                for inner in stmt.body:
                    if isinstance(inner, ast.Assign):
                        if len(inner.targets) == 1 and isinstance(inner.targets[0], ast.Name):
                            var_name = inner.targets[0].id

                            if var_name in self.bool_vars:
                                initial_value = self.bool_vars[var_name]

                                if (
                                    isinstance(inner.value, ast.Constant)
                                    and isinstance(inner.value.value, bool)
                                    and inner.value.value != initial_value
                                ):
                                    diagnostic = Diagnostic(
                                        rule_id=self.RULE_ID,
                                        message=(
                                            "Cette boucle avec variable indicatrice peut souvent "
                                            "être remplacée par any() ou all() pour un code plus lisible."
                                        ),
                                        line=stmt.lineno,
                                        column=stmt.col_offset,
                                        end_line=stmt.end_lineno,
                                        end_column=stmt.end_col_offset,
                                    )
                                    self.diagnostics.append(diagnostic)