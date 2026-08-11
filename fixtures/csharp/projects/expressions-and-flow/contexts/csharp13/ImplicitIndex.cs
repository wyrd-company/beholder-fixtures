namespace ExpressionsFlow.CSharp13;

public static class ImplicitIndex
{
    // Implicit index initializer (C# 13): allows index-from-end in collection initializer context
    public static Dictionary<string, int> DictionaryWithIndex()
    {
        return new Dictionary<string, int>
        {
            ["alpha"] = 1,
            ["beta"] = 2,
        };
    }

    // C# 13 also permits ^ in initializer index expressions with suitable collection
    public static List<int> ListWithFromEnd()
    {
        var list = new List<int> { 10, 20, 30 };
        list[^1] = 99;
        list[^2] = 88;
        return list;
    }

    public static Dictionary<string, int> WithImplicitFromEnd()
    {
        var items = new List<int> { 1, 2, 3, 4 };
        items[^1] = 40;
        return new Dictionary<string, int>
        {
            ["first"] = items[0],
            ["last"] = items[^1],
        };
    }
}
