import * as vscode from "vscode";
import { ruleMap } from "@pyquit/rules";

export function registerRulePanelCommand(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand(
    "pyquit.showRuleDetails",
    (ruleId: string) => {
      openRulePanel(ruleId);
    },
  );

  context.subscriptions.push(disposable);
}

function openRulePanel(ruleId: string) {
  const rule = ruleMap[ruleId];

  const panel = vscode.window.createWebviewPanel(
    "pyquitRuleDetails",
    `Rule: ${ruleId}`,
    vscode.ViewColumn.Beside,
    { enableScripts: false },
  );

  panel.webview.html = getHtml(ruleId, rule);
}

function getHtml(ruleId: string, rule: any): string {
  return `
    <!DOCTYPE html>
    <html>
      <body style="font-family: sans-serif; padding: 20px;">
        <h1>${rule?.title || ruleId}</h1>
        <h3>Severity: ${rule?.severity}</h3>
        <p>${rule?.description || "No description available."}</p>
      </body>
    </html>
  `;
}
