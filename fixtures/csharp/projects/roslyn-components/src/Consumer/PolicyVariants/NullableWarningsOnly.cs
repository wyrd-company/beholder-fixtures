#nullable enable warnings

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: nullable warnings-only. Warnings are emitted but annotations
// have no effect on the type system; contrasts with annotations-only.
public sealed class NullableWarningsOnly
{
    public string MaybeName { get; set; } = string.Empty;

    public void Consume(string? maybe)
    {
        // With warnings-only, this produces a warning because the parameter
        // is nullable but no annotation controls its flow.
        if (maybe is not null)
        {
            MaybeName = maybe;
        }
    }
}
