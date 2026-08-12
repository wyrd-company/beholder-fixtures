namespace GenericsAndDispatch.Compat;

// Version 1 of a published API surface, consumed across an assembly metadata boundary.
// The overload set has only the object-typed Render.
public static class OverloadApi
{
    public static string Render(object value) => $"object:{value}";
}

// Version 1 bakes an optional default of 1 into each caller's IL at the call site.
public static class DefaultApi
{
    public static string Greet(string name, int times = 1) => $"{name} x{times}";
}
