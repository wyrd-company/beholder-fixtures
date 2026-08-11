#define FEATURE_A
#undef FEATURE_B

using System.Diagnostics;

namespace SourceBinding.Core.Preprocessor;

#if FEATURE_A && !FEATURE_B
public sealed class FeatureAOnly { }
#elif FEATURE_B
public sealed class FeatureBOnly { }
#else
public sealed class FeatureFallback { }
#endif

#if FEATURE_A
public sealed class ActiveDeclaration
{
    public static string Describe() => "feature-a active";
}
#else
public sealed class ActiveDeclaration
{
    public static string Describe() => "fallback";
}
#endif

// Duplicate declaration conditional exclusion: only one symbol set compiles.
#if FEATURE_A
public sealed class ConditionalTypeOne
{
    public int Value => 1;
}
#endif

#if !FEATURE_A
public sealed class ConditionalTypeOne
{
    public int Value => 99;
}
#endif

// Project-supplied symbol FEATURE_A originates from Core.csproj DefineConstants.
// FEATURE_B is undefined above via #undef, demonstrating symbol absence.
#if FEATURE_B
public sealed class ShouldNotBeIncluded { }
#endif

#if !FEATURE_B
public sealed class AfterUndefine
{
    public static bool IsExcluded => true;
}
#endif

// Inactive region may contain malformed-looking text that is not parsed.
#if false
This is inactive text that looks malformed: @@@ ### """ not parsed as C#
#endif

#pragma warning disable CS0219
public static class WarningSuppression
{
    public static void Suppressed()
    {
        int unused = 123; // suppressed
        _ = unused;
    }
}
#pragma warning restore CS0219

public static class WarningHidden
{
#pragma warning disable CS0219
    public static void Hidden()
    {
        int hiddenUnused = 456;
        _ = hiddenUnused;
    }
#pragma warning restore CS0219

    public static void Visible()
    {
        int used = 1;
        _ = used;
    }
}

#nullable enable
public sealed class NullableEnabled
{
    public string? MaybeNull { get; set; }
}
#nullable disable
public sealed class NullableDisabled
{
    public string MaybeNull { get; set; } = string.Empty;
}
#nullable restore

public static class DiagnosticMapping
{
#pragma warning disable CS0618
    public static void CallObsolete()
    {
        _ = LegacyObsolete.OldMethod();
    }
#pragma warning restore CS0618
}

[Obsolete("use NewMethod")]
public static class LegacyObsolete
{
    public static int OldMethod() => 42;

    public static int NewMethod() => 43;
}
