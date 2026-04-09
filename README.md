# CrisPy

CrisPy is a rule-based static analysis platform combining a Python analyzer, VS Code extension, and interactive documentation to detect and explain Python code issues, with a focus on performance.

## Why CrisPy?

- Detect performance issues early in development
- Provide clear explanations for each rule
- Seamless integration with VS Code
- Centralized and reusable rule system

# Getting Started

This project is a **PNPM monorepo** managed with **Turborepo**.

**Benefits**:

- Incremental builds
- Task caching
- Parallel execution
- Faster CI pipelines

## Apps & Packages

- `apps/analyzer` → Python
- `apps/docs` → Next.js / React / TypeScript / MDX
- `apps/extension` → Node.js / VS Code / TypeScript
- `packages/rules` → Shared rules

## Prerequisites

- VS Code
- Python 3.10+
- Node.js 18+
- PNPM 8+ (npm install -g pnpm)
- Git

## Clone & Install

```bash
# Clone the repository
git clone <repository-url>
cd crispy

# Install dependencies
pnpm install

# Setup environment variables
cp .env.example .env
```

## Development Setup

### Project structure

```bash
apps/
├── analyzer/
│   └── src/
│       ├── engine/       # The main analyzer with the list of all rules
│       ├── models/       # the rules model
│       ├── rules/        # Contains all rules, each rule in a separate file
│       ├── main.py       # Application entry point
│       └── test.py       # The test file to test rules
│
├── docs/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── ui/         # Shadcn UI components
│   │   │   └── Layout.tsx  # The main application layout
│   │   ├── assets/         # Static assets
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # service layer
│   │   ├── types/          # Frontend-specific types
│   │   └── pages/          # Dynamic next js pages
│   │       ├── rules/      # Contains all rules in markdown each rule in a separate file (.mdx)
│   │       └── index.tsx   # Application entry page
│   └── tests/              # Frontend tests
│
├── extension/               # The vscode extension code
│
packages/
└── rules/
       └── src/
            ├── rules.json    # Rules definition
            └── index.ts      # Export all shared rules
```

### Application Overview

#### Analyzer (apps/analyzer)

Python-based static analysis engine:

- Executes rule set
- Parses input code
- Produces diagnostics / reports

Run locally:

```sh
cd apps/analyzer
python src/main.py
```

#### Docs (apps/docs)

Documentation platform:

- Next.js + React
- MDX-based rule documentation
- Shadcn UI components

Run locally:

```sh
cd apps/docs
pnpm dev
```

#### Extension (apps/extension)

VS Code extension:

- Integrates analyzer into editor
- Provides real-time feedback

Run locally:

```sh
cd apps/extension
pnpm build
# then launch via VS Code Extension Host
```

#### Shared Rules (packages/rules)

- Centralized rule definitions
- Shared across analyzer, docs, and extension

## Workflow

### Before Starting Work

Make sure you are up to date with the dev branch:

```shell
git pull origin dev
```

### Before Every Push

Always build the project to ensure everything compiles correctly:

```shell
pnpm run build
```

### After Every Pull

Install dependencies at root:

```shell
pnpm install
```

## Contribution Guidelines

- Pull latest changes from dev
- Create a feature branch
- Implement your changes
- Run build and tests
- Submit a PR to dev

## Rule Naming Convention

Each rule in CrisPy follows a consistent naming convention across the documentation, analyzer, and configuration.

### Rule ID Format

All rules use a unique identifier:

```
PY<rule_number>
```

Example:

- PY001
- PY002

### Documentation (MDX)

Each rule is documented in an .mdx file:

```
py<rule_number>.mdx
```

- Example:
  - py001.mdx
- Located in: `apps/docs/src/pages/rules/`
- Used for: detailed explanations, examples, and usage guidance

### Analyzer (Python)

In the Python analyzer, rules follow this format:

```
PY<rule_number>_<rule_name>
```

- Example:
  - PY001_numpy_array
- Located in: `apps/analyzer/src/rules/`
- Contains the rule implementation logic

### Shared Configuration (rules.json)

Each rule is registered in rules.json using its ID:

```json
{
  "PY001": {
    "title": "Prefer NumPy Array",
    "severity": "info",
    "docsPath": "/rules/py001",
    "category": "performance"
  }
}
```

- `title` → Human-readable rule name

- `severity` → info | warning | error

- `docsPath` → to documentation page

- `category` → e.g., performance, readability

### .crispy Configuration Files

CrisPy configuration files (`.crispy`) allow you to customize rule severity levels per project:

```json
{
  "prefer-numpy-array": "warning",
  "avoid-mutable-default-args": "danger",
  "prefer-explicit-typing": "off"
}
```

**How It Works:**

- Config keys use rule `slug` (kebab-case format)
- Values are severity levels: `off`, `info`, `warning`, `danger`
- VS Code provides **autocomplete** for all available rules

**Schema Generation:**
The VS Code schema (`apps/extension/language/crispy.schema.json`) is **automatically generated** from `rules.json`:

```bash
# Generate schema manually
pnpm --filter @crispy/rules generate-schema

# Or as part of the build
pnpm build:rules
```

The schema generation ensures:

- Autocomplete stays in sync with rules
- New rules are automatically available for configuration
- Single source of truth in `rules.json`
- No manual schema maintenance needed

### Summary Mapping

| Layer      | Format            | Example              |
| ---------- | ----------------- | -------------------- |
| Rule ID    | `PY001`           | `PY001`              |
| Docs (MDX) | `py001.mdx`       | `py001.mdx`          |
| Analyzer   | `PY001_<name>`    | `PY001_numpy_array`  |
| Config     | `rules.json` key  | `"PY001"`            |
| Config     | `slug` in .crispy | `prefer-numpy-array` |

## Notes

- Keep rules consistent between packages/rules, apps/analyzer, and apps/docs

- Each rule should have:
  - Implementation (Python)
  - Definition (rules.json)
  - Documentation (.mdx)
- Follow monorepo best practices: avoid duplication, prefer shared packages
