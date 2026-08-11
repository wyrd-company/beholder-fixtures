namespace GenericsAndDispatch.CSharp13;

public interface IValueSource
{
    int GetValue();
}

public struct RegularValue : IValueSource
{
    public int Value { get; init; }
    public RegularValue(int value) => Value = value;
    public int GetValue() => Value;
}

public ref struct RefValue : IValueSource
{
    public Span<int> Span;
    public RefValue(Span<int> span) => Span = span;
    public int GetValue() => Span.Length > 0 ? Span[0] : 0;
}

public static class AllowsRefStructAlgorithm
{
    public static int Run<T>(T source) where T : IValueSource, allows ref struct => source.GetValue();

    public static int RunWithTransform<T>(T source, Func<int, int> transform) where T : IValueSource, allows ref struct =>
        transform(source.GetValue());
}

public static class AllowsRefStructExercises
{
    public static void Run()
    {
        var regular = new RegularValue(42);
        int fromRegular = AllowsRefStructAlgorithm.Run(regular);

        Span<int> buffer = stackalloc int[3] { 7, 8, 9 };
        var refValue = new RefValue(buffer);
        int fromRef = AllowsRefStructAlgorithm.Run(refValue);
        int transformed = AllowsRefStructAlgorithm.RunWithTransform(refValue, v => v * 2);

        // Interface dispatch restriction: direct IValueSource boxing not allowed for ref struct; generic path avoids boxing.
        // Downlevel consumer would see constraint as metadata attribute.

        _ = fromRegular;
        _ = fromRef;
        _ = transformed;
    }
}
