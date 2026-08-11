namespace Acme.Forwarding;

public sealed class RelocatedType
{
    public string Origin => "Forwarding.Definition (current location)";
    public string Describe() => "RelocatedType now lives in Forwarding.Definition";
    public int Version => 2;

    public sealed class NestedPayload
    {
        public string Label => "nested payload in relocated type";
    }
}
