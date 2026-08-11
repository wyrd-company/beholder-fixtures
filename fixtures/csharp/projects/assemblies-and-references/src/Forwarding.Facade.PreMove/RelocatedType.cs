namespace Acme.Forwarding;

// Pre-move shape: RelocatedType is defined directly in the "Forwarding.Facade" identity,
// matching what that assembly contained before the move. Forwarding.Consumer.Legacy
// references this project to represent a binary built against that pre-move shape.
public sealed class RelocatedType
{
    public string Origin => "Forwarding.Facade (pre-move location)";
    public string Describe() => "RelocatedType originally defined in Forwarding.Facade";
    public int Version => 1;

    public sealed class NestedPayload
    {
        public string Label => "nested payload in pre-move type";
    }
}
