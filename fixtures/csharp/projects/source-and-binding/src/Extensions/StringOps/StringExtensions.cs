namespace SourceBinding.Extensions.StringOps;

public static class StringExtensions
{
    public static int WordCount(this string value) => value.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;

    public static string Surround(this string value, string prefix, string suffix) => $"{prefix}{value}{suffix}";

    public static int InstanceWinsDemo(this string value) => value.Length;
}
