namespace GenericsAndDispatch.Compat;

// Version 2 of the published API, built with the SAME assembly identity as ProducerV1
// (GenericsAndDispatch.Compat.Producer), so it is a drop-in binary replacement. A more specific
// Render(string) overload was added; the object-typed overload is unchanged, so a caller that
// baked a call to Render(object) still resolves against this assembly.
public static class OverloadApi
{
    public static string Render(object value) => $"object:{value}";

    public static string Render(string value) => $"string:{value}";
}

// Version 2 changed the optional default from 1 to 99. A consumer already compiled against
// version 1 keeps the baked 1 when run against this replacement, because the default is baked into
// the caller. Only a consumer recompiled against this assembly bakes 99.
public static class DefaultApi
{
    public static string Greet(string name, int times = 99) => $"{name} x{times}";
}
