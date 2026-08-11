namespace SourceBinding.Core.Lexical;

public static class LexicalIdentity
{
    // Escaped and keyword-like identifiers.
    public static int EscapedIdentifiers()
    {
        int @class = 11;
        int @string = 22;
        int @int = 33;
        int @for = 44;
        int @namespace = 55;
        return @class + @string + @int + @for + @namespace;
    }

    // Unicode and escaped spelling equivalence.
    public static string UnicodeEquivalence()
    {
        int \u0061 = 1; // \u0061 spells 'a'.
        int aRef = a; // 'a' spelling equivalent to \u0061, same declaration accessed via different spelling.
        int caf\u00e9 = 100; // caf\u00e9 spells 'café' via escape.
        int caféRef = caf\u00e9; // equivalent spelling access.
        // Visually confusable distinct code points: Latin 'a' U+0061 versus Cyrillic 'а' U+0430.
        int latinA = aRef + \u0061;
        int cyrillicA = 7;
        int \u0430 = 7; // Cyrillic small letter a, distinct from Latin 'a'.
        _ = cyrillicA;
        _ = latinA;
        _ = \u0430;
        return $"{caf\u00e9}-{caféRef}-{aRef}-{latinA}";
    }

    // Contextual identifiers: var, record, etc. can be used as identifiers in suitable contexts.
    public static int ContextualIdentifiers()
    {
        int var = 5;
        int record = 6;
        int required = 7;
        int file = 8;
        int scoped = 9;
        return var + record + required + file + scoped;
    }

    // Verbatim identifiers and strings.
    public static string VerbatimForms()
    {
        string verbatim = @"verbatim\nkeeps\backslashes";
        string verbatimWithQuote = @"verbatim ""quoted"" text";
        string regular = "regular\ninterpreted";
        return verbatim + verbatimWithQuote + regular;
    }

    // Literal forms.
    public static string LiteralForms()
    {
        // Regular, verbatim, and interpolated.
        string regular = "hello";
        string verbatimPath = @"C:\temp\file.txt";
        string interpolated = $"value {regular} at {verbatimPath}";
        string verbatimInterpolated = $@"verbatim {regular} still";

        // Numeric with separators and radix.
        int decimalWithSeparator = 1_000_000;
        int hexWithSeparator = 0xFF_FF;
        int binaryWithSeparator = 0b1010_0101;
        long longWithSuffix = 123_456L;
        double doubleWithSeparator = 1_234.567_8;
        float floatWithSuffix = 1.5f;
        decimal decimalWithSuffix = 123.45m;

        // Checked literal edge.
        const int maxInt = int.MaxValue;
        const int minInt = int.MinValue;
        int edge = checked(maxInt);

        _ = decimalWithSeparator;
        _ = hexWithSeparator;
        _ = binaryWithSeparator;
        _ = longWithSuffix;
        _ = doubleWithSeparator;
        _ = floatWithSuffix;
        _ = decimalWithSuffix;
        _ = edge;
        _ = minInt;

        return regular + interpolated + verbatimInterpolated;
    }

    // Raw string delimiters and interpolation-brace variants.
    public static string RawStrings()
    {
        string rawSingle = """single line raw string""";
        string rawWithQuotes = """raw with "quotes" inside""";
        string rawMulti =
            """
            multi
            line
            raw
            """;

        string name = "world";
        string interpolatedRaw = $"""Hello {name} from raw {1 + 1}""";

        // Double-dollar raw with doubled braces.
        string interpolatedRawDouble = $$"""Hello {{name}} still {{"literal"}}""";
        string rawDelimiterFour = """  delimiter variant "content" """;

        _ = rawDelimiterFour;
        return rawSingle + rawWithQuotes + rawMulti + interpolatedRaw + interpolatedRawDouble;
    }

    // UTF-8 literals (C# 11).
    public static ReadOnlySpan<byte> Utf8Literals()
    {
        ReadOnlySpan<byte> utf8 = "hello"u8;
        ReadOnlySpan<byte> utf8Raw = """raw utf8"""u8;
        ReadOnlySpan<byte> utf8Additional = "additional"u8;
        _ = utf8Raw;
        _ = utf8Additional;
        return utf8;
    }
}
