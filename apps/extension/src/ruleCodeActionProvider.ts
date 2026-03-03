import * as vscode from "vscode";

export class PyQuitCodeActionProvider implements vscode.CodeActionProvider {
  provideCodeActions(
    document: vscode.TextDocument,
    range: vscode.Range,
    context: vscode.CodeActionContext,
  ): vscode.CodeAction[] {
    return context.diagnostics.map((diagnostic) => {
      const action = new vscode.CodeAction(
        "Show rule details",
        vscode.CodeActionKind.QuickFix,
      );

      action.command = {
        command: "pyquit.showRuleDetails",
        title: "Show rule details",
        arguments: [diagnostic.code],
      };

      return action;
    });
  }
}
