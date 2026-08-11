namespace ExpressionsFlow.CSharp11;

public static class ListPatterns
{
    // List pattern (C# 11) over arrays and lists
    public static bool IsSingle<T>(T[] values) => values is [var single];

    public static bool IsFirstTwo(int[] values) => values is [1, 2, ..];

    public static bool HasMiddle(int[] values) => values is [_, .. var middle, _] && middle.Length > 0;

    // Slice pattern within list pattern
    public static string Classify(int[] values) => values switch
    {
        [] => "empty",
        [var one] => $"one:{one}",
        [1, .., 9] => "starts-1-ends-9",
        [_, _, ..] => "at-least-two",
        _ => "other",
    };

    // Recursive + list pattern
    public static bool IsNested(int[][] matrix) => matrix is [[1, 2], [3, 4]];

    // Raw string interpolation (C# 11)
    public static string RawInterpolation(string label) => $"""raw:{label}""";

    public static string RawMultiline(string label) =>
        $"""
        item:{label}
        end
        """;
}
