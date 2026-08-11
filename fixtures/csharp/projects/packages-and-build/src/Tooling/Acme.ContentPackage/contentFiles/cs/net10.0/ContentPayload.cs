// CS-CAN-097: source-distributing contentFiles asset — this C# source is emitted into the consumer assembly via NuGet contentFiles.
// It is not a referenced assembly type; the consumer compiles it as its own source.
namespace Acme.ContentPackage;

public sealed class ContentPayload
{
    public string Text { get; set; } = "contentFiles-payload";
    public string Describe() => $"ContentPayload:{Text}";
}
