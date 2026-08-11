// CS-CAN-099: version-gated syntax under LangVersion latest — uses C# 11+ and C# 12 features.
// Demonstrates file-local type, required members, collection expressions — gates not available in fixed 10.0.
namespace Catalog.Packages.LangLatest;

file sealed class FileLocalHelper
{
    public static string Note => "file-local";
}

public sealed class LatestFeature
{
    // C# 12 collection expression (latest)
    public static int[] Numbers => [1, 2, 3];

    // C# 11 file-local type is referenced above; required member (C# 11) shown below.
    public required string RequiredName { get; init; }

    public string Describe() => $"{RequiredName}:{string.Join(",", Numbers)}:{FileLocalHelper.Note}";

    public const string LanguageVersion = "latest";
    public const string SdkVersion = "10.0.110";
}
