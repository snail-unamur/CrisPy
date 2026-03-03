import * as vscode from "vscode";
import * as path from "node:path";
import { runLint } from "./runner";
import { PyQuitCodeActionProvider } from "./ruleCodeActionProvider";
import { registerRulePanelCommand } from "./rulePanel";

let collection: vscode.DiagnosticCollection;

export function activate(context: vscode.ExtensionContext) {
  collection = vscode.languages.createDiagnosticCollection("py-optimize");
  context.subscriptions.push(collection);

  const analyzerPath = path.join(
    context.extensionPath,
    "..",
    "analyzer",
    "src",
    "main.py",
  );

  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument((doc) =>
      runLint(doc, collection, analyzerPath),
    ),
    vscode.workspace.onDidOpenTextDocument((doc) =>
      runLint(doc, collection, analyzerPath),
    ),
    vscode.languages.registerCodeActionsProvider(
      "python",
      new PyQuitCodeActionProvider(),
      { providedCodeActionKinds: [vscode.CodeActionKind.QuickFix] },
    ),
  );

  registerRulePanelCommand(context);
}

export function deactivate() {
  collection?.dispose();
}
