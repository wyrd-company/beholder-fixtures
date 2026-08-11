#nullable enable
namespace Bakery.TypesAndValues.Nullable.WarningsOnly;

// CS-CAN-024: warnings-only scope — <Nullable>warnings</Nullable> means warnings
// are enabled but annotations are treated as warnings rather than metadata.
// This file re-enables nullable to demonstrate a warnings-only project can still
// contain file-level nullable directives; the project-level setting would otherwise
// suppress annotation metadata emission.

public sealed class WarningsOnlyInventory
{
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
}
