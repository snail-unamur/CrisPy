import rules from "./rules.json";

export type RuleMeta = {
  title: string;
  description?: string;
  severity: "info" | "warning" | "error";
  category: string;
  docsPath: string;
};

export const ruleMap = rules as Record<string, RuleMeta>;
