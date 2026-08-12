using System;

namespace SourceBinding.Core.Partial;

public partial class PartialEntity
{
    // Legacy partial method (no accessibility, implicitly private). No implementation -> call and argument evaluation erased.
    partial void LegacyHook(int value);

    // Legacy partial method with implementation.
    partial void LegacyImplementedHook(int value);

    // Extended partial method (C# 9) with accessibility and implementation required.
    public partial void ExtendedHook(int value);

    // C# 13 partial property and indexer: declaring declaration.
    public partial string CatalogLabel { get; set; }

    public partial int this[int index] { get; set; }

    private string _catalogLabel = string.Empty;
    private int[] _store = new int[8];
    private static int _sideEffectCounter;

    private static int ProduceSideEffect()
    {
        _sideEffectCounter++;
        return _sideEffectCounter;
    }

    public void Invoke()
    {
        // This call and its argument side effect are erased when LegacyHook lacks implementation.
        LegacyHook(ProduceSideEffect());
        LegacyImplementedHook(ProduceSideEffect());
        ExtendedHook(42);
        _ = CatalogLabel;
        _ = this[2];
    }
}

public partial class PartialEntity
{
    // Implementations for the partial members.
    partial void LegacyImplementedHook(int value)
    {
        _catalogLabel = $"legacy:{value}";
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
