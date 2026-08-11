// CS-CAN-013: second compilation of the same physical SharedModel.cs file with a different symbol (COMPANION_COMPILATION).
using Catalog.Packages.Shared;

namespace Catalog.Packages.Companion;

public sealed class CompanionEntry
{
    public SharedModel Model { get; } = new();
    public string Tag => SharedModel.CompilationTag; // "Companion" here, "Core" in Core compilation
    public string Describe() => Model.Describe();
}
