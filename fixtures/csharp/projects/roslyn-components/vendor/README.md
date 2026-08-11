# Vendored dependencies for roslyn-components

Offline restore uses `../nuget.config` (`clear` + `vendor` source + `globalPackagesFolder=./packages`).

## Pinned packages (brief § Dependency needs)

| Package | Version | Source | License |
| --- | --- | --- | --- |
| `Microsoft.CodeAnalysis.CSharp` | 4.14.0 | https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/4.14.0 | MIT — https://licenses.nuget.org/MIT |
| `Microsoft.CodeAnalysis.Common` | 4.14.0 | transitive of above — https://www.nuget.org/packages/Microsoft.CodeAnalysis.Common/4.14.0 | MIT |
| `Microsoft.CodeAnalysis.Analyzers` | 3.11.0 | https://www.nuget.org/packages/Microsoft.CodeAnalysis.Analyzers/3.11.0 | MIT |
| `NETStandard.Library` | 2.0.3 | https://www.nuget.org/packages/NETStandard.Library/2.0.3 | MIT — dotnet/standard LICENSE.TXT |

Source and license files are extracted under `licenses/` (`*.nupkg` preserved with NuGet + MSBuild metadata).
`THIRD-PARTY-NOTICES` / `ThirdPartyNotices` files are retained per package.

## Transitive netstandard2.0 closure for offline component build

The `netstandard2.0` target of `Microsoft.CodeAnalysis.CSharp/Common` 4.14.0
declares the following additional dependencies. They are vendored alongside the
named packages so that `dotnet restore` with `nuget.config:clear` succeeds
without network access. All are MIT.

| Package | Version |
| --- | --- |
| `System.Collections.Immutable` | 9.0.0 |
| `System.Reflection.Metadata` | 9.0.0 |
| `System.Memory` | 4.5.5 |
| `System.Buffers` | 4.5.1 |
| `System.Numerics.Vectors` | 4.5.0 |
| `System.Runtime.CompilerServices.Unsafe` | 6.0.0 |
| `System.Text.Encoding.CodePages` | 7.0.0 |
| `System.Threading.Tasks.Extensions` | 4.5.4 |
| `Microsoft.NETCore.Platforms` | 1.1.0 (via `NETStandard.Library`) |
