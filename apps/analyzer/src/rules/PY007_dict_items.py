import ast
from models.diagnostic import Diagnostic


class DictItemsRule(ast.NodeVisitor):
    RULE_ID = "PY007"

    def __init__(self):
        self.diagnostics = []

    def visit_For(self, node: ast.For):
        # recherche de la forme "for k in d:" puis d[k] dans le corps
        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.Name):
            dict_name = node.iter.id
            key_name = node.target.id

            # un visiteur auxiliaire pour parcourir le corps de la boucle
            class _Finder(ast.NodeVisitor):
                def __init__(self, dict_name: str, key_name: str):
                    self.dict_name = dict_name
                    self.key_name = key_name
                    self.found = False

                def visit_Subscript(self, sub: ast.Subscript):
                    if (
                        isinstance(sub.value, ast.Name)
                        and sub.value.id == self.dict_name
                        and isinstance(sub.slice, ast.Name)
                        and sub.slice.id == self.key_name
                    ):
                        self.found = True
                    self.generic_visit(sub)

            finder = _Finder(dict_name, key_name)
            for stmt in node.body:
                finder.visit(stmt)

            if finder.found:
                diagnostic = Diagnostic(
                    rule_id=self.RULE_ID,
                    message=(
                        "Utilisez `dict.items()` pour parcourir simultanément la clé et la valeur "
                        "plutôt que d'accéder à `d[k]` à l'intérieur de la boucle."
                    ),
                    line=node.lineno,
                    column=node.col_offset,
                    end_line=node.end_lineno,  # type: ignore
                    end_column=node.end_col_offset,  # type: ignore
                )
                self.diagnostics.append(diagnostic)

        self.generic_visit(node)
