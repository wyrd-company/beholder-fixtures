using GenericsAndDispatch.Compat;

namespace GenericsAndDispatch.Compat.Consumers;

// Compiled against version 1 of GenericsAndDispatch.Compat.Producer. Because version 2 shares the
// same assembly identity, this assembly can run unchanged against the version 2 replacement.
public static class ConsumerV1
{
    // Render("text") bakes a metadata token to Render(object): the only candidate in version 1.
    // Run against the version 2 replacement the token still resolves to Render(object), so the old
    // binding is preserved even though version 2 adds the more specific Render(string) overload.
    public static string BoundRender() => OverloadApi.Render("text");

    // The omitted optional argument bakes times=1 from version 1 into this call site. Run against
    // the version 2 replacement (whose declared default is 99) this caller still passes 1, because
    // the default lives in the caller's IL, not the producer.
    public static string BakedGreet() => DefaultApi.Greet("hello");
}
