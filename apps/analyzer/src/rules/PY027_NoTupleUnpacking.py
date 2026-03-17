import ast
from models.diagnostic import Diagnostic


class MultipleAssignmentUnpackingRule(ast.NodeVisitor):
    RULE_ID = "PY027"

    def __init__(self):
        self.diagnostics = []

    def visit_While(self, node: ast.While):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._check_body(node.body)
        self.generic_visit(node)

    def _check_body(self, body):
        for i in range(len(body) - 2):
            first = body[i]
            second = body[i + 1]
            third = body[i + 2]

            if (
                isinstance(first, ast.Assign)
                and isinstance(second, ast.Assign)
                and isinstance(third, ast.Assign)
                and len(first.targets) == 1
                and len(second.targets) == 1
                and len(third.targets) == 1
                and isinstance(first.targets[0], ast.Name)
                and isinstance(second.targets[0], ast.Name)
                and isinstance(third.targets[0], ast.Name)
                and isinstance(first.value, ast.Name)
                and isinstance(third.value, ast.Name)
            ):
                temp_name = first.targets[0].id
                second_target = second.targets[0].id
                third_target = third.targets[0].id
                first_source = first.value.id
                third_source = third.value.id

                if first_source == second_target and temp_name == third_source:
                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "Suite d'affectations détectée pouvant être remplacée "
                            "par un unpacking multiple, par exemple "
                            "'a, b = b, a % b'."
                        ),
                        line=first.lineno,
                        column=first.col_offset,
                        end_line=third.end_lineno,
                        end_column=third.end_col_offset
                    )

                    self.diagnostics.append(diagnostic)