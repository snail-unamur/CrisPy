import * as vscode from "vscode";
import { ruleMap } from "@crispy/rules";

export class CrisPyCodeActionProvider implements vscode.CodeActionProvider {
  provideCodeActions(
    document: vscode.TextDocument,
    range: vscode.Range,
    context: vscode.CodeActionContext,
  ): vscode.CodeAction[] {
    const actions: vscode.CodeAction[] = [];

    for (const diagnostic of context.diagnostics) {
      const ruleCode = String(diagnostic.code);
      const rule = ruleMap[ruleCode];
      const ruleSlug = rule?.slug || ruleCode;

      // Show rule detail
      const showDetails = new vscode.CodeAction(
        "Show rule details",
        vscode.CodeActionKind.QuickFix,
      );

      showDetails.command = {
        command: "crispy.showRuleDetails",
        title: "Show rule details",
        arguments: [ruleCode],
      };

      actions.push(showDetails);

      // Disable rule for the nex line
      const disableNextLine = new vscode.CodeAction(
        `Disable for next line`,
        vscode.CodeActionKind.QuickFix,
      );
      disableNextLine.edit = new vscode.WorkspaceEdit();

      const line = diagnostic.range.start.line;

      disableNextLine.edit.insert(
        document.uri,
        new vscode.Position(line, 0),
        `# crispy-disable-next-line ${ruleSlug}\n`,
      );

      actions.push(disableNextLine);

      // Disable rule for the file
      const disableFile = new vscode.CodeAction(
        `Disable for the entire file`,
        vscode.CodeActionKind.QuickFix,
      );

      disableFile.edit = new vscode.WorkspaceEdit();

      disableFile.edit.insert(
        document.uri,
        new vscode.Position(0, 0),
        `# crispy-disable ${ruleSlug}\n`,
      );

      actions.push(disableFile);
    }

    return actions;
  }
}
