namespace GenericsAndDispatch.Compat;

// Version 2 of the same published API surface. A more specific Render(string) overload was
// added; the object-typed overload is unchanged, so it is source- and binary-compatible.
public static class OverloadApi
{
    public static string Render(object value) => $"object:{value}";

    public static string Render(string value) => $"string:{value}";
}

// Version 2 changed the optional default from 1 to 99. A consumer already compiled against
// version 1 keeps the baked 1 until it is recompiled against this metadata.
public static class DefaultApi
{
    public static string Greet(string name, int times = 99) => $"{name} x{times}";
}
