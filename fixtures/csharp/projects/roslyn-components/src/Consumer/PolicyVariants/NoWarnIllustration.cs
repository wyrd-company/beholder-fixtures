namespace Fixture.Roslyn.Policy;

// CS-CAN-102: NoWarn at project level (Consumer.csproj: <NoWarn>CS0436</NoWarn>).
// The duplicate-type scenario below would otherwise emit CS0436 (type in
// multiple assemblies) if the attribute type were shared via project
// reference without ReferenceOutputAssembly=false; NoWarn suppresses it
// without using pragmas or attributes.

// Also demonstrates TreatWarningsAsErrors / WarningsNotAsErrors boundary:
// compiler errors (e.g., CS0246 unknown type) cannot be downgraded to
// warnings via editorconfig severity or WarningsNotAsErrors. The fixture
// does not produce such errors; this file documents the boundary:
// a hypothetical "dotnet_diagnostic.CS0246.severity = suggestion" in
// .editorconfig would have no effect because compiler errors are not
// downgradable, unlike analyzer diagnostics such as RCAN001.
public sealed class NoWarnIllustration
{
    public string DescribeNoWarn() => "NoWarn suppresses CS0436 at the project level; see Consumer.csproj.";
}
