namespace Bakery.TypesAndValues.Nullable.AnnotatedApi;

public static class AnnotatedAnonymous
{
    public static object CreateShape() => new { Name = "a", Count = 1 };

    public static Type GetShapeType() => CreateShape().GetType();
}
