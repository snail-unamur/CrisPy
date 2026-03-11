import ast
from models.diagnostic import Diagnostic


class GeneratorInsteadOfListRule(ast.NodeVisitor):
    RULE_ID = "PY020"

    def __init__(self):
        self.diagnostics = []

    def visit_Call(self, node: ast.Call):

        # Vérifier que c'est un appel à une fonction
        if isinstance(node.func, ast.Name):

            func_name = node.func.id

            # Fonctions typiques où un générateur est préférable
            target_funcs = {"sum", "any", "all", "max", "min"}

            if func_name in target_funcs and node.args:

                arg = node.args[0]

                # Détecter une list comprehension
                if isinstance(arg, ast.ListComp):

                    diagnostic = Diagnostic(
                        rule_id=self.RULE_ID,
                        message=(
                            "Évitez de créer une liste temporaire dans "
                            f"'{func_name}()'. Utilisez un générateur pour "
                            "réduire l'utilisation mémoire (O(n) → O(1))."
                        ),
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        end_column=node.end_col_offset
                    )

                    self.diagnostics.append(diagnostic)

        self.generic_visit(node)