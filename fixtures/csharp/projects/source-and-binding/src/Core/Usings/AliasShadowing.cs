using SourceBinding.Core.Namespaces.Open;
using ContributionA = SourceBinding.Core.Namespaces.Open.ContributionB;

namespace SourceBinding.Core.Usings;

public static class AliasShadowingDemo
{
    // Alias ContributionA shadows the imported type SourceBinding.Core.Namespaces.Open.ContributionA.
    // Resolved via alias, this refers to ContributionB.
    public static string ViaShadowingAlias() => ContributionA.Describe();

    // Original ContributionB remains accessible directly.
    public static string ViaOriginal() => ContributionB.Describe();

    // Namespace/type collision resolution via alias vs import: using alias wins.
    public static string DescribeAliasWins() => ViaShadowingAlias() + "+" + ViaOriginal();
}
