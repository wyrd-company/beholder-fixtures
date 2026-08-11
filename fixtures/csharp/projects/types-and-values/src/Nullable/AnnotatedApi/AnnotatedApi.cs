using System.Diagnostics.CodeAnalysis;

namespace Bakery.TypesAndValues.Nullable.AnnotatedApi;

// CS-CAN-024: nullable reference annotations — enabled scope, annotated API surface and flow attributes.

public sealed class AnnotatedInventory
{
    public string? FindByName(string name)
    {
        return name.Length > 0 ? name : null;
    }

    public bool TryFind(string name, [MaybeNullWhen(false)] out string result)
    {
        if (name.Length == 0)
        {
            result = null;
            return false;
        }

        result = name;
        return true;
    }

    public string GetOrDefault(string? input, string fallback) => input ?? fallback;

    public void SetLabel([DisallowNull] string? label)
    {
        _ = label ?? "default";
    }

    public string? LazyLabel
    {
        get => _lazyLabel;
        set => _lazyLabel = value ?? "fallback";
    }

    private string? _lazyLabel;

    [AllowNull]
    public string InitializedLabel
    {
        get => _initializedLabel;
        set => _initializedLabel = value ?? string.Empty;
    }

    private string _initializedLabel = string.Empty;

    [return: MaybeNull]
    public T FindFirst<T>(IEnumerable<T> source) where T : class
    {
        foreach (T item in source)
        {
            return item;
        }

        return null;
    }

    public bool TryGetCount(string? input, [NotNullWhen(true)] out string? normalized)
    {
        if (input is null)
        {
            normalized = null;
            return false;
        }

        normalized = input;
        return true;
    }

    [MemberNotNull(nameof(_initializedLabel))]
    public void EnsureInitialized()
    {
        _initializedLabel ??= "ready";
    }

    [MemberNotNullWhen(true, nameof(_lazyLabel))]
    public bool HasLazyLabel() => _lazyLabel is not null;

    public string GetInitializedLabel() => _initializedLabel;

#pragma warning disable CS8777
    [return: NotNull]
    public string? EnsureNotNull([NotNull] string? input) => input!;
#pragma warning restore CS8777

    [return: NotNullIfNotNull(nameof(source))]
    public string? MapIfNotNull(string? source) => source is null ? null : source.ToUpperInvariant();
}

public abstract class AnnotatedBase
{
    public virtual string? Describe(string? input) => input;

    public abstract string? AbstractLabel { get; set; }
}

public sealed class AnnotatedDerived : AnnotatedBase
{
    public override string Describe(string? input) => input ?? "default";

    public override string? AbstractLabel { get; set; }
}

public interface IAnnotatedContract
{
    string? Fetch(string? query);
}

public sealed class AnnotatedContractImpl : IAnnotatedContract
{
    public string? Fetch(string? query) => query;
}

public sealed class GenericBox<T>
{
    public T? Value { get; set; }

    public bool HasValue([NotNullWhen(true)] out T? value)
    {
        value = Value;
        return value is not null;
    }
}

public sealed class GenericStructBox<T> where T : struct
{
    public T? Value { get; set; }
}

public sealed class GenericNullableDemo
{
    public void ExerciseClassGeneric()
    {
        GenericBox<string> box = new() { Value = "rye" };
        if (box.HasValue(out string? value))
        {
            _ = value.Length;
        }
    }

    public void ExerciseStructGeneric()
    {
        GenericStructBox<int> box = new() { Value = 5 };
        _ = box.Value ?? 0;
    }
}

public sealed class ConstructorInitialization
{
    public string Label { get; set; }

    public string? OptionalNote { get; set; }

    public ConstructorInitialization(string label)
    {
        Label = label;
    }

    [MemberNotNull(nameof(Label))]
    public void InitializeIfNeeded()
    {
        Label ??= "fallback";
    }
}
