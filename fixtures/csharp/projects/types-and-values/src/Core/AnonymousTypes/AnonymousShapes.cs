namespace Bakery.TypesAndValues.Core.AnonymousTypes;

// CS-CAN-026: anonymous types — repeated equal shapes, reordered/differently named
// shapes, projections, captures, equality, escape via inference or object,
// same-compilation reuse vs cross-assembly identity.

public static class AnonymousShapes
{
    public static object CreateSimple() => new { Name = "sourdough", Count = 6 };

    public static object CreateProjection()
    {
        string name = "rye";
        int count = 4;
        return new { name, count };
    }

    public static void SameShapeReused()
    {
        var first = new { Name = "a", Count = 1 };
        var second = new { Name = "b", Count = 2 };
        bool sameType = first.GetType() == second.GetType();
        _ = sameType;
    }

    public static void ReorderedShapeIsDifferent()
    {
        var first = new { Name = "a", Count = 1 };
        var second = new { Count = 1, Name = "a" };
        bool differentType = first.GetType() != second.GetType();
        _ = differentType;
    }

    public static void DifferentlyNamedShapeIsDifferent()
    {
        var first = new { Name = "a", Count = 1 };
        var second = new { Label = "a", Count = 1 };
        bool differentType = first.GetType() != second.GetType();
        _ = differentType;
    }

    public static void DifferentMemberTypeIsDifferent()
    {
        var first = new { Name = "a", Count = 1 };
        var second = new { Name = "a", Count = 1L };
        bool differentType = first.GetType() != second.GetType();
        _ = differentType;
    }

    public static void NullabilityVariation()
    {
        var withValue = new { Label = "a", Note = "present" };
        var withNull = new { Label = "a", Note = (string?)null };
        bool differentNullability = withValue.GetType() != withNull.GetType();
        _ = differentNullability;
    }

    public static void CaptureAndEquality()
    {
        string prefix = "batch";
        var first = new { Label = prefix + "-1", Count = 2 };
        var second = new { Label = prefix + "-1", Count = 2 };
        bool equal = first.Equals(second);
        bool notSameReference = !ReferenceEquals(first, second);
        _ = equal && notSameReference;
    }

    public static T EscapeViaInference<T>(T shape) => shape;

    public static object EscapeViaObject() => new { Name = "brioche", Count = 3 };

    public static void EscapeAndObserve(object boxed)
    {
        var type = boxed.GetType();
        var name = type.GetProperty("Name")?.GetValue(boxed) as string;
        _ = name;
    }

    public static void ProjectionWithAnonymousCapture()
    {
        var inventory = new[] { "sourdough", "rye", "brioche" };
        var projections = inventory.Select(name => new { name, Length = name.Length }).ToList();
        foreach (var item in projections)
        {
            _ = item.name;
            _ = item.Length;
        }
    }

    public static void ObserveGeneratedNamesWithoutDepending()
    {
        var shape = new { Name = "a", Count = 1 };
        Type type = shape.GetType();
        bool isCompilerGenerated =
            type.GetCustomAttributes(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute), false).Length > 0;
        bool hasAnonymousName = type.Name.Contains("AnonymousType");
        // Do not assert exact name/shape; only observe semantic association.
        _ = isCompilerGenerated && hasAnonymousName;
    }

    public static (object First, object Second) SameCompilationReusePair()
    {
        var first = new { Name = "a", Count = 1 };
        var second = new { Name = "b", Count = 2 };
        _ = first.GetType() == second.GetType();
        return (first, second);
    }

    // Cross-assembly identity: even equal shapes compiled in another assembly
    // produce a different anonymous type. The consumer project observes that
    // Bakery.TypesAndValues.Nullable.* anonymous types do not equal this assembly's.
}
