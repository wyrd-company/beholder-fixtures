namespace Bakery.TypesAndValues.CSharp11;

// CS-CAN-031: auto-default struct fields — C# 11 allows field initializers
// to provide auto-default values when a parameterless constructor leaves fields
// unassigned; the compiler fills them without explicit assignment in the constructor body.

public struct AutoDefaultCounter
{
    public int Count = 5;

    public string Label = "rye";

    public int Extra;

    public AutoDefaultCounter()
    {
        // C#11 auto-default: deliberately leave Count, Label, and Extra unassigned;
        // compiler assigns Count=5, Label="rye", Extra=0 from initializers/defaults.
    }
}

public struct AutoDefaultWithProperty
{
    public int Count { get; set; } = 11;

    public string Label { get; set; } = "brioche";

    public AutoDefaultWithProperty()
    {
        // C#11 auto-default for auto-properties: leave Count/Label unassigned.
    }
}

public struct CSharp11ExplicitAutoDefault
{
    public int Count = 77;

    public int Extra;

    public string Label = "seed";

    public CSharp11ExplicitAutoDefault()
    {
        // Deliberately leave all three fields unassigned; compiler-generated
        // assignments fill Count=77, Label="seed", Extra=0.
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

    public static bool CSharp11AutoDefaultObserved()
    {
        CSharp11ExplicitAutoDefault withNew = new();
        CSharp11ExplicitAutoDefault withDefault = default;
        bool newHasAuto = withNew.Count == 77 && withNew.Label == "seed" && withNew.Extra == 0;
        bool defaultZeroed = withDefault.Count == 0 && withDefault.Label is null && withDefault.Extra == 0;
        return newHasAuto && defaultZeroed;
    }
}
