import * as vscode from "vscode";
import * as path from "node:path";
import { runLint } from "./runner";
import { CrisPyCodeActionProvider } from "./ruleCodeActionProvider";
import { registerRulePanelCommand } from "./rulePanel";

let collection: vscode.DiagnosticCollection;

const debounceTimers = new Map<string, NodeJS.Timeout>();

function triggerLint(document: vscode.TextDocument, analyzerPath: string) {
  const key = document.uri.toString();

  if (debounceTimers.has(key)) {
    clearTimeout(debounceTimers.get(key));
  }

  const timeout = setTimeout(() => {
    runLint(document, collection, analyzerPath);
    debounceTimers.delete(key);
  }, 300);

  debounceTimers.set(key, timeout);
}

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
    vscode.workspace.onDidOpenTextDocument((doc) =>
      triggerLint(doc, analyzerPath),
    ),
    vscode.workspace.onDidSaveTextDocument((doc) =>
      triggerLint(doc, analyzerPath),
    ),
    vscode.workspace.onDidChangeTextDocument((event) =>
      triggerLint(event.document, analyzerPath),
    ),
    vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor) {
        triggerLint(editor.document, analyzerPath);
      }
    }),
    vscode.workspace.onDidCloseTextDocument((doc) => {
      collection.delete(doc.uri);
    }),
    vscode.languages.registerCodeActionsProvider(
      "python",
      new CrisPyCodeActionProvider(),
      {
        providedCodeActionKinds: [vscode.CodeActionKind.QuickFix],
      },
    ),
  );

  registerRulePanelCommand(context);

  vscode.workspace.textDocuments.forEach((doc) =>
    triggerLint(doc, analyzerPath),
  );
}

export function deactivate() {
  collection?.dispose();
}
