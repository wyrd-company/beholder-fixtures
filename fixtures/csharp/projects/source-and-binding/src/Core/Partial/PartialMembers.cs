using System;

namespace SourceBinding.Core.Partial;

public partial class PartialEntity
{
    // Legacy partial method (no accessibility, implicitly private). No implementation -> calls erased.
    partial void LegacyHook();

    // Legacy partial method with implementation.
    partial void LegacyImplementedHook();

    // Extended partial method (C# 9) with accessibility and implementation required.
    public partial void ExtendedHook(int value);

    // C# 13 partial property and indexer: declaring declaration.
    public partial string CatalogLabel { get; set; }

    public partial int this[int index] { get; set; }

    private string _catalogLabel = string.Empty;
    private int[] _store = new int[8];

    public void Invoke()
    {
        // This call is erased when LegacyHook lacks implementation (no side effects emitted).
        LegacyHook();
        LegacyImplementedHook();
        ExtendedHook(42);
        _ = CatalogLabel;
        _ = this[2];
    }
}

public partial class PartialEntity
{
    // Implementations for the partial members.
    partial void LegacyImplementedHook()
    {
        _catalogLabel = "legacy";
    }

    public partial void ExtendedHook(int value)
    {
        _catalogLabel = value.ToString();
    }

    public partial string CatalogLabel
    {
        get => _catalogLabel;
        set => _catalogLabel = value;
    }

    public partial int this[int index]
    {
        get => _store[index];
        set => _store[index] = value;
    }
}
