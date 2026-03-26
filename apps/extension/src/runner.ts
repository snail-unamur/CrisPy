import * as vscode from "vscode";
import { execFile } from "node:child_process";
import { ruleMap } from "@pyquit/rules";
import { mapSeverity } from "./severity";

const SEVERITY_PRIORITY: Record<number, number> = {
  [vscode.DiagnosticSeverity.Error]: 0,
  [vscode.DiagnosticSeverity.Warning]: 1,
  [vscode.DiagnosticSeverity.Information]: 2,
  [vscode.DiagnosticSeverity.Hint]: 3,
};

type WorkspaceConfig = {
  disabledRules?: string[];
  rules?: Record<string, "off" | "warn" | "error">;
};

type DisableState = {
  fileDisabled: Set<string>;
  lineDisabled: Map<number, Set<string>>;
};

async function loadWorkspaceConfig(
  currentUri: vscode.Uri,
): Promise<WorkspaceConfig | null> {
  let currentDir = vscode.Uri.joinPath(currentUri, "..");
  const workspaceRoot = vscode.workspace.getWorkspaceFolder(currentUri)?.uri;

  while (true) {
    const configUri = vscode.Uri.joinPath(currentDir, ".pyquit");

    try {
      await vscode.workspace.fs.stat(configUri);

      const content = await vscode.workspace.fs.readFile(configUri);
      return JSON.parse(new TextDecoder().decode(content));
    } catch {
      const parentDir = vscode.Uri.joinPath(currentDir, "..");

      if (
        parentDir.toString() === currentDir.toString() ||
        (workspaceRoot &&
          !parentDir.toString().startsWith(workspaceRoot.toString()))
      ) {
        break;
      }
      currentDir = parentDir;
    }
  }
  return null;
}

function getWorkspaceDisabledRules(config: any): Set<string> {
  if (!config) return new Set();

  return new Set(
    Object.entries(config)
      .filter(([_, value]) => value === "off")
      .map(([slug]) => slug),
  );
}

function getInFileDisabledRules(document: vscode.TextDocument): DisableState {
  const fileDisabled = new Set<string>();
  const lineDisabled = new Map<number, Set<string>>();

  for (let i = 0; i < document.lineCount; i++) {
    const text = document.lineAt(i).text.trim();

    // entire file
    if (
      text.startsWith("# pyquit-disable") &&
      !text.startsWith("# pyquit-disable-next-line")
    ) {
      const parts = text
        .replace("# pyquit-disable", "")
        .trim()
        .split(/\s+/)
        .filter(Boolean);

      for (const slug of parts) {
        fileDisabled.add(slug);
      }

      continue;
    }

    // next line
    if (text.startsWith("# pyquit-disable-next-line")) {
      const parts = text
        .replace("# pyquit-disable-next-line", "")
        .trim()
        .split(/\s+/)
        .filter(Boolean);

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
          set.add(slug);
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
  workspaceDisabled: Set<string>,
): boolean {
  const rule = ruleMap[ruleId];
  const slug = rule?.slug || ruleId;

  // workspace
  if (workspaceDisabled.has(slug) || workspaceDisabled.has("ALL")) {
    return true;
  }

  // file
  if (state.fileDisabled.has("ALL") || state.fileDisabled.has(slug)) {
    return true;
  }

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

  const workspaceConfig = await loadWorkspaceConfig(document.uri);
  const workspaceDisabled = getWorkspaceDisabledRules(workspaceConfig);

  const version = document.version;

  execFile(pythonPath, [analyzerPath, document.fileName], (err, stdout) => {
    if (err || document.isClosed || document.version !== version) return;

    try {
      const results = JSON.parse(stdout);
      const disabled = getInFileDisabledRules(document);
      const priorityMap = new Map<number, vscode.Diagnostic>();

      for (const r of results) {
        if (!r) continue;

        const ruleId = r.rule_id;
        if (!ruleId) continue;

        const line = Math.max(0, (r.line ?? 1) - 1);

        if (isDisabled(ruleId, line, disabled, workspaceDisabled)) continue;

        const rule = ruleMap[ruleId];
        const severity = mapSeverity(rule?.severity);

        const startCol = Math.max(0, (r.column ?? 1) - 1);

        const endLine = Math.max(0, (r.end_line ?? r.line ?? 1) - 1);
        const endCol = Math.max(startCol, (r.end_column ?? r.column ?? 1) - 1);

        const range = new vscode.Range(
          new vscode.Position(line, startCol),
          new vscode.Position(endLine, endCol),
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
