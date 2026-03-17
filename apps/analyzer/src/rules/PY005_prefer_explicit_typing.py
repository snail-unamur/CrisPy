import ast
from models.diagnostic import Diagnostic


class ExplicitTypingRule(ast.NodeVisitor):
    RULE_ID = "PY005"

    def __init__(self):
        self.diagnostics = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for arg in node.args.args:

            if arg.arg in ("self", "cls"):
                continue

            if arg.annotation is None:
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=f"Le paramètre '{arg.arg}' devrait avoir un type hint explicite.",
                    line=arg.lineno,
                    column=arg.col_offset,
                    end_line=getattr(arg, "end_lineno", arg.lineno),
                    end_column=getattr(arg, "end_col_offset", arg.col_offset),
                )

                self.diagnostics.append(diagnostic)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):

                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=f"La variable '{target.id}' devrait avoir un type hint explicite.",
                    line=target.lineno,
                    column=target.col_offset,
                    end_line=getattr(target, "end_lineno", target.lineno),
                    end_column=getattr(target, "end_col_offset", target.col_offset),
                )

                self.diagnostics.append(diagnostic)

        self.generic_visit(node)