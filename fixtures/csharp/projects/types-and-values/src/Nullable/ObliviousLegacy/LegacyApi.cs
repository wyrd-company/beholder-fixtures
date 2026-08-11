namespace Bakery.TypesAndValues.Nullable.ObliviousLegacy;

// CS-CAN-024: oblivious scope — no <Nullable> property, pre-C# 8 metadata without annotations.
// This file is compiled without nullable annotations; reference types are oblivious.

public class LegacyInventory
{
    public string Find(string name)
    {
        return name;
    }

    public string GetLabel(string input)
    {
        return input.ToUpperInvariant();
    }

    public void SetLabel(string label)
    {
        _ = label;
    }

    public string Label
    {
        get => _label;
        set => _label = value;
    }

    private string _label = string.Empty;
}

public class LegacyHolder
{
    public string Name { get; set; }

    public LegacyHolder(string name) => Name = name;
}
