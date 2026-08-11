// CS-CAN-013: one physical source compiled into two assemblies with distinct symbols.
// This file is linked into Core and Companion. Conditional constants give each compilation a different shape.
namespace Catalog.Packages.Shared;

public sealed class SharedModel
{
    public string Origin => "SharedModel";

#if CORE_COMPILATION
    public const string CompilationTag = "Core";
    public int CoreOnlyValue => 100;
    public string Describe() => $"Core:{CoreOnlyValue}";
#elif COMPANION_COMPILATION
    public const string CompilationTag = "Companion";
    public int CompanionOnlyValue => 200;
    public string Describe() => $"Companion:{CompanionOnlyValue}";
#else
    public const string CompilationTag = "Unknown";
    public string Describe() => "Unknown";
#endif
}
