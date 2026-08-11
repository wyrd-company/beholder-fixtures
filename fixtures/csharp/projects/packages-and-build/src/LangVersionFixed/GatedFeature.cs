// CS-CAN-099: version-gated syntax under fixed LangVersion 10.0.
// Uses only features available at C# 10 (record struct) without requiring latest/preview features like file-local types or collection expressions.
namespace Catalog.Packages.LangFixed;

public record struct FixedRecord(int Id, string Name)
{
    public string Describe() => $"{Id}:{Name}";
}

// Uses nullable enable and file-scoped namespace already in use; no latest-only syntax here.
// Conditional keyword availability: 'file' type modifier (C# 11) and collection expressions (C# 12) are not used in this fixed context.
public static class FixedFeature
{
    public static FixedRecord Create() => new(1, "fixed");
    public const string LanguageVersion = "10.0";
    public const string SdkVersion = "10.0.110";
}
