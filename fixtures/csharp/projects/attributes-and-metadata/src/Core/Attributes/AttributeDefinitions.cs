using System.Diagnostics;

namespace Fixture.AttributesAndMetadata.Core.Attributes;

/// <summary>
/// A general-purpose custom attribute usable on every declaration target,
/// accepting a positional argument plus named array- and <see langword="typeof"/>-typed
/// arguments, and allowing duplicate application.
/// </summary>
[AttributeUsage(AttributeTargets.All, AllowMultiple = true, Inherited = false)]
public sealed class ShowcaseAttribute : Attribute
{
    public ShowcaseAttribute(string label)
    {
        Label = label;
    }

    public string Label { get; }

    public string[] Tags { get; set; } = Array.Empty<string>();

    public Type? Correlate { get; set; }
}

/// <summary>A generic custom attribute (valid from C# 11 onward).</summary>
/// <typeparam name="T">The type this application associates with its target.</typeparam>
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method | AttributeTargets.Struct)]
public sealed class AssociatedTypeAttribute<T> : Attribute
{
    public string? Note { get; set; }
}

/// <summary>Reflection-visible when applied to a class, and inherited by derived classes.</summary>
[AttributeUsage(AttributeTargets.Class, Inherited = true)]
public sealed class InheritedMarkerAttribute : Attribute
{
}

/// <summary>Reflection-visible only on the exact class it decorates, never on a derived class.</summary>
[AttributeUsage(AttributeTargets.Class, Inherited = false)]
public sealed class NonInheritedMarkerAttribute : Attribute
{
}

/// <summary>
/// Names the compilation symbol that gates every conditional-elision
/// demonstration in this project: applications of this custom attribute
/// class, and calls guarded by <see cref="System.Diagnostics.ConditionalAttribute"/>
/// with the same symbol, are both omitted from emitted metadata wherever the
/// symbol is undefined at the syntactic call or application site.
/// </summary>
internal static class ConditionalSymbols
{
    public const string ShowcaseEnabled = "ATTR_META_SHOWCASE_ENABLED";
}

/// <summary>
/// A conditional attribute class: applications of this attribute are elided
/// from emitted metadata wherever <see cref="ConditionalSymbols.ShowcaseEnabled"/>
/// is not defined at the application's syntactic location.
/// </summary>
[Conditional(ConditionalSymbols.ShowcaseEnabled)]
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public sealed class ShowcaseDiagnosticAttribute : Attribute
{
}
