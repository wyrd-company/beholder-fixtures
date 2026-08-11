using System.Collections.Generic;
using static System.Math;
using AcmeAlias = SourceBinding.Core.Namespaces.Open.ContributionA;
using IntMap = System.Collections.Generic.Dictionary<int, string>;
using NumberList = System.Collections.Generic.List<int>;
using StringMap = System.Collections.Generic.Dictionary<string, string>;

namespace SourceBinding.Core.Usings;

public static class UsingDirectiveSurface
{
    // Namespace import, using static, and alias.
    public static int AliasAndStatic()
    {
        var map = new IntMap();
        map[1] = "one";
        int abs = Abs(-5); // from using static System.Math
        string viaAlias = AcmeAlias.Describe();
        _ = viaAlias;
        return map.Count + abs;
    }

    // Generic and tuple aliases resolved via C# 12 alias-any-type (primary in contexts/csharp12).
    // Here we use them in latest context as well.
    public static (int, string) TupleAlias((int, string) value) => value;

    // Root qualification with global::.
    public static string RootQualified()
    {
        return global::SourceBinding.Core.Namespaces.GlobalNamespaceType.Describe();
    }

    // Extern-root-style qualification via global::System.
    public static int GlobalSystemInt() => global::System.Math.Abs(-3);

    public static void ResolvedAmbiguity()
    {
        // Alias shadowing: local alias AcmeAlias shadows any other ContributionA import.
        AcmeAlias local = new AcmeAlias();
        _ = local;

        var numbers = new NumberList { 1, 2, 3 };
        var strings = new StringMap { ["k"] = "v" };
        _ = numbers;
        _ = strings;
    }
}
