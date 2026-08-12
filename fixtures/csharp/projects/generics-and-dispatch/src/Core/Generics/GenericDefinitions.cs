namespace GenericsAndDispatch.Core.Generics;

// Same-named type arities and generic-base substitution.
public class Box<T>
{
    public T Value { get; set; }

    public Box(T value) => Value = value;

    public static int Instances;
}

public class Box<T1, T2>
{
    public T1 First { get; }
    public T2 Second { get; }

    public Box(T1 first, T2 second)
    {
        First = first;
        Second = second;
    }

    public static int Instances;
}

// Nested generics with independent arity and captured outer parameter.
public class Outer<TOuter>
{
    public TOuter OuterValue { get; }

    public Outer(TOuter value) => OuterValue = value;

    public class Inner<TInner>
    {
        public TOuter OuterCaptured { get; }
        public TInner InnerValue { get; }

        public Inner(TOuter outer, TInner inner)
        {
            OuterCaptured = outer;
            InnerValue = inner;
        }
    }

    public class InnerWithOuter : Box<TOuter>
    {
        public InnerWithOuter(TOuter value) : base(value) { }
    }
}

public class DerivedBox<T> : Box<T>
{
    public DerivedBox(T value) : base(value) { }
}

// Same-named method arities.
public static class Factory
{
    public static Box<T> Create<T>(T value) => new(value);

    public static Box<T1, T2> Create<T1, T2>(T1 first, T2 second) => new(first, second);

    public static TResult Transform<TSource, TResult>(TSource source, Func<TSource, TResult> selector) =>
        selector(source);

    public static TResult Convert<TSource, TResult>(TSource source, Func<TSource, TResult> selector) where TResult : new() =>
        selector(source);
}

// Static fields per closed construction.
public static class Counter<T>
{
    public static int Count;
    public static string Name => typeof(T).Name;
}

public static class GenericExercises
{
    public static void Run()
    {
        // Inferred and explicit generic calls.
        var inferred = Factory.Create(42);
        var explicitSingle = Factory.Create<int>(42);
        var explicitDouble = Factory.Create<int, string>(42, "answer");
        var inferredDouble = Factory.Create(7, "seven");

        // Nested generic construction.
        var outer = new Outer<int>(10);
        var inner = new Outer<int>.Inner<string>(10, "inner");
        var derived = new DerivedBox<string>("derived");

        // Open and closed type reflection, static per-construction state.
        Type openSingle = typeof(Box<>);
        Type closedSingle = typeof(Box<int>);
        Type openDouble = typeof(Box<,>);
        Type closedDouble = typeof(Box<int, string>);
        Type nestedOpen = typeof(Outer<>.Inner<>);
        Type nestedClosed = typeof(Outer<int>.Inner<string>);

        // Type-parameter identity versus metadata name.
        string openName = openSingle.Name;
        string closedName = closedSingle.Name;

        Counter<int>.Count = 1;
        Counter<string>.Count = 2;
        Counter<int>.Count++;

        // Runtime code-sharing versus non-erased constructed identity.
        Type def = typeof(Box<>);
        Type closedInt = def.MakeGenericType(typeof(int));
        Type closedString = def.MakeGenericType(typeof(string));
        bool sameDefinition = closedInt.GetGenericTypeDefinition() == closedString.GetGenericTypeDefinition();
        bool distinctHandles = closedInt.TypeHandle.Value != closedString.TypeHandle.Value;
        bool distinctTypes = closedInt != closedString;
        IntPtr handleInt = closedInt.TypeHandle.Value;
        IntPtr handleString = closedString.TypeHandle.Value;

        // MethodHandle sharing for generic method definition versus distinct instantiation.
        var methodDef = typeof(Factory).GetMethod(nameof(Factory.Create), System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static)!.GetGenericMethodDefinition();
        var methodInt = methodDef.MakeGenericMethod(typeof(int));
        var methodString = methodDef.MakeGenericMethod(typeof(string));
        IntPtr mHandleInt = methodInt.MethodHandle.Value;
        IntPtr mHandleString = methodString.MethodHandle.Value;

        _ = inferred;
        _ = explicitSingle;
        _ = explicitDouble;
        _ = inferredDouble;
        _ = outer;
        _ = inner;
        _ = derived;
        _ = openSingle;
        _ = closedSingle;
        _ = openDouble;
        _ = closedDouble;
        _ = nestedOpen;
        _ = nestedClosed;
        _ = openName;
        _ = closedName;
        _ = sameDefinition;
        _ = distinctHandles;
        _ = distinctTypes;
        _ = handleInt;
        _ = handleString;
        _ = mHandleInt;
        _ = mHandleString;
    }

    public static Type GetDefinition<T>(Box<T> box) => box.GetType().GetGenericTypeDefinition();

    public static Type GetConstruction<T>() => typeof(Box<T>);
}
