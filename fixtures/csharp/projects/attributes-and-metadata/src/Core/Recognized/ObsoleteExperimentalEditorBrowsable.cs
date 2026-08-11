using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using Fixture.AttributesAndMetadata.Core.Attributes;

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
/// An accessor-level reference: only the <see langword="set"/> accessor is
/// obsolete, so reading <see cref="Value"/> is an ordinary, undiagnosed
/// reference while writing it is not.
/// </summary>
public sealed class ObsoleteAccessorShowcase
{
    private int _value;

    public int Value
    {
        get => _value;
        [Obsolete(
            "Superseded setter; kept only for this fixture's accessor reference demonstration.",
            DiagnosticId = "SHOWCASE_OBS_ACCESSOR",
            UrlFormat = "https://example.invalid/diagnostics/{0}")]
        set => _value = value;
    }
}

/// <summary>
/// An interface-implementation-level reference: the implementing method is
/// obsolete, but the interface member it implements is not, so a call
/// through the interface reference is undiagnosed while a direct call on the
/// concrete type is.
/// </summary>
public sealed class ObsoleteInterfaceImplementationShowcase : IShowcaseContract
{
    [Obsolete(
        "Superseded implementation; kept only for this fixture's interface-implementation reference demonstration.",
        DiagnosticId = "SHOWCASE_OBS_IMPL",
        UrlFormat = "https://example.invalid/diagnostics/{0}")]
    public void Act()
    {
    }
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

    /// <summary>
    /// Reading <see cref="ObsoleteAccessorShowcase.Value"/> is an ordinary,
    /// undiagnosed reference; only the <see langword="set"/> accessor is
    /// obsolete.
    /// </summary>
    public static int ReferenceAccessorGetter()
    {
        var showcase = new ObsoleteAccessorShowcase();
        return showcase.Value;
    }

    public static int ReferenceAccessorSetter()
    {
        var showcase = new ObsoleteAccessorShowcase();
#pragma warning disable SHOWCASE_OBS_ACCESSOR
        showcase.Value = 5;
#pragma warning restore SHOWCASE_OBS_ACCESSOR
        return showcase.Value;
    }

    /// <summary>
    /// A call through the <see cref="Attributes.IShowcaseContract"/>
    /// reference is undiagnosed: the interface member itself is not
    /// obsolete, only this concrete implementation.
    /// </summary>
    public static void ReferenceInterfaceImplementationViaInterface()
    {
        IShowcaseContract contract = new ObsoleteInterfaceImplementationShowcase();
        contract.Act();
    }

    public static void ReferenceInterfaceImplementationDirectly()
    {
        var concrete = new ObsoleteInterfaceImplementationShowcase();
#pragma warning disable SHOWCASE_OBS_IMPL
        concrete.Act();
#pragma warning restore SHOWCASE_OBS_IMPL
    }
}
