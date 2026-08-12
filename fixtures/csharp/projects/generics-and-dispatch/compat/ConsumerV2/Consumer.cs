using GenericsAndDispatch.Compat;

namespace GenericsAndDispatch.Compat.Consumers;

// Compiled against version 2 metadata across the producer/consumer assembly boundary.
public static class ConsumerV2
{
    // The identical call text now binds Render(string): version 2 exposes the added, more
    // specific overload, so recompilation rebinds this call site from Render(object).
    public static string BoundRender() => OverloadApi.Render("text");

    // The omitted optional argument bakes times=99 from version 2 metadata into this call site.
    public static string BakedGreet() => DefaultApi.Greet("hello");
}
