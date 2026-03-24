import * as vscode from "vscode";
import { execFile } from "node:child_process";
import { ruleMap } from "@pyquit/rules";
import { mapSeverity } from "./severity";

type DisableState = {
  fileDisabled: Set<string>; // Stores slugs
  lineDisabled: Map<number, Set<string>>; // Stores slugs
};

const SEVERITY_PRIORITY: Record<number, number> = {
  [vscode.DiagnosticSeverity.Error]: 0,
  [vscode.DiagnosticSeverity.Warning]: 1,
  [vscode.DiagnosticSeverity.Information]: 2,
  [vscode.DiagnosticSeverity.Hint]: 3,
};

function parseDisables(document: vscode.TextDocument): DisableState {
  const fileDisabled = new Set<string>();
  const lineDisabled = new Map<number, Set<string>>();

  for (let i = 0; i < document.lineCount; i++) {
    const text = document.lineAt(i).text.trim();

    // entire file
    if (
      text.startsWith("# pyquit-disable") &&
      !text.startsWith("# pyquit-disable-next-line")
    ) {
      const parts = text.replace("# pyquit-disable", "").trim().split(/\s+/);

      for (const slug of parts) {
        if (slug) fileDisabled.add(slug);
      }

      continue;
    }

    // next line
    if (text.startsWith("# pyquit-disable-next-line")) {
      const parts = text
        .replace("# pyquit-disable-next-line", "")
        .trim()
        .split(/\s+/);

      let targetLine = i + 1;

      while (targetLine < document.lineCount) {
        const nextText = document.lineAt(targetLine).text.trim();
        if (nextText.startsWith("# pyquit-disable-next-line")) {
          targetLine++;
        } else {
          break;
        }
      }

      if (targetLine < document.lineCount) {
        if (!lineDisabled.has(targetLine)) {
          lineDisabled.set(targetLine, new Set());
        }

        const set = lineDisabled.get(targetLine)!;

        for (const slug of parts) {
          if (slug) set.add(slug);
        }
      }
    }
  }

  return { fileDisabled, lineDisabled };
}
function isDisabled(
  ruleId: string,
  line: number,
  state: DisableState,
): boolean {
  const rule = ruleMap[ruleId];
  const slug = rule?.slug || ruleId;

  if (state.fileDisabled.has("ALL") || state.fileDisabled.has(slug))
    return true;

  const lineRules = state.lineDisabled.get(line);
  return lineRules?.has(slug) || lineRules?.has("ALL") || false;
}

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
      const disabled = parseDisables(document);
      const priorityMap = new Map<number, vscode.Diagnostic>();

      for (const r of results) {
        const ruleId = r.rule_id;
        const line = r.line - 1;

        if (isDisabled(ruleId, line, disabled)) continue; //disabled rules

        const rule = ruleMap[ruleId];
        const severity = mapSeverity(rule?.severity);
        const range = new vscode.Range(
          new vscode.Position(line, r.column),
          new vscode.Position(r.end_line - 1, r.end_column),
        );

        const diagnostic = new vscode.Diagnostic(
          range,
          rule?.title || `Optimization suggestion (${rule?.slug || ruleId})`,
          severity,
        );
        diagnostic.code = ruleId;

        // priority
        const existing = priorityMap.get(line);
        if (existing) {
          const newPrio = SEVERITY_PRIORITY[diagnostic.severity] ?? 99;
          const oldPrio = SEVERITY_PRIORITY[existing.severity] ?? 99;
          if (newPrio < oldPrio) {
            priorityMap.set(line, diagnostic);
          }
        } else {
          priorityMap.set(line, diagnostic);
        }
      }

      collection.set(document.uri, Array.from(priorityMap.values()));
    } catch (e) {
      console.error("PyQuit JSON parse error:", e);
    }
  });
}
