using IntDict = System.Collections.Generic.Dictionary<int, string>;
using StringList = System.Collections.Generic.List<string>;
using Pair = (int Id, string Label);
using IntSpan = System.Span<int>;
using IntArray = int[];

namespace SourceBinding.Core.Usings;

public static class AliasAnyTypeSurface
{
    // Tuple, generic, and array aliases (C# 12 alias-any-type).
    public static Pair CreatePair(int id, string label) => (id, label);

    public static IntDict BuildMap() => new IntDict { [1] = "one" };

    public static StringList BuildList() => new StringList { "a", "b" };

    public static int FromSpan(IntSpan span) => span.Length;

    public static IntArray CreateArray() => new int[] { 1, 2, 3 };

    public static int SumArray(IntArray array) => array.Length;

    // Unsafe pointer alias demonstration (requires unsafe context).
    public static unsafe int PointerAlias(int* pointer) => *pointer;
}
