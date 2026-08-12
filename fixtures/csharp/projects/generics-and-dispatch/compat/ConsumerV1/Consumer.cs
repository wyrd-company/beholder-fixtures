using GenericsAndDispatch.Compat;

namespace GenericsAndDispatch.Compat.Consumers;

// Compiled against version 1 metadata across the producer/consumer assembly boundary.
public static class ConsumerV1
{
    // Render("text") binds Render(object): it is the only candidate in version 1. The baked
    // metadata token stays Render(object) even after version 2 adds the more specific overload,
    // so the old binding is preserved until this assembly is recompiled.
    public static string BoundRender() => OverloadApi.Render("text");

    // The omitted optional argument bakes times=1 from version 1 metadata into this call site;
    // it is independent of the producer's later default.
    public static string BakedGreet() => DefaultApi.Greet("hello");
}
