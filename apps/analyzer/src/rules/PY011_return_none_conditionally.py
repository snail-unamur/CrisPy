import ast
from models.diagnostic import Diagnostic


class ConditionalNoneReturnRule(ast.NodeVisitor):
    RULE_ID = "PY011"

    def __init__(self):
        self.diagnostics = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        returns_none = []
        returns_value = []

        for child in ast.walk(node):
            if isinstance(child, ast.Return):
                if child.value is None:
                    returns_none.append(child)
                elif isinstance(child.value, ast.Constant) and child.value.value is None:
                    returns_none.append(child)
                else:
                    returns_value.append(child)

        if returns_none and returns_value:
            for ret in returns_none:
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Évitez de retourner conditionnellement None dans une fonction "
                        "qui retourne aussi une valeur. Préférez un type de retour cohérent."
                    ),
                    line=ret.lineno,
                    column=ret.col_offset,
                    end_line=ret.end_lineno,
                    end_column=ret.end_col_offset,
                )
                self.diagnostics.append(diagnostic)

        self.generic_visit(node)