# Vendored dependencies — interop-languages-and-testing

This directory vendors the third-party packages required for CS-CAN-117
(test discovery and framework-mediated invocation) plus the F# runtime
required by the non-C# CLI producer.

## Pinned versions

All versions are pinned to a single stable release and restored offline via
`nuget.config` (`local-vendor` → `./vendor/packages`).

| Package | Pinned version | Source | License | Project URL |
| --- | --- | --- | --- | --- |
| `xunit` | 2.8.1 | nuget.org `https://api.nuget.org/v3-flatcontainer/xunit/2.8.1/xunit.2.8.1.nupkg` | Apache-2.0 | https://github.com/xunit/xunit |
| `xunit.abstractions` | 2.0.3 | nuget.org | Apache-2.0 (MIT url) | https://github.com/xunit/xunit |
| `xunit.analyzers` | 1.14.0 | nuget.org | Apache-2.0 | https://github.com/xunit/xunit |
| `xunit.assert` | 2.8.1 | nuget.org | Apache-2.0 | https://github.com/xunit/xunit |
| `xunit.core` | 2.8.1 | nuget.org | Apache-2.0 | https://github.com/xunit/xunit |
| `xunit.extensibility.core` | 2.8.1 | nuget.org | Apache-2.0 | https://github.com/xunit/xunit |
| `xunit.extensibility.execution` | 2.8.1 | nuget.org | Apache-2.0 | https://github.com/xunit/xunit |
| `xunit.runner.visualstudio` | 2.8.1 | nuget.org | Apache-2.0 | https://github.com/xunit/xunit |
| `Microsoft.NET.Test.Sdk` | 17.11.1 | nuget.org | MIT | https://github.com/microsoft/vstest |
| `Microsoft.CodeCoverage` | 17.11.1 | nuget.org | MIT | https://github.com/microsoft/vstest |
| `Microsoft.TestPlatform.ObjectModel` | 17.11.1 | nuget.org | MIT | https://github.com/microsoft/vstest |
| `Microsoft.TestPlatform.TestHost` | 17.11.1 | nuget.org | MIT | https://github.com/microsoft/vstest |
| `Newtonsoft.Json` | 13.0.1 | nuget.org | MIT | https://www.newtonsoft.com/json |
| `FSharp.Core` | 10.0.110 | SDK 10.0.110 `FSharp/library-packs` (`/usr/lib/dotnet/sdk/10.0.110/FSharp/library-packs/FSharp.Core.10.0.110.nupkg`) | MIT | https://github.com/dotnet/fsharp |

The stable xUnit **v2** line is used intentionally; xUnit v3 and
`Microsoft.Testing.Platform` are unresolved in CS-GAP-010 and are not used.

## Offline feasibility

- `nuget.config` clears all upstream sources and adds only `./vendor/packages`.
- `dotnet restore --ignore-failed-sources` succeeds offline because every
  package and its transitive closure is present in `vendor/packages`.
- `dotnet build --no-restore` and `dotnet test --no-restore` perform no
  downloads.
- MSBuild properties and targets are carried inside the `.nupkg` files
  themselves; no additional SDK imports are required.

## Licenses and notices

Per-package license records are in `vendor/licenses/*.LICENSE.txt` (derived
from the `.nuspec` `<license>` and `<licenseUrl>` fields). The applicable
license texts are vendored locally at `vendor/licenses/MIT.txt` (MIT) and
`vendor/licenses/Apache-2.0.txt` (Apache-2.0). The original `LICENSE.md` from
`Newtonsoft.Json` and `ThirdPartyNotices.txt` from `Microsoft.CodeCoverage` and
`Microsoft.TestPlatform.TestHost` are preserved as
`newtonsoft.json.13.0.1.LICENSE.md`,
`microsoft.codecoverage.17.11.1.ThirdPartyNotices.txt`, and
`microsoft.testplatform.testhost.17.11.1.ThirdPartyNotices.txt`.
The per-package records map each package to its `LocalLicense` file and
`VendoredPackage`, with flat-container provenance verified.
