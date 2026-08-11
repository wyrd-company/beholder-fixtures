using System.Reflection;
using Fixture.AttributesAndMetadata.Core.Recognized;

namespace Fixture.AttributesAndMetadata.Core.NonInvariant;

public static partial class PartialInitializerLatitude
{
    public static readonly int First = 1;
}

public static partial class PartialInitializerLatitude
{
    public static readonly int Second = 2;
}

/// <summary>
/// CS-CAN-126: avoids invariants over reflection member order and
/// partial-declaration field-initializer order. Reflection results are
/// consumed as an order-independent set; the two partial-type field
/// initializers are read only for their combined final values, never for
/// which file's initializer the runtime ran first — the CLI does not
/// guarantee an order across a type's partial declarations.
/// </summary>
public static class OrderingTimingLatitude
{
    public static string DescribeReflectionOrderIndependence()
    {
        var members = typeof(NullableFlowShowcase)
            .GetMembers(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Select(m => m.Name)
            .ToHashSet(StringComparer.Ordinal);

        return $"member-set-size={members.Count} contains-display={members.Contains(nameof(NullableFlowShowcase.Display))}";
    }

    public static string DescribePartialInitializerCombinedState()
    {
        var values = new[] { PartialInitializerLatitude.First, PartialInitializerLatitude.Second }.ToHashSet();
        return $"partial-initializer-distinct-values-observed={values.Count}";
    }

    public static string DescribeModuleInitializerOrderLatitude()
        => "module-initializer-order-among-several-not-asserted; see ModuleInitializationObservation";
}
