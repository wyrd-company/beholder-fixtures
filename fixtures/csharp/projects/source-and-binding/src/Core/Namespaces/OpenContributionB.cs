namespace SourceBinding.Core.Namespaces.Open;

// Contribution B to the same open namespace, same namespace as OpenContributionA.
public sealed class ContributionB
{
    public static string Describe() => "contribution B";
}

public sealed class NamespaceTypeCollision
{
    public static string FromB() => ContributionA.Describe() + "+" + ContributionB.Describe();
}
