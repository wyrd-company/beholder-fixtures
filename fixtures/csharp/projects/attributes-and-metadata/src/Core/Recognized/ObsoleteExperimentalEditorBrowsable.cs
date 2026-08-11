using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Linq;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// Declares a warning-level obsolete member, an error-level obsolete member,
/// an experimental member, an obsolete type, and an editor-browsable-hidden
/// member, each with a custom diagnostic identifier and URL.
/// </summary>
public static class ObsoleteExperimentalShowcase
{
    [Obsolete(
        "Superseded; kept only for this fixture's warning-level reference demonstration.",
        DiagnosticId = "SHOWCASE_OBS_WARN",
        UrlFormat = "https://example.invalid/diagnostics/{0}")]
    public static void WarnObsolete()
    {
    }

    [Obsolete(
        "Removed permanently; kept only for this fixture's error-level reference demonstration.",
        error: true,
        DiagnosticId = "SHOWCASE_OBS_ERROR",
        UrlFormat = "https://example.invalid/diagnostics/{0}")]
    public static void ErrorObsolete()
    {
    }

    [Experimental("SHOWCASE_EXPERIMENTAL", UrlFormat = "https://example.invalid/diagnostics/{0}")]
    public static void ExperimentalFeature()
    {
    }

    [EditorBrowsable(EditorBrowsableState.Never)]
    public static int HiddenFromIntelliSense() => 1;
}

[Obsolete(
    "Superseded type; kept only for this fixture's warning-level reference demonstration.",
    DiagnosticId = "SHOWCASE_OBS_TYPE",
    UrlFormat = "https://example.invalid/diagnostics/{0}")]
public sealed class ObsoleteTypeShowcase
{
}

/// <summary>
/// Exercises every declared reference: a pragma-suppressed warning-level
/// obsolete call, a pragma-suppressed experimental call, an ordinary
/// (unsuppressed) call proving <see cref="EditorBrowsableAttribute"/> has no
/// semantic effect on compilation, and reflected-only references to the
/// error-level obsolete member and the obsolete type — a call to an
/// error-level obsolete member is a compile error unconditionally, even
/// under pragma suppression, so its reference here is metadata-only.
/// </summary>
public static class ObsoleteReferenceDemo
{
    public static void ReferenceWarningLevelObsolete()
    {
#pragma warning disable SHOWCASE_OBS_WARN
        ObsoleteExperimentalShowcase.WarnObsolete();
#pragma warning restore SHOWCASE_OBS_WARN
    }

    public static void ReferenceExperimental()
    {
#pragma warning disable SHOWCASE_EXPERIMENTAL
        ObsoleteExperimentalShowcase.ExperimentalFeature();
#pragma warning restore SHOWCASE_EXPERIMENTAL
    }

    /// <summary>
    /// Calls the editor-browsable-hidden member with no suppression at all,
    /// which is itself the proof that <see cref="EditorBrowsableAttribute"/>
    /// only affects tooling display, never compilation.
    /// </summary>
    public static int ReferenceEditorBrowsableHidden()
        => ObsoleteExperimentalShowcase.HiddenFromIntelliSense();

    [return: NotNull]
    public static string DescribeErrorLevelObsoleteMetadata()
    {
        var method = typeof(ObsoleteExperimentalShowcase).GetMethod(nameof(ObsoleteExperimentalShowcase.ErrorObsolete))!;
        var attribute = method.GetCustomAttributes(typeof(ObsoleteAttribute), false)
            .Cast<ObsoleteAttribute>()
            .Single();
        return $"error-obsolete-diagnostic-id={attribute.DiagnosticId} is-error={attribute.IsError}";
    }

    [return: NotNull]
    public static string DescribeObsoleteTypeMetadata()
    {
#pragma warning disable SHOWCASE_OBS_TYPE
        var attribute = typeof(ObsoleteTypeShowcase).GetCustomAttributes(typeof(ObsoleteAttribute), false)
            .Cast<ObsoleteAttribute>()
            .Single();
#pragma warning restore SHOWCASE_OBS_TYPE
        return $"obsolete-type-diagnostic-id={attribute.DiagnosticId} is-error={attribute.IsError}";
    }
}
