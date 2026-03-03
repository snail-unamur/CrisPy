import * as vscode from "vscode";
import { execFile } from "node:child_process";
import { ruleMap } from "@pyquit/rules";
import { mapSeverity } from "./severity";

export async function runLint(
  document: vscode.TextDocument,
  collection: vscode.DiagnosticCollection,
  analyzerPath: string,
) {
  if (document.languageId !== "python") return;

  const pythonExtension = vscode.extensions.getExtension("ms-python.python");
  if (!pythonExtension) return;

  const api = await pythonExtension.activate();
  const pythonPath =
    api.settings.getExecutionDetails(document.uri).execCommand?.[0] ?? "python";

  execFile(pythonPath, [analyzerPath, document.fileName], (err, stdout) => {
    if (err || document.isClosed) return;

    try {
      const results = JSON.parse(stdout);

      const diagnostics = results.map((r: any) => {
        const rule = ruleMap[r.rule_id];

        const range = new vscode.Range(
          new vscode.Position(r.line - 1, r.column),
          new vscode.Position(r.end_line - 1, r.end_column),
        );

        const diagnostic = new vscode.Diagnostic(
          range,
          rule?.title || `Optimization suggestion (${r.rule_id})`,
          mapSeverity(rule?.severity),
        );

        diagnostic.code = r.rule_id;

        return diagnostic;
      });

      collection.set(document.uri, diagnostics);
    } catch {
      console.error("PyQuit JSON parse error:", stdout);
    }
  });
}
