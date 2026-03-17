import ast
import re
from models.diagnostic import Diagnostic


class TypeInVariableNameRule(ast.NodeVisitor):
    RULE_ID = "PY028"

    def __init__(self):
        self.diagnostics = []
        self.type_patterns = re.compile(
            r".*(_int|_str|_list|_dict|_set|_tuple|_bool|_float|_obj|_num)$"
        )

    def _check_name(self, node, name: str):
        if self.type_patterns.match(name):
            diagnostic = Diagnostic(
                rule_id=self.RULE_ID,
                message=(
                    f"Le nom '{name}' contient une information de type. "
                    "Préférez un nom basé sur le rôle ou la signification "
                    "de la variable plutôt que sur son type."
                ),
                line=node.lineno,
                column=node.col_offset,
                end_line=node.end_lineno,
                end_column=node.end_col_offset
            )

            self.diagnostics.append(diagnostic)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self._check_name(target, target.id)

        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            self._check_name(node.target, node.target.id)

        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        if isinstance(node.target, ast.Name):
            self._check_name(node.target, node.target.id)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for arg in node.args.args:
            self._check_name(arg, arg.arg)

        self.generic_visit(node)