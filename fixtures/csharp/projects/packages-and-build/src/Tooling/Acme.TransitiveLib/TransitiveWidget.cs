namespace Acme.TransitiveLib;

public sealed class TransitiveWidget
{
    public string Label { get; set; } = "transitive";
    public string Describe() => $"TransitiveWidget:{Label}";
}
