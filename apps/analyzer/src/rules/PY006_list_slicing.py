import ast
from models.diagnostic import Diagnostic


class ListSlicingRule(ast.NodeVisitor):
    RULE_ID = "PY006"

    def __init__(self):
        self.diagnostics = []

    def visit_Subscript(self, node: ast.Subscript):
        # A slice expression (e.g. lst[1:10], lst[::2], lst[-5:]) creates a new
        # list in memory. On large sequences, this can double memory usage and
        # degrade performance. Instead, prefer iterators such as
        # ``itertools.islice`` or custom generators when you only need to
        # traverse a subset of the data.
        if isinstance(node.slice, ast.Slice):
            diagnostic = Diagnostic(
                rule_id=self.RULE_ID,
                message=(
                    "Le slicing d'une séquence crée une copie en mémoire. "
                    "Pour de grandes listes, utilisez "
                    "``itertools.islice`` ou un générateur pour éviter des "
                    "allocations inutiles."
                ),
                line=node.lineno,
                column=node.col_offset,
                end_line=node.end_lineno,  # type: ignore
                end_column=node.end_col_offset, # type: ignore
            )
            self.diagnostics.append(diagnostic)

        self.generic_visit(node)
