import ast
from models.diagnostic import Diagnostic


class StringJoinRule(ast.NodeVisitor):
    RULE_ID = "PY015"

    def __init__(self):
        self.diagnostics = []
        self.string_vars = set()

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.string_vars.add(target.id)

        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._check_loop_body(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._check_loop_body(node)
        self.generic_visit(node)

    def _check_loop_body(self, node):
        for stmt in node.body:
            if isinstance(stmt, ast.AugAssign):
                if isinstance(stmt.op, ast.Add):
                    if isinstance(stmt.target, ast.Name):
                        var_name = stmt.target.id
                        if var_name in self.string_vars:
                            diagnostic = Diagnostic(
                                rule_id=self.RULE_ID,
                                message=(
                                    "Évitez de concaténer des chaînes avec '+=' dans une boucle. "
                                    "Utilisez plutôt ''.join(...) pour de meilleures performances."
                                ),
                                line=stmt.lineno,
                                column=stmt.col_offset,
                                end_line=stmt.end_lineno,
                                end_column=stmt.end_col_offset,
                            )
                            self.diagnostics.append(diagnostic)