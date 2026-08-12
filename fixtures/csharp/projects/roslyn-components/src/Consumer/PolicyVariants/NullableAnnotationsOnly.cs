#nullable disable
#nullable enable annotations

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: nullable annotations-only. Starts from disabled (both off)
// then enables annotations only, leaving warnings disabled. Distinct from
// warnings-only and fully enabled/disabled.
public sealed class NullableAnnotationsOnly
{
    public string? MaybeName { get; set; }

    public void Accept(string value)
    {
    }

    public void Call()
    {
        // With annotations-only, this mismatch is visible in metadata but
        // no CS8600/CS8604 warning is emitted in this file because warnings
        // remain disabled.
        string? maybe = MaybeName;
        if (maybe is not null)
        {
            Accept(maybe);
        }
    }
}
