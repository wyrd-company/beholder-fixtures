namespace GenericsAndDispatch.Core.Dispatch;

public sealed class Container
{
    public int Value;
    public Container(int value) => Value = value;
}

public static class ByRefExercises
{
    public static void Swap(ref int left, ref int right) => (left, right) = (right, left);

    public static bool TryDivide(int dividend, int divisor, out int result)
    {
        if (divisor == 0)
        {
            result = 0;
            return false;
        }

        result = dividend / divisor;
        return true;
    }

    public static int Read(in int value) => value;

    public static ref readonly int ReadOnlyRef(in int value) => ref value;

    public static ref int FindMax(ref int a, ref int b) => ref a > b ? ref a : ref b;

    public static ref int ConditionalRef(bool chooseFirst, ref int first, ref int second) =>
        ref chooseFirst ? ref first : ref second;

    public static void AcceptScoped(scoped ref int value) => value++;

    public static void WithOutVar()
    {
        if (TryDivide(10, 2, out var result))
        {
            _ = result;
        }

        _ = TryDivide(9, 3, out int direct);
        _ = direct;
    }

    public static void Run()
    {
        int a = 1;
        int b = 2;
        Swap(ref a, ref b);
        _ = Read(in a);

        ref int max = ref FindMax(ref a, ref b);
        max++;

        int[] array = [10, 20, 30];
        ref int element = ref array[1];
        element = 99;

        ref readonly int ro = ref ReadOnlyRef(in a);
        _ = ro;

        scoped ref int scopedLocal = ref a;
        AcceptScoped(ref scopedLocal);

        bool first = true;
        ref int chosen = ref ConditionalRef(first, ref a, ref b);
        chosen++;

        // Temporary-to-in (rvalue promoted to temp for in param).
        _ = Read(42);

        // Defensive copy awareness: readonly struct with in param.
        ReadonlyPoint point = new(5, 6);
        _ = point.Distance(in point);

        // Metadata signature collision: by-value versus in overload choice.
        string byValue = Format("text");
        string byIn = Format(in a);
        _ = byValue;
        _ = byIn;

        WithOutVar();
    }

    private static string Format(string value) => value;
    private static string Format(in int value) => value.ToString();

    private static int FormatImpl(int value) => value;
}

public readonly struct ReadonlyPoint
{
    public int X { get; init; }
    public int Y { get; init; }
    public ReadonlyPoint(int x, int y) => (X, Y) = (x, y);
    public double Distance(in ReadonlyPoint other)
    {
        int dx = X - other.X;
        int dy = Y - other.Y;
        return Math.Sqrt(dx * dx + dy * dy);
    }
}

public ref struct SpanHolder
{
    public Span<int> Span;
    public SpanHolder(Span<int> span) => Span = span;
    public ref int At(int index) => ref Span[index];
}

public static class RefReturnUsage
{
    public static void RefLocalReassignment()
    {
        int x = 10;
        int y = 20;
        ref int r = ref x;
        r = 15;
        r = ref y;
        r = 25;
    }
}
