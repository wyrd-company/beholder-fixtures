#nullable disable
#nullable enable warnings

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: nullable warnings-only. Starts from disabled (both off)
// then enables warnings only, leaving annotations disabled. Contrasts with
// annotations-only.
public sealed class NullableWarningsOnly
{
    public string MaybeName { get; set; } = string.Empty;

    public void Consume(string? maybe)
    {
        // With warnings-only, this produces a warning because the parameter
        // is nullable but annotations remain disabled, so no annotation
        // controls its flow.
        if (maybe is not null)
        {
            MaybeName = maybe;
        }
    }
}
