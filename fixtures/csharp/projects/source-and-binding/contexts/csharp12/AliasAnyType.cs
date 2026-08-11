using IntMap12 = System.Collections.Generic.Dictionary<int, string>;
using Pair12 = (int Id, string Name);
using NumberList12 = System.Collections.Generic.List<int>;
using SpanAlias12 = System.Span<int>;

namespace SourceBinding.CSharp12;

public static class AliasAnyTypeDemo12
{
    public static IntMap12 BuildMap() => new IntMap12 { [1] = "one" };

    public static Pair12 BuildPair() => (1, "a");

    public static NumberList12 BuildList() => new NumberList12 { 1, 2, 3 };

    public static int ViaSpan(SpanAlias12 span) => span.Length;

    public static unsafe int PointerAlias(int* p) => *p;
}
