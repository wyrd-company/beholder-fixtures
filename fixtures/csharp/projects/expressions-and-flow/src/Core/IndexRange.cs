namespace ExpressionsFlow.Core;

public sealed class CustomSliceable
{
    private readonly int[] _data;

    public CustomSliceable(int[] data) => _data = data;

    public int Length => _data.Length;

    public int Count => _data.Length;

    public int this[int index] => _data[index];

    public int this[Index index] => _data[index];

    public CustomSliceable this[Range range]
    {
        get
        {
            var (offset, length) = range.GetOffsetAndLength(_data.Length);
            return new CustomSliceable(_data[offset..(offset + length)]);
        }
    }

    public CustomSliceable Slice(int start, int length) => new(_data[start..(start + length)]);

    public int[] ToArray() => (int[])_data.Clone();
}

public static class IndexRange
{
    // Array slicing with Index and Range
    public static int[] ArraySlice()
    {
        int[] data = [1, 2, 3, 4, 5];
        int last = data[^1];
        int[] middle = data[1..4];
        int[] fromStart = data[..3];
        int[] toEnd = data[2..];
        int[] full = data[..];
        _ = last;
        _ = fromStart;
        _ = toEnd;
        _ = full;
        return middle;
    }

    // String slicing
    public static string StringSlice()
    {
        string text = "stock-items";
        string slice = text[2..7];
        char last = text[^1];
        Range r = 0..5;
        string viaRange = text[r];
        _ = last;
        _ = viaRange;
        return slice;
    }

    // Span slicing (view versus copy)
    public static bool SpanIsView()
    {
        Span<int> span = stackalloc int[] { 1, 2, 3, 4 };
        Span<int> view = span[1..3];
        view[0] = 99;
        return span[1] == 99;
    }

    public static bool ArrayIsCopy()
    {
        int[] arr = [1, 2, 3, 4];
        int[] copy = arr[1..3];
        copy[0] = 99;
        return arr[1] != 99;
    }

    // Custom type with Index/Range/Length/Count and Slice
    public static CustomSliceable CustomSlicing()
    {
        var custom = new CustomSliceable([10, 20, 30, 40, 50]);
        CustomSliceable slice = custom[1..4];
        int viaIndex = custom[^2];
        CustomSliceable viaSpanLike = custom.Slice(0, 2);
        _ = viaIndex;
        _ = viaSpanLike;
        return slice;
    }

    public static int ImplicitIndex() => new CustomSliceable([5, 6, 7])[^1];

    public static int ImplicitRange()
    {
        var c = new CustomSliceable([1, 2, 3, 4]);
        return c[0..2].Length;
    }

    // From-end zero
    public static int[] FromEndZero()
    {
        int[] data = [1, 2, 3];
        // ^0 is one past the end; data[^0] would throw, but range with ^0 is valid end.
        int[] slice = data[0..^0];
        return slice;
    }

    // Integer indexer vs Index overload competition
    public static int OverloadCompetition()
    {
        var c = new CustomSliceable([10, 20, 30]);
        int byInt = c[1];
        int byIndex = c[new Index(1)];
        return byInt + byIndex;
    }

    // Object-initializer interaction: index assignment via initializer uses indexer setter if present
    public static CustomSliceable? InitializerInteraction()
    {
        // CustomSliceable has no setter, so index initializer is not applicable;
        // this demonstrates the shape requirement.
        return null;
    }

    public static List<int> ListWithIndexInitializer()
    {
        var list = new List<int> { 1, 2, 3 };
        list[^1] = 99;
        return list;
    }

    public static Dictionary<string, int> DictionaryNotSliceable()
    {
        var d = new Dictionary<string, int> { ["a"] = 1 };
        // d[0..1] is not valid shape; demonstrates missing shape members as diagnostic.
        return d;
    }

    // Boundary failures are diagnostics/runtime:
    //   int[] data = [1,2,3];
    //   int bad = data[10]; // IndexOutOfRangeException at runtime
    //   int[] badRange = data[5..10]; // ArgumentOutOfRangeException
    // Inaccessible/missing shape: type without Length/Count and without Range indexer cannot be sliced.
}

public static class SlicePatterns
{
    // Slicing within initializer-like context is not directly applicable;
    // provided to tie slice shape to initializer narrative.
    public static int[] ViaRangeVariable()
    {
        int[] data = [1, 2, 3, 4, 5];
        Range r = ^3..^1;
        return data[r];
    }
}
