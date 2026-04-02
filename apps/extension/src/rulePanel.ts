import * as vscode from "vscode";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkRehype from "remark-rehype";
import rehypeStringify from "rehype-stringify";
import rehypePrettyCode from "rehype-pretty-code";

async function renderMarkdown(content: string) {
  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype)
    .use(rehypePrettyCode, {
      theme: "github-dark",
      keepBackground: true,
    })
    .use(rehypeStringify)
    .process(content);

  return String(file);
}

export function registerRulePanelCommand(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand(
    "crispy.showRuleDetails",
    (ruleId: string) => {
      openRulePanel(context, ruleId);
    },
  );

  context.subscriptions.push(disposable);
}

async function openRulePanel(context: vscode.ExtensionContext, ruleId: string) {
  try {
    const fileName = `${ruleId.toLowerCase()}.mdx`;

    const ruleUri = vscode.Uri.joinPath(
      context.extensionUri,
      "..",
      "docs",
      "pages",
      "rules",
      fileName,
    );

    // AFTER: TAILWIND SUPPORT DIFFICULT WITH CDN
    // const cssUri = vscode.Uri.joinPath(
    //   context.extensionUri,
    //   "..",
    //   "docs",
    //   "global.css",
    // );
    // const stylesMainUri = panel.webview.asWebviewUri(cssUri);

    const fileData = await vscode.workspace.fs.readFile(ruleUri);
    const markdownContent = Buffer.from(fileData).toString("utf8");

    const panel = vscode.window.createWebviewPanel(
      "CrisPyRuleDetails",
      `Rule: ${ruleId.toUpperCase()}`,
      vscode.ViewColumn.Beside,
      { enableScripts: false },
    );

    const htmlContent = await renderMarkdown(markdownContent);
    panel.webview.html = getFullHtml(htmlContent);
  } catch (error) {
    vscode.window.showErrorMessage(`Documentation introuvable : ${ruleId}`);
    console.error(error);
  }
}

function getFullHtml(content: string): string {
  return `
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        :root {
          --padding-x: 2.5rem;
          --accent-color: #10b981; /* Emerald 500 */
        }

        body {
          font-family: var(--vscode-font-family, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif);
          font-size: var(--vscode-font-size, 14px);
          line-height: 1.6;
          color: var(--vscode-editor-foreground);
          background-color: var(--vscode-editor-background);
          margin: 0;
          padding: 0;
          overflow-x: hidden;
        }

        /* Container & Padding */
        main {
          max-width: 900px; /* Optimal reading width */
          margin: 0 auto;
          padding: 3rem var(--padding-x);
          box-sizing: border-box;
        }

        /* Typography / Prose Style */
        h1 { font-size: 1.75rem; font-weight: 750; color: var(--accent-color); margin-top: 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 0.5rem; }
        h2 { font-size: 1.5rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; color: var(--vscode-editor-foreground); border-bottom: 1px solid rgba(128,128,128,0.1); }
        h3 { font-size: 1.25rem; font-weight: 600; margin-top: 2rem; color: var(--vscode-editor-foreground); opacity: 0.9; }
        
        p { margin-bottom: 1.25rem; }
        
        /* Lists */
        ul, ol { margin-bottom: 1.25rem; padding-left: 1.5rem; }
        li { margin-bottom: 0.5rem; }
        li::marker { color: var(--accent-color); font-weight: bold; }

        /* Code Blocks (Rehype Pretty Code) */
        pre {
          background-color: #0d1117 !important;
          border-radius: 8px;
          padding: 1rem 0;
          margin: 1.5rem 0;
          overflow-x: auto;
        }

        figure[data-rehype-pretty-code-figure] {
            margin: 1.5rem 0;
            padding: 0;
            border-radius: 8px;
            overflow: hidden;
            background-color: #0d1117;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        figure[data-rehype-pretty-code-figure] * {
            background-color: transparent !important;
        }

        [data-rehype-pretty-code-figure] pre {
            background-color: transparent !important;
            margin: 0 !important;
            padding: 1rem 0;
            overflow-x: auto;
        }

        [data-line] {
            padding: 0 1.25rem;
            line-height: 1.5;
            border-left: 3px solid transparent;
        }

        [data-highlighted-line] {
            background-color: rgba(56, 139, 253, 0.1);
            border-left-color: #388bfd;
        }

        code {
          font-family: var(--vscode-editor-font-family, "Fira Code", monospace);
          font-size: 0.9em;
          counter-reset: line;

        }

        /* Inline Code */
        :not(pre) > code {
          background-color: rgba(128,128,128,0.15);
          padding: 0.2rem 0.4rem;
          border-radius: 4px;
          color: var(--accent-color);
        }

        /* Blockquotes (The X / Bad Practice style) */
        blockquote {
          border-left: 4px solid var(--accent-color);
          background: rgba(16, 185, 129, 0.05);
          margin: 2rem 0;
          padding: 1rem 1.5rem;
          border-radius: 0 8px 8px 0;
          font-style: italic;
        }

        /* Custom Bad/Good Practice classes if you use them */
        .bad-practice { border-left-color: #ef4444; background: rgba(239, 68, 68, 0.05); }
        .good-practice { border-left-color: #10b981; background: rgba(16, 185, 129, 0.05); }

        /* Links */
        a { color: var(--accent-color); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.2s; }
        a:hover { border-bottom-color: var(--accent-color); }
      </style>
    </head>
    <body>
      <main class="prose">
        ${content}
      </main>
    </body>
    </html>
  `;
}
