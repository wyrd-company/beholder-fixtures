namespace SourceBinding.Core.Namespaces.Open;

// Contribution A to the same open namespace.
public sealed class ContributionA
{
    public static string Describe() => "contribution A";
}

public static class OpenNamespaceExtensionsA
{
    public static string ExtendA(this ContributionA value) => "extended A";
}
