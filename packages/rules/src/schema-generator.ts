import * as fs from "node:fs";
import * as path from "node:path";
import rulesData from "./rules.json";

interface Rule {
  title: string;
  slug: string;
  severity: string;
  category: string;
  docsPath: string;
}

interface SchemaProperty {
  enum: string[];
  description: string;
}

interface JSONSchema {
  $schema: string;
  title: string;
  type: string;
  properties: Record<string, SchemaProperty>;
  additionalProperties: boolean;
}

function generateSchema(): JSONSchema {
  const properties: Record<string, SchemaProperty> = {};

  // Iterate through all rules and create schema properties
  Object.entries(rulesData).forEach(([ruleId, rule]) => {
    const typedRule = rule as Rule;
    properties[typedRule.slug] = {
      enum: ["off", "info", "warning", "danger"],
      description: `${ruleId}: ${typedRule.title}`,
    };
  });

  const schema: JSONSchema = {
    $schema: "http://json-schema.org/draft-07/schema#",
    title: "CrisPy Rules Configuration",
    type: "object",
    properties,
    additionalProperties: false,
  };

  return schema;
}

function writeSchema(schema: JSONSchema, outputPath: string): void {
  const outputDir = path.dirname(outputPath);

  // Create directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Write schema with pretty formatting
  fs.writeFileSync(outputPath, JSON.stringify(schema, null, 2) + "\n");
  console.log(`✓ Schema generated successfully at: ${outputPath}`);
}

// Main execution
const outputPath = path.resolve(
  __dirname,
  "../../..",
  "apps/extension/language/crispy.schema.json",
);

try {
  const schema = generateSchema();
  writeSchema(schema, outputPath);
  console.log(`✓ Generated schema for ${Object.keys(rulesData).length} rules`);
  process.exit(0);
} catch (error) {
  console.error("✗ Error generating schema:", error);
  process.exit(1);
}
