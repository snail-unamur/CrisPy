import ast
from models.diagnostic import Diagnostic


class MutableDefaultRule(ast.NodeVisitor):
    RULE_ID = "PY010"

    def __init__(self):
        self.diagnostics = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # inspect default values for arguments
        for arg, default in zip(node.args.args[-len(node.args.defaults) :], node.args.defaults):
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Ne pas utiliser d'arguments par défaut mutables (liste, dict, set, ...)"
                    ),
                    line=default.lineno,
                    column=default.col_offset,
                    end_line=default.end_lineno,  # type: ignore
                    end_column=default.end_col_offset,  # type: ignore
                )
                self.diagnostics.append(diagnostic)
            # also catch cases like default=list() or dict()
            elif isinstance(default, ast.Call) and isinstance(default.func, ast.Name) and default.func.id in {"list", "dict", "set"}:
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Ne pas utiliser d'arguments par défaut mutables (liste, dict, set, ...)"
                    ),
                    line=default.lineno,
                    column=default.col_offset,
                    end_line=default.end_lineno,  # type: ignore
                    end_column=default.end_col_offset,  # type: ignore
                )
                self.diagnostics.append(diagnostic)
        self.generic_visit(node)
