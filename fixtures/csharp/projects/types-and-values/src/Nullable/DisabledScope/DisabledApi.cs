#nullable disable
namespace Bakery.TypesAndValues.Nullable.DisabledScope;

// CS-CAN-024: disabled scope — both file-level #nullable disable and
// project-level <Nullable>disable</Nullable> mean all nullable analysis is off.
// Reference types are treated as nullable-oblivious within this scope.

public sealed class DisabledInventory
{
    public string Find(string name)
    {
        return name;
    }

    public string GetLabel(string input)
    {
        return input;
    }

    public void Consume(string maybe)
    {
        // No warnings for dereference even if null could be passed.
        int len = maybe.Length;
        _ = len;
    }

    public string MaybeReturnsNull(string name)
    {
        if (name.Length == 0)
        {
            return null!;
        }

        return name;
    }
}
