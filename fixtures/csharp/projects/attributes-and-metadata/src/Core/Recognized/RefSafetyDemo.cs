using System.Diagnostics.CodeAnalysis;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// A <see langword="ref struct"/> whose instance <c>this</c> is scoped by
/// default, so returning a <see langword="ref"/> to its own field requires
/// the recognized ref-safety attribute <see cref="UnscopedRefAttribute"/> to
/// widen the returned reference's safe-context.
/// </summary>
public ref struct RefSafetyShowcase
{
    private int _value;

    public RefSafetyShowcase(int value) => _value = value;

    [UnscopedRef]
    public ref int GetValueRef() => ref _value;
}

public static class RefSafetyUsage
{
    public static int DescribeUnscopedRef()
    {
        var showcase = new RefSafetyShowcase(7);
        ref var value = ref showcase.GetValueRef();
        value += 1;
        return showcase.GetValueRef();
    }
}
