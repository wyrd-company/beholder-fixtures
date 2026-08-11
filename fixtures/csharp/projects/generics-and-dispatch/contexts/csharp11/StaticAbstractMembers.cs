namespace GenericsAndDispatch.CSharp11;

public interface IFactory<T> where T : IFactory<T>
{
    static abstract T Create(int value);
    static abstract string Kind { get; }
    static virtual string Label => "factory";
}

public interface IAddable<T> where T : IAddable<T>
{
    static abstract T operator +(T left, T right);
    static abstract T operator checked +(T left, T right);
}

public interface IMathOps<T> where T : IMathOps<T>
{
    static abstract T Zero { get; }
    static abstract T One { get; }
    static abstract T Add(T left, T right);
}

public struct Counter : IFactory<Counter>, IAddable<Counter>, IMathOps<Counter>
{
    public int Value { get; init; }
    public Counter(int value) => Value = value;
    public static Counter Create(int value) => new(value);
    public static string Kind => "counter";
    public static Counter operator +(Counter left, Counter right) => new(left.Value + right.Value);
    public static Counter operator checked +(Counter left, Counter right) => new(checked(left.Value + right.Value));
    public static Counter Zero => new(0);
    public static Counter One => new(1);
    public static Counter Add(Counter left, Counter right) => left + right;
}

public struct Meter : IFactory<Meter>, IAddable<Meter>, IMathOps<Meter>
{
    public double Value { get; init; }
    public Meter(double value) => Value = value;
    public static Meter Create(int value) => new(value);
    public static string Kind => "meter";
    public static Meter operator +(Meter left, Meter right) => new(left.Value + right.Value);
    public static Meter operator checked +(Meter left, Meter right) => new(left.Value + right.Value);
    public static Meter Zero => new(0);
    public static Meter One => new(1);
    public static Meter Add(Meter left, Meter right) => left + right;
}

// Explicit static implementation and inherited default body.
public struct ExplicitCounter : IFactory<ExplicitCounter>
{
    public int Value;
    public ExplicitCounter(int value) => Value = value;
    static ExplicitCounter IFactory<ExplicitCounter>.Create(int value) => new(value);
    static string IFactory<ExplicitCounter>.Kind => "explicit";
}

public static class StaticAbstractExercises
{
    public static T Create<T>(int value) where T : IFactory<T> => T.Create(value);

    public static T Sum<T>(T left, T right) where T : IAddable<T> => left + right;

    public static T CheckedSum<T>(T left, T right) where T : IAddable<T> => checked(left + right);

    public static T GenericAdd<T>(T left, T right) where T : IMathOps<T> => T.Add(left, right);

    public static string GetKind<T>() where T : IFactory<T> => T.Kind;

    public static string GetLabel<T>() where T : IFactory<T> => T.Label;

    public static void Run()
    {
        var c1 = Create<Counter>(5);
        var c2 = Create<Meter>(7);
        var sum = Sum(new Counter(2), new Counter(3));
        var checkedSum = CheckedSum(new Counter(2), new Counter(8));
        var added = GenericAdd(Counter.Zero, Counter.One);
        string kind = GetKind<Counter>();
        string label = GetLabel<Counter>();
        var explicitInstance = Create<ExplicitCounter>(9);
        _ = c1; _ = c2; _ = sum; _ = checkedSum; _ = added; _ = kind; _ = label; _ = explicitInstance;
    }
}
