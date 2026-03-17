import ast
from models.diagnostic import Diagnostic


class ExceptOrderRule(ast.NodeVisitor):
    RULE_ID = "PY029"

    def __init__(self):
        self.diagnostics = []

    def visit_Try(self, node: ast.Try):
        generic_seen = False

        for handler in node.handlers:
            if handler.type is None:
                generic_seen = True
                continue

            if isinstance(handler.type, ast.Name):
                if handler.type.id in {"Exception", "BaseException"}:
                    generic_seen = True
                    continue

                if generic_seen:
                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "Ordre des clauses 'except' suspect. "
                            "Placez les exceptions spécifiques avant "
                            "les exceptions génériques comme 'Exception'."
                        ),
                        line=handler.lineno,
                        column=handler.col_offset,
                        end_line=handler.end_lineno,
                        end_column=handler.end_col_offset
                    )

                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)