namespace Bakery.TypesAndValues.CSharp11;

// CS-CAN-031: auto-default struct fields — C# 11 allows field initializers
// to act as auto-defaults without an explicit parameterless constructor,
// and struct members can be auto-initialized.

public struct AutoDefaultCounter
{
    public int Count = 5;

    public string Label = "rye";

    public int Extra;

    public AutoDefaultCounter()
    {
    }
}

public struct AutoDefaultWithProperty
{
    public int Count { get; set; } = 11;

    public string Label { get; set; } = "brioche";

    public AutoDefaultWithProperty()
    {
    }
}

public static class AutoDefaultExercises
{
    public static AutoDefaultCounter NewVsDefault()
    {
        AutoDefaultCounter withNew = new();
        AutoDefaultCounter withDefault = default;
        _ = withDefault;
        return withNew;
    }

    public static bool ObserveDefaults()
    {
        AutoDefaultCounter withNew = new();
        AutoDefaultCounter withDefault = default;
        bool newHasInitializer = withNew.Count == 5 && withNew.Label == "rye" && withNew.Extra == 0;
        bool defaultIsZeroed = withDefault.Count == 0 && withDefault.Label is null && withDefault.Extra == 0;
        return newHasInitializer && defaultIsZeroed;
    }

    public static AutoDefaultWithProperty WithPropertyInitializer() => new();

    public static bool PropertyInitializerDefaults()
    {
        AutoDefaultWithProperty withNew = new();
        AutoDefaultWithProperty withDefault = default;
        return withNew.Count == 11 && withDefault.Count == 0 && withDefault.Label is null;
    }

    public static void AssignAllFieldsWithoutConstructor()
    {
        AutoDefaultCounter counter = new();
        counter.Count = 9;
        counter.Label = "sourdough";
        counter.Extra = 1;
        _ = counter;
    }
}
