namespace Catalog.FunctionsAndAsync.CSharp12;

public delegate int DefaultFunc(int x = 5);

public static class DefaultLambdaHost
{
    public static DefaultFunc WithDefault(int fallback = 7) => (int x = 5) => x + fallback;

    public static DefaultFunc AttributedWithDefault() => [SampleMarker("default")] (int x = 5) => x * 2;

    public static int CallWithDefault(DefaultFunc fn) => fn();
}

[AttributeUsage(AttributeTargets.All)]
internal sealed class SampleMarkerAttribute : Attribute
{
    public SampleMarkerAttribute(string tag) => Tag = tag;
    public string Tag { get; }
}
