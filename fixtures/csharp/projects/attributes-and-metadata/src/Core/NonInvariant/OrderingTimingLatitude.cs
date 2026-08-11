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

    public static string DescribeTokenOrderIndependence()
    {
        // Metadata-token order among these declared methods is never relied
        // upon; only set membership is asserted.
        var methodNames = typeof(NullableFlowShowcase)
            .GetMethods(BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly)
            .Select(m => m.Name)
            .ToHashSet(StringComparer.Ordinal);

        return $"token-order-independent-method-set-size={methodNames.Count} contains-fail={methodNames.Contains(nameof(NullableFlowShowcase.Fail))}";
    }

    public static string DescribeBeforeFieldInitLatitude()
    {
        // A type with only static field initializers and no explicit static
        // constructor is free to be emitted `beforefieldinit`, letting the
        // runtime initialize it any time before first use rather than
        // exactly at first access; only the flag's presence is observed,
        // never initialization timing.
        var isBeforeFieldInit = typeof(BeforeFieldInitCandidate).Attributes.HasFlag(TypeAttributes.BeforeFieldInit);
        return $"beforefieldinit-flag-observed={isBeforeFieldInit}";
    }

    public static string DescribeFinalizerLatitude()
    {
        // `Finalize` is an ECMA-335-defined override name, not a synthesized
        // one, so reflecting for it by name does not violate CS-CAN-125; the
        // finalizer's execution time and thread are never asserted.
        var finalizeMethod = typeof(FinalizerLatitudeShowcase)
            .GetMethod("Finalize", BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.DeclaredOnly);

        return $"finalizer-declared={finalizeMethod is not null}";
    }
}

internal static class BeforeFieldInitCandidate
{
    internal static readonly int Value = 42;
}

public sealed class FinalizerLatitudeShowcase
{
    ~FinalizerLatitudeShowcase()
    {
        // Finalizer timing and thread are entirely garbage-collector
        // determined; nothing here asserts when or on which thread this runs.
    }
}
