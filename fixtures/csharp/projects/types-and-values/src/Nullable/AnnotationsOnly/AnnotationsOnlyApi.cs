namespace Bakery.TypesAndValues.Nullable.AnnotationsOnly;

// CS-CAN-024: annotations-only scope — <Nullable>annotations</Nullable> means
// annotations are emitted but warnings are not produced.

public sealed class AnnotationsOnlyInventory
{
    public string? Find(string? name) => name;

    public string Require(string? input) => input ?? "fallback";

    public string? OptionalLabel { get; set; }

    public string RequiredLabel { get; set; } = "ready";

    public void SetOptional(string? label) => OptionalLabel = label;
}
