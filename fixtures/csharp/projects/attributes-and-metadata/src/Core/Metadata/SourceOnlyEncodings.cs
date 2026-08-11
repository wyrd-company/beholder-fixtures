using System.Dynamic;

namespace Fixture.AttributesAndMetadata.Core.Metadata;

/// <summary>
/// Public surface encoding source-only distinctions in emitted metadata —
/// <c>dynamic</c>, tuple element names, nullable reference annotations,
/// native-sized integers, and ref returns/parameters — for a second
/// assembly to consume.
/// </summary>
public static class SourceOnlyEncodings
{
    /// <summary>
    /// Returns an <see cref="ExpandoObject"/> rather than an anonymous type:
    /// anonymous types are compiler-emitted as <c>internal</c>, so a second
    /// assembly's dynamic binder cannot see their members at all.
    /// </summary>
    public static dynamic DescribeDynamic()
    {
        dynamic expando = new ExpandoObject();
        expando.Kind = "dynamic-result";
        return expando;
    }

    public static (int Count, string Label) DescribeTuple() => (42, "answer");

    public static string? DescribeNullable(string? input) => input;

    public static nint DescribeNativeInt() => (nint)128;

    public static nuint DescribeNativeUInt() => (nuint)256;

    public static void DescribeRef(ref int value) => value += 1;

    public static ref readonly int DescribeRefReadonly(in int value) => ref value;
}
