namespace Bakery.TypesAndValues.Nullable.ObliviousLegacy;

public static class LegacyAnonymous
{
    public static object CreateShape() => new { Name = "a", Count = 1 };

    public static Type GetShapeType() => CreateShape().GetType();
}
