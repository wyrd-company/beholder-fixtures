using GenericsAndDispatch.Compat;

namespace GenericsAndDispatch.Compat.Consumers;

// Compiled against version 2 of GenericsAndDispatch.Compat.Producer: the same source recompiled
// against the replacement, to contrast with ConsumerV1's retained version 1 bindings.
public static class ConsumerV2
{
    // The identical call text now bakes Render(string): version 2 exposes the added, more specific
    // overload, so recompiling against it rebinds this call site from Render(object).
    public static string BoundRender() => OverloadApi.Render("text");

    // The omitted optional argument bakes times=99 from version 2 into this call site.
    public static string BakedGreet() => DefaultApi.Greet("hello");
}
