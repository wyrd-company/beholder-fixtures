namespace Acme.Conflict
{
    public sealed class CollidingType
    {
        public string Source => "Conflict.External reference";
        public string Describe() => "CollidingType from external reference";
    }
}

namespace Acme.Polyfill
{
    public sealed class PolyfillOverlap
    {
        public string Origin => "Conflict.External polyfill";
    }
}
