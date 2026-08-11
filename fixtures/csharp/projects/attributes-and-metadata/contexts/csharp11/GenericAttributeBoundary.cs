namespace Fixture.AttributesAndMetadata.Contexts.CSharp11;

/// <summary>Generic attribute classes became valid at their C# 11 version floor; built here under <c>LangVersion 11.0</c>.</summary>
[AttributeUsage(AttributeTargets.Class)]
public sealed class BoundaryMarkerAttribute<T> : Attribute
{
    public string? Note { get; set; }
}

[BoundaryMarker<string>(Note = "generic-attribute-at-langversion-11")]
public sealed class GenericAttributeBoundaryTarget
{
}

public static class GenericAttributeBoundaryObservation
{
    public static string Describe()
    {
        var attribute = typeof(GenericAttributeBoundaryTarget)
            .GetCustomAttributes(false)
            .OfType<Attribute>()
            .SingleOrDefault(a => a.GetType().IsGenericType);

        return attribute is null ? "no-generic-attribute-found" : "generic-attribute-present";
    }
}
