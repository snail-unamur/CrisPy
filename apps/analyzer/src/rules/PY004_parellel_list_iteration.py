import ast
from models.diagnostic import Diagnostic


class ParallelListIteration(ast.NodeVisitor):
    RULE_ID = "PY004"

    def __init__(self):
        self.diagnostics = []

    def visit_For(self, node: ast.For):
        """
        Detect loops of the form:
            for i in range(len(a)):
                ...
                a[i]
                b[i]

        Suggest using zip(a, b) instead.
        """

        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
            if node.iter.func.id == "range" and len(node.iter.args) == 1:
                arg = node.iter.args[0]

                if (
                    isinstance(arg, ast.Call)
                    and isinstance(arg.func, ast.Name)
                    and arg.func.id == "len"
                    and len(arg.args) == 1
                ):
                    if isinstance(node.target, ast.Name):
                        index_var = node.target.id

                        indexed_sequences = set()

                        for child in ast.walk(node):
                            if isinstance(child, ast.Subscript):
                                if (
                                    isinstance(child.slice, ast.Name)
                                    and child.slice.id == index_var
                                ):
                                    if isinstance(child.value, ast.Name):
                                        indexed_sequences.add(child.value.id)

                        if len(indexed_sequences) >= 2:
                            diagnostic = Diagnostic(
                                rule_id=self.RULE_ID,
                                message=(
                                    "Itération parallèle détectée avec un index. "
                                    "Utilisez `zip()` pour parcourir plusieurs listes "
                                    "en parallèle plutôt que `range(len(...))`."
                                ),
                                line=node.lineno,
                                column=node.col_offset,
                                end_line=node.end_lineno,  # type: ignore
                                end_column=node.end_col_offset,  # type: ignore
                            )
                            self.diagnostics.append(diagnostic)

        self.generic_visit(node)