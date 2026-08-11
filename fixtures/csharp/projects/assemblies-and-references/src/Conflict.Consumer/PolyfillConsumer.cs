namespace Acme.Polyfill;

public sealed class PolyfillOverlap
{
    public string Origin => "Conflict.Consumer polyfill (local wins)";
    public string Describe() => "Local polyfill wins over reference polyfill with same qualified name";
}

public sealed class PolyfillConsumer
{
    public string UseLocalPolyfill() => new PolyfillOverlap().Describe();
}
