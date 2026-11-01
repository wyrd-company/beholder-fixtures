# beholder-fixtures

Fixtures for beholder efficacy evaluation and development.

[Beholder](https://github.com/wyrd-company/beholder) indexes source code and
records what each name in it refers to. This repository holds the controlled
source that Beholder is measured against: 84 small fixture projects in six
languages, and for each project a semantic-oracle dataset that states the
facts a correct indexer finds in it.

| Language | Projects |
| --- | ---: |
| C# | 14 |
| Dart | 12 |
| Go | 8 |
| Python | 14 |
| Rust | 17 |
| TypeScript | 19 |

## Layout

| Path | Contents |
| --- | --- |
| `fixtures/<language>/projects/<project>/` | One fixture project. It builds, lints and tests offline with its own `Taskfile.yml`, and lists the checklist items it covers in `coverage.md`. |
| `fixtures/<language>/projects/<project>/semantic-oracle.yml` | The project's semantic-oracle dataset. |
| `fixtures/<language>/ground-rules.md` | The rules every project in that language follows. |
| `fixtures/<language>/plan/`, `reviews/`, `prompts/` | The reviewed corpus plan, its reviews, and the prompts used to plan and review it. |
| `fixtures/<language>/coverage.md` | Which project covers each checklist item. |
| `reports/<language>/` | Independent language-feature research and the synthesized checklist (`synthesis/checklist.md`) that defines the corpus scope. |
| `*.md` at the root | The research and synthesis prompts that produced the reports. |

## Using the fixtures

Each project is self-contained. From a project directory:

```sh
task build
task lint
task test
```

Each language's `ground-rules.md` names the toolchain version the projects
require. No task downloads anything: third-party dependencies are vendored.

Semantic-oracle datasets are written and checked with Beholder's
`semantic-oracle` tools. The format is specified in Beholder's
`docs/specifications/semantic-oracle-model.yml` and the language profiles
beside it. Beholder includes this repository as a git submodule that it
initializes only when a task needs the fixtures.

## Repository checks

```sh
task check
```

`task notices` regenerates `THIRD-PARTY-NOTICES.md` after a vendored package
is added, removed or upgraded.

## License

The fixture projects, datasets, plans and reports written for this repository
are licensed under the [MIT License](LICENSE).

Vendored third-party packages keep their own licenses. They are listed with
their licenses in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md), and each
package's own license and notice files stay beside it.
