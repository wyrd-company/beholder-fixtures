using System;

namespace SourceBinding.CSharp11;

public static class RawLiteralDemo
{
    public static string RawSingle() => """raw single""";

    public static string RawMulti() =>
        """
        multi
        line
        """;

    public static string InterpolatedRaw(string name) => $"""Hello {name}""";

    public static ReadOnlySpan<byte> Utf8() => "utf8 literal"u8;

    public static ReadOnlySpan<byte> RawUtf8() => """raw utf8"""u8;
}
