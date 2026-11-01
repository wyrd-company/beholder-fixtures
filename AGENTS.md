# beholder-fixtures

Controlled source used to measure how accurately Beholder, and other
indexers, resolve the meaning of code. The repository holds 84 fixture
projects in six languages and their semantic-oracle datasets. Beholder
(`wyrd-company/beholder`) owns the dataset format, the authoring and
validation tools, and the evaluator; this repository owns the source and the
datasets.

## Vocabulary

| Term | Meaning |
| --- | --- |
| fixture project | One self-contained project under `fixtures/<language>/projects/<project>/`. It builds, lints and tests offline. |
| corpus | All fixture projects of one language, or of all six. |
| language-feature checklist | `reports/<language>/synthesis/checklist.md`. The research authority for what a language's corpus covers. |
| research report | One independent research pass under `reports/<language>/<source>/report.md`. Input to the checklist, not an authority. |
| ground rules | `fixtures/<language>/ground-rules.md`. The rules every project in that language follows. |
| plan | `fixtures/<language>/plan/`. The reviewed assignment of checklist items to projects. |
| coverage | `coverage.md`. Which checklist items a project, or a corpus, demonstrates. |
| build context | A declared combination of toolchain, target, configuration flags and features in which a project's source is valid. |
| vendored package | Third-party code copied into a project so that it builds offline. Listed in `THIRD-PARTY-NOTICES.md`. |
| first-party package | A package written for this repository that looks vendored, such as `@fixtures/*`, `Acme.*` or `example.invalid/*`. Listed in `scripts/first-party-packages.txt`. |
| semantic-oracle dataset | `<project>/semantic-oracle.yml`. The facts a correct indexer finds in the project: entities, references, relations, visibility and public API, each tied to exact source locations. |
| language profile | Beholder's per-language rules for what a dataset records. |
| pilot | One of the three datasets used to calibrate the v1 contract: Rust `modules-visibility-and-resolution`, TypeScript `package-publishing-ecosystem`, Python `plugin-content-library`. |

## Rules

- Fixture source is valid in its declared build contexts. Do not add invalid
  source, expected-failure programs or diagnostics as fixture content.
- Do not change fixture source to make a dataset or a validation pass. A
  dataset describes the source as it is.
- Dataset facts come from the source, the build configuration and the
  language specification. Never take them from SCIP, Beholder or any other
  indexer, or from coverage files or research reports.
- Themes and example values are generic and do not use code analysis,
  indexing or fixture evaluation as their domain.
- Vendored packages are pinned on purpose. Do not upgrade, remove or add one
  without a plan change. After any such change, run `task notices` and
  commit the regenerated `THIRD-PARTY-NOTICES.md`; `task check` fails
  otherwise.
- Keep each vendored package's license and notice files.
- `vendor/` and `node_modules/` directories are tracked. Never add them to a
  `.gitignore`.
- Line endings are never converted (`.gitattributes`), because datasets
  record byte digests of source files.
- A project has no dependency on another fixture project.
- Each language's ground rules govern its projects. Read them before
  changing a project.

## Checks

- In a project: `task build`, `task lint`, `task test`.
- At the root: `task check` (third-party notices).
- Datasets: Beholder's `semantic-oracle validate` and `semantic-oracle audit`,
  run from a Beholder checkout. See Beholder's
  `docs/semantic-oracle-authoring.md`.

## Repository

- Private until the corpus is accepted (`wyrd-company/beholder#19`).
- Work arrives through pull requests. Use conventional commits.
- The work is tracked in Beholder: epic `wyrd-company/beholder#13`.
