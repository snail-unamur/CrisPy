import ast
import builtins
from models.diagnostic import Diagnostic


class ShadowBuiltinRule(ast.NodeVisitor):
    RULE_ID = "PY016"

    def __init__(self):
        self.diagnostics = []
        self.builtin_names = set(dir(builtins))

    def _add_diagnostic(self, node, name: str):
        diagnostic = Diagnostic(
            rule_id=self.RULE_ID,
            message=(
                f"Le nom '{name}' masque un nom intégré Python. "
                "Choisissez un autre nom de variable."
            ),
            line=node.lineno,
            column=node.col_offset,
            end_line=node.end_lineno,
            end_column=node.end_col_offset,
        )
        self.diagnostics.append(diagnostic)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in self.builtin_names:
                self._add_diagnostic(target, target.id)

        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id in self.builtin_names:
            self._add_diagnostic(node.target, node.target.id)

        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        if isinstance(node.target, ast.Name) and node.target.id in self.builtin_names:
            self._add_diagnostic(node.target, node.target.id)

        self.generic_visit(node)