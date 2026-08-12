namespace Bakery.TypesAndValues.Nullable.WarningsOnly;

// CS-CAN-024: warnings-only scope — <Nullable>warnings</Nullable> means warnings
// are enabled but annotations are not emitted as metadata. This file inherits
// the project-level warnings-only context; annotated sections use local #nullable
// enable, and intentional warnings use narrow pragma suppression.

public sealed class WarningsOnlyInventory
{
    // Valid source section compiled in the project-level warnings-only context
    // (no nullable annotations, warnings still enabled).
    public string FindNoAnnotation(string name) => name;

    public void ConsumeNoAnnotation(string maybe)
    {
        if (maybe is not null)
        {
            _ = maybe.Length;
        }
    }

#nullable enable
    public string? Find(string? name) => name;

    public string Require(string? input)
    {
        if (input is null)
        {
            return "fallback";
        }

        return input;
    }

    public void Consume(string? maybe)
    {
        if (maybe is not null)
        {
            _ = maybe.Length;
        }
    }

    public void DereferenceWithWarning(string? maybe)
    {
#pragma warning disable CS8602
        _ = maybe.Length;
#pragma warning restore CS8602
    }
#nullable restore
}
