import * as vscode from "vscode";

export function mapSeverity(
  severity: "info" | "warning" | "error" | "hint",
): vscode.DiagnosticSeverity {
  switch (severity) {
    case "info":
      return vscode.DiagnosticSeverity.Information;
    case "warning":
      return vscode.DiagnosticSeverity.Warning;
    case "error":
      return vscode.DiagnosticSeverity.Error;
    case "hint":
      return vscode.DiagnosticSeverity.Hint;
    default:
      return vscode.DiagnosticSeverity.Information;
  }
}
