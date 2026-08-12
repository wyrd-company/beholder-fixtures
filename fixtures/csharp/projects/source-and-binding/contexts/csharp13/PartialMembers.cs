namespace SourceBinding.CSharp13;

public partial class PartialDemo13
{
    public partial string Label { get; set; }

    public partial int this[int index] { get; set; }

    partial void LegacyHook(int value);

    public partial void ExtendedHook(int value);

    private string _label = string.Empty;
    private int[] _data = new int[4];
    private static int _counter;

    private static int ProduceSideEffect()
    {
        _counter++;
        return _counter;
    }

    public void Trigger()
    {
        LegacyHook(ProduceSideEffect());
        ExtendedHook(7);
        _ = Label;
        _ = this[0];
    }
}

public partial class PartialDemo13
{
    public partial string Label
    {
        get => _label;
        set => _label = value;
    }

    public partial int this[int index]
    {
        get => _data[index];
        set => _data[index] = value;
    }

    public partial void ExtendedHook(int value) => _label = value.ToString();
}
