namespace GenericsAndDispatch.Compat;

// Version 1 of a published API, built as assembly identity GenericsAndDispatch.Compat.Producer.
// Version 2 (ProducerV2) shares that identity, so it can replace this assembly at run time.
// The overload set has only the object-typed Render.
public static class OverloadApi
{
    public static string Render(object value) => $"object:{value}";
}

// Version 1 declares the optional default as 1. Callers bake that value into their own IL at the
// call site, so a caller keeps 1 even when the version 2 replacement declares a different default.
public static class DefaultApi
{
    public static string Greet(string name, int times = 1) => $"{name} x{times}";
}
