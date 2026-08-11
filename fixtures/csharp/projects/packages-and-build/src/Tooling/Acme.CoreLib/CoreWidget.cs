namespace Acme.CoreLib;

public sealed class CoreWidget
{
    public string Label { get; set; } = "core";
    public string Describe() => $"CoreWidget:{Label}";
}

public sealed class CoreHelper
{
    public static string HelperMethod() => "helper";
}
