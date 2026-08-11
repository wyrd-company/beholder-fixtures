namespace Bakery.TypesAndValues.Core.Enums;

// CS-CAN-032: enums — explicit underlying types, aliases, duplicate values,
// unnamed numeric values, flags usage, conversions, switches, boxing, generic constraints.

public enum BakeKind
{
    Plain = 0,
    Sourdough = 1,
    Rye = 2,
}

public enum BakeKindByte : byte
{
    Raw = 0,
    Light = 1,
    Perfect = 2,
}

public enum BakeKindShort : short
{
    Starter = -1,
    Plain = 0,
    Enriched = 1,
}

public enum BakeAlias : int
{
    Plain = 0,
    Sourdough = 1,
    French = 1,
    Rye = 2,
    Pumpernickel = 2,
}

public enum TrayFlags
{
    None = 0,
    ContainsSourdough = 1,
    ContainsRye = 2,
    ContainsBrioche = 4,
    Assorted = ContainsSourdough | ContainsRye | ContainsBrioche,
}

[Flags]
public enum BakeFlags : int
{
    None = 0,
    Golden = 1,
    Crusty = 2,
    Seeded = 4,
    GoldenCrusty = Golden | Crusty,
}

public static class EnumExercises
{
    public static BakeKind FromInt(int value) => (BakeKind)value;

    public static int ToInt(BakeKind kind) => (int)kind;

    public static BakeKindByte FromByte(byte value) => (BakeKindByte)value;

    public static bool HasFlag(BakeFlags flags, BakeFlags test) => flags.HasFlag(test);

    public static BakeFlags Combine(BakeFlags left, BakeFlags right) => left | right;

    public static TrayFlags AssortedFlags() => TrayFlags.Assorted;

    public static bool AliasEqual()
    {
        return BakeAlias.Sourdough == BakeAlias.French &&
               BakeAlias.Rye == BakeAlias.Pumpernickel;
    }

    public static bool UnnamedNumericValue()
    {
        BakeKind unknown = (BakeKind)99;
        bool isDefined = Enum.IsDefined(typeof(BakeKind), unknown);
        _ = unknown;
        return !isDefined;
    }

    public static string SwitchExhaustive(BakeKind kind) => kind switch
    {
        BakeKind.Plain => "plain",
        BakeKind.Sourdough => "sourdough",
        BakeKind.Rye => "rye",
        _ => "unknown",
    };

    public static string SwitchNonClosedWithDefault(BakeKind kind)
    {
        switch (kind)
        {
            case BakeKind.Plain:
                return "plain";
            case BakeKind.Sourdough:
                return "sourdough";
            default:
                return "other";
        }
    }

    public static object BoxEnum(BakeKind kind) => kind;

    public static BakeKind UnboxEnum(object boxed) => (BakeKind)boxed;

    public static bool BoxedEquality(BakeKind left, BakeKind right)
    {
        object a = left;
        object b = right;
        return a.Equals(b) == (left == right);
    }

    public static T ParseEnum<T>(string name) where T : struct, Enum =>
        Enum.Parse<T>(name);

    public static bool TryParseEnum<T>(string name, out T result) where T : struct, Enum =>
        Enum.TryParse(name, out result);

    public static T GenericConstraint<T>(T value) where T : Enum => value;

    public static void StaleConstantObservation()
    {
        // Enum constants are baked as literals at call sites; cross-assembly
        // recompilation would show stale values, but this project is self-contained.
        int baked = (int)BakeKind.Sourdough;
        _ = baked;
    }
}
