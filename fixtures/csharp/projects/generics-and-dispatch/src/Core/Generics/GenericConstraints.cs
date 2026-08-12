namespace GenericsAndDispatch.Core.Generics;

public interface IIdentifiable
{
    string Id { get; }
}

public abstract class EntityBase
{
    public string Tag { get; set; } = string.Empty;
}

public enum StatusKind { Unknown, Active, Inactive }

public delegate void WorkHandler(string message);

// Constraints exercising each kind with enabled operations.
public static class ConstraintSamples
{
    public static string NeedClass<T>(T value) where T : class => value.ToString() ?? string.Empty;

    public static string NeedNullableClass<T>(T? value) where T : class? => value?.ToString() ?? "null";

    public static T NeedStruct<T>(T value) where T : struct => value;

    public static unsafe int NeedUnmanaged<T>(T value) where T : unmanaged => sizeof(T);

    public static bool NeedNotNull<T>(T value) where T : notnull => value is not null;

    public static string NeedBase<T>(T value) where T : EntityBase => value.Tag;

    public static string NeedInterface<T>(T value) where T : IIdentifiable => value.Id;

    public static int NeedEnum<T>(T value) where T : struct, Enum => Convert.ToInt32(value);

    public static void NeedDelegate<T>(T handler, string message) where T : Delegate => handler.DynamicInvoke(message);

    public static T NeedNew<T>() where T : new() => new();

    public static T NeedDefault<T>(T? fallback = default) where T : struct => fallback ?? default;

    public static TResult NeedTypeParameter<TParam, TResult>(TParam value, Func<TParam, TResult> map)
        where TParam : IIdentifiable
        where TResult : TParam =>
        map(value);
}

public abstract class DefaultConstraintBase
{
    public abstract T Get<T>();
}

public class DefaultConstraintDerived : DefaultConstraintBase
{
    public override T Get<T>() where T : default => default!;
}

public sealed class SampleEntity : EntityBase, IIdentifiable
{
    public string Id => Tag;
    public SampleEntity() { }
    public SampleEntity(string tag) => Tag = tag;
}

public struct SampleStruct : IIdentifiable
{
    public string Id { get; init; }
    public SampleStruct(string id) => Id = id;
}

public class ConstraintAggregator<T>
    where T : class, IIdentifiable, new()
{
    public T Create(string id)
    {
        var instance = new T();
        return instance;
    }
}

public class NullableConstraintHost<T> where T : class? { public T? Value { get; set; } }

public class StructInterfaceHost<T> where T : struct, IIdentifiable { public string Read(T value) => value.Id; }

public class UnmanagedHost<T> where T : unmanaged { public T Zero => default; }

public class NotNullHost<T> where T : notnull { public T Value { get; } public NotNullHost(T value) => Value = value; }

public class TypeParameterChain<TOuter> where TOuter : IIdentifiable
{
    public TResult Project<TInner, TResult>(TInner inner, Func<TInner, TResult> map)
        where TInner : TOuter
        where TResult : class => map(inner);
}

public sealed class ConcreteEntity : EntityBase, IIdentifiable
{
    public string Id { get; init; }
    public ConcreteEntity(string id) => Id = id;
}

public static class ConstraintExercises
{
    public static void Run()
    {
        ConstraintSamples.NeedClass("text");
        ConstraintSamples.NeedNullableClass<string>("text");
        ConstraintSamples.NeedNullableClass<string>(null);
        ConstraintSamples.NeedStruct(42);
        ConstraintSamples.NeedUnmanaged(5);
        ConstraintSamples.NeedNotNull("value");
        ConstraintSamples.NeedBase(new SampleEntity("tag"));
        ConstraintSamples.NeedInterface(new SampleEntity("id"));
        ConstraintSamples.NeedEnum(StatusKind.Active);
        ConstraintSamples.NeedDelegate<WorkHandler>(msg => { _ = msg; }, "msg");
        var created = ConstraintSamples.NeedNew<SampleEntity>();
        _ = ConstraintSamples.NeedDefault<int>();
        var defaultImpl = new DefaultConstraintDerived();
        _ = defaultImpl.Get<int>();

        var host = new ConstraintAggregator<SampleEntity>();
        _ = host.Create("x");

        TypeParameterChain<IIdentifiable> chain = new();
        _ = chain.Project<SampleEntity, string>(new SampleEntity("p"), e => e.Id);
    }
}
