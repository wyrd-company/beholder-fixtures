using Fixture.AttributesAndMetadata.Core.Metadata;
using Fixture.AttributesAndMetadata.Core.Recognized;

namespace Fixture.AttributesAndMetadata.MetadataConsumer;

/// <summary>
/// A second assembly consuming <c>Core</c>'s <see langword="init"/>,
/// <see langword="volatile"/>, <see langword="readonly"/>/<see langword="scoped"/>,
/// <see langword="ref struct"/>, <c>unmanaged</c>-constraint, and extension
/// encodings, each forced to round-trip through emitted metadata.
/// </summary>
public static class AdditionalConsumeEncodings
{
    public static string ConsumeInit()
    {
        var record = new InitOnlyRecord { Value = 9 };
        return $"init-consumed value={record.Value}";
    }

    public static string ConsumeVolatile()
    {
        VolatileCounterHost.Counter = 3;
        var observed = VolatileCounterHost.Counter;
        return $"volatile-consumed value={observed}";
    }

    public static string ConsumeReadOnlyAndScoped()
    {
        var box = new ReadOnlyValueBox(11);
        var described = ScopedParameterShowcase.DescribeScoped(box);
        return $"readonly-scoped-consumed value={described}";
    }

    public static string ConsumeRefStruct()
    {
        var showcase = new RefSafetyShowcase(4);
        ref var value = ref showcase.GetValueRef();
        value += 1;
        return $"ref-struct-consumed value={showcase.GetValueRef()}";
    }

    public static string ConsumeUnmanagedConstraint()
    {
        var size = UnmanagedConstraintShowcase.DescribeUnmanagedSize<int>();
        return $"unmanaged-constraint-consumed size={size}";
    }

    public static string ConsumeExtension()
    {
        var box = new ReadOnlyValueBox(21);
        var described = box.DescribeExtension();
        return $"extension-consumed={described}";
    }
}
