// CS-CAN-099: version-gated syntax under LangVersion preview — uses preview features gated behind preview.
// Uses C# 14 preview field keyword and extension members if available; otherwise latest features plus preview marker.
namespace Catalog.Packages.LangPreview;

// Demonstrates preview-gated compilation; the LangVersion preview enables preview syntax.
public class PreviewFeature
{
    // Preview field keyword (C# 14) — backing field for property without explicit field.
    // This syntax requires LangVersion preview in SDK 10.0.110 if still preview, or latest if already stable.
    // The declaration is valid and distinct under preview.
    public string Name
    {
        get => field;
        set => field = value;
    } = "preview";

    // Collection expression also latest but included to show richer surface in preview context.
    public static int[] Numbers => [4, 5, 6];

    public string Describe() => $"{Name}:{string.Join(",", Numbers)}";

    public const string LanguageVersion = "preview";
    public const string SdkVersion = "10.0.110";
}
