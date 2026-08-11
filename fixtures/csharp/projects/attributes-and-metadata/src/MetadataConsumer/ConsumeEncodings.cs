using Fixture.AttributesAndMetadata.Core.Metadata;

namespace Fixture.AttributesAndMetadata.MetadataConsumer;

/// <summary>
/// A second assembly consuming <c>Core</c>'s <c>dynamic</c>, tuple-name,
/// nullable, native-int, and ref encodings across an assembly boundary,
/// forcing each encoding to round-trip through emitted metadata.
/// </summary>
public static class ConsumeEncodings
{
    public static string ConsumeDynamic()
    {
        dynamic result = SourceOnlyEncodings.DescribeDynamic();
        string kind = (string)result.Kind;
        return $"dynamic-consumed={kind}";
    }

    public static string ConsumeTuple()
    {
        var (count, label) = SourceOnlyEncodings.DescribeTuple();
        return $"tuple-consumed count={count} label={label}";
    }

    public static string ConsumeNullable()
    {
        var maybeNull = SourceOnlyEncodings.DescribeNullable(null);
        return $"nullable-consumed is-null={maybeNull is null}";
    }

    public static string ConsumeNativeInt()
    {
        nint value = SourceOnlyEncodings.DescribeNativeInt();
        return $"native-int-consumed size={nint.Size} value={value}";
    }

    public static string ConsumeRef()
    {
        var value = 10;
        SourceOnlyEncodings.DescribeRef(ref value);
        ref readonly var viewed = ref SourceOnlyEncodings.DescribeRefReadonly(in value);
        return $"ref-consumed value={value} viewed={viewed}";
    }
}
