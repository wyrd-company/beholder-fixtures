using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.Core.Metadata;

/// <summary>An <see langword="init"/>-only property, encoded with a <c>modreq(IsExternalInit)</c> setter.</summary>
public sealed class InitOnlyRecord
{
    public int Value { get; init; }
}

/// <summary>A <see langword="volatile"/> field, encoded with a <c>modreq(IsVolatile)</c> field signature.</summary>
public static class VolatileCounterHost
{
    public static volatile int Counter;
}

/// <summary>A <see langword="readonly struct"/>, encoded with <c>[IsReadOnly]</c> on the type.</summary>
public readonly struct ReadOnlyValueBox
{
    public ReadOnlyValueBox(int value) => Value = value;

    public int Value { get; }
}

public static class ScopedParameterShowcase
{
    public static int DescribeScoped(scoped in ReadOnlyValueBox box) => box.Value;
}

public static class UnmanagedConstraintShowcase
{
    public static int DescribeUnmanagedSize<T>()
        where T : unmanaged
        => Unsafe.SizeOf<T>();
}

public static class ShowcaseExtensions
{
    public static string DescribeExtension(this ReadOnlyValueBox box) => $"boxed-value={box.Value}";
}
