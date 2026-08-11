namespace Acme.Graph.Core;

public sealed class TransitType
{
    public string Source => "Graph.Core";
    public string Describe() => "Transit type from core layer";
}

public sealed class CoreHelper
{
    public static string Label => "core-helper";
}
