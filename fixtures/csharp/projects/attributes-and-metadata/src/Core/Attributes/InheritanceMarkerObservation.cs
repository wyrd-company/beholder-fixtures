namespace Fixture.AttributesAndMetadata.Core.Attributes;

/// <summary>
/// Reflects over <see cref="InheritanceMarkerDerived"/> to contrast
/// inherited-versus-non-inherited custom-attribute lookup: both
/// <see cref="InheritedMarkerAttribute"/> (<c>Inherited = true</c>) and
/// <see cref="NonInheritedMarkerAttribute"/> (<c>Inherited = false</c>) are
/// declared only on <see cref="InheritanceMarkerBase"/>, so only the former
/// is found through inherited lookup on the derived type.
/// </summary>
public static class InheritanceMarkerObservation
{
    public static string DescribeInheritedLookup()
    {
        var derivedType = typeof(InheritanceMarkerDerived);

        var inheritedMarkerFound = derivedType.IsDefined(typeof(InheritedMarkerAttribute), inherit: true);
        var nonInheritedMarkerFoundViaInherit = derivedType.IsDefined(typeof(NonInheritedMarkerAttribute), inherit: true);
        var nonInheritedMarkerFoundDirectly = derivedType.IsDefined(typeof(NonInheritedMarkerAttribute), inherit: false);

        return $"inherited-marker-found-on-derived={inheritedMarkerFound} " +
               $"non-inherited-marker-found-via-inherit-true={nonInheritedMarkerFoundViaInherit} " +
               $"non-inherited-marker-found-via-inherit-false={nonInheritedMarkerFoundDirectly}";
    }
}
