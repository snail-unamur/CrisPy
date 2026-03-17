import ast
from models.diagnostic import Diagnostic


class EAFPInsteadOfLBYLRule(ast.NodeVisitor):
    RULE_ID = "PY031"

    def __init__(self):
        self.diagnostics = []

    def visit_If(self, node: ast.If):
        if isinstance(node.test, ast.Call):
            test_call = node.test

            if self._is_os_path_exists(test_call):
                for stmt in node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                        if self._is_file_action(stmt.value):
                            diagnostic = Diagnostic(
                                rule_id=self.RULE_ID,
                                message=(
                                    "Style LBYL détecté avec 'os.path.exists(...)'. "
                                    "Préférez le style EAFP avec 'try/except' "
                                    "pour un code plus pythonique et plus robuste."
                                ),
                                line=node.lineno,
                                column=node.col_offset,
                                end_line=node.end_lineno,
                                end_column=node.end_col_offset
                            )

                            self.diagnostics.append(diagnostic)

                    elif isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                        if self._is_file_action(stmt.value):
                            diagnostic = Diagnostic(
                                rule_id=self.RULE_ID,
                                message=(
                                    "Style LBYL détecté avec 'os.path.exists(...)'. "
                                    "Préférez le style EAFP avec 'try/except' "
                                    "pour un code plus pythonique et plus robuste."
                                ),
                                line=node.lineno,
                                column=node.col_offset,
                                end_line=node.end_lineno,
                                end_column=node.end_col_offset
                            )

                            self.diagnostics.append(diagnostic)

        self.generic_visit(node)

    def _is_os_path_exists(self, call: ast.Call) -> bool:
        if isinstance(call.func, ast.Attribute) and call.func.attr == "exists":
            value = call.func.value
            if isinstance(value, ast.Attribute) and value.attr == "path":
                if isinstance(value.value, ast.Name) and value.value.id == "os":
                    return True
        return False

    def _is_file_action(self, call: ast.Call) -> bool:
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in {"unlink", "remove"}:
                if isinstance(call.func.value, ast.Name) and call.func.value.id == "os":
                    return True

        if isinstance(call.func, ast.Name) and call.func.id == "open":
            return True

        return False