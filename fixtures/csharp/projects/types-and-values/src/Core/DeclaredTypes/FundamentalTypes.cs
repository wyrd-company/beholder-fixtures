namespace Bakery.TypesAndValues.Core.DeclaredTypes;

// CS-CAN-019: fundamental declared type kinds — class, static/abstract/sealed class,
// struct, interface, enum, delegate with construction, conversion, inheritance, copy, boxing, calls.

public class Pastry
{
    public string Name { get; }

    public Pastry(string name) => Name = name;

    public virtual string Describe() => $"Pastry:{Name}";
}

public sealed class Croissant : Pastry
{
    public int Layers { get; }

    public Croissant(string name, int layers) : base(name) => Layers = layers;

    public override string Describe() => $"Croissant:{Name}:{Layers}";
}

public abstract class BakedGood
{
    public abstract TimeSpan BakeTime { get; }

    public virtual string Category => "baked";
}

public sealed class Bread : BakedGood
{
    public override TimeSpan BakeTime => TimeSpan.FromMinutes(30);
}

public static class BakeryOps
{
    public static int TotalLayers(Croissant croissant) => croissant.Layers;

    public static Pastry CreatePastry(string name) => new Pastry(name);
}

public struct Crumb
{
    public int WeightGrams;

    public Crumb(int weightGrams) => WeightGrams = weightGrams;

    public void AddWeight(int delta) => WeightGrams += delta;
}

public interface IBakable
{
    string Name { get; }

    void Bake();
}

public sealed class BakablePastry : IBakable
{
    public string Name { get; }

    public BakablePastry(string name) => Name = name;

    public void Bake() { }
}

public enum BakeLevel : byte
{
    Raw = 0,
    Light = 1,
    Golden = 2,
    Dark = 3,

    Perfect = Golden,
}

public delegate Pastry PastryFactory(string name);

public delegate TResult MapFactory<out TResult>(int seed);

public static class FundamentalExercises
{
    public static Pastry NewPastry() => new Pastry("plain");

    public static Croissant NewCroissant() => new Croissant("butter", 24);

    public static BakedGood NewBreadAsAbstract() => new Bread();

    public static Crumb NewCrumb() => new Crumb(5);

    public static IBakable NewBakable() => new BakablePastry("sourdough");

    public static PastryFactory FactoryMethodGroup => BakeryOps.CreatePastry;

    public static PastryFactory FactoryLambda => name => new Pastry(name);

    public static BakeLevel ToBakeLevel(int value) => (BakeLevel)value;

    public static int FromBakeLevel(BakeLevel level) => (int)level;

    public static void ExerciseConversions()
    {
        Pastry pastry = new Croissant("almond", 18);
        Croissant croissant = (Croissant)pastry;
        _ = croissant.Layers;

        IBakable bakable = new BakablePastry("rye");
        object boxedCrumb = new Crumb(7);
        Crumb unboxed = (Crumb)boxedCrumb;
        _ = unboxed.WeightGrams;

        Pastry baseAsDerived = croissant;
        _ = baseAsDerived.Describe();

        MapFactory<Pastry> covariant = seed => new Pastry($"seed-{seed}");
        MapFactory<object> converted = covariant;
        _ = converted(1);

        BakeLevel alias = BakeLevel.Perfect;
        _ = (byte)alias;
        _ = bakable.Name;
    }

    public static void ExerciseCopyAndMutation()
    {
        Crumb left = new Crumb(10);
        Crumb copy = left;
        copy.AddWeight(5);
        bool copyIsIndependent = left.WeightGrams == 10 && copy.WeightGrams == 15;
        _ = copyIsIndependent;

        object boxed = new Crumb(12);
        Crumb second = (Crumb)boxed;
        second.AddWeight(3);
        _ = ((Crumb)boxed).WeightGrams == 12 && second.WeightGrams == 15;
    }

    public static string ExerciseInterfaceDispatch(IBakable bakable)
    {
        bakable.Bake();
        return bakable.Name;
    }

    public static void ExerciseDelegateMulticast()
    {
        PastryFactory first = name => new Pastry(name + "-a");
        PastryFactory second = name => new Pastry(name + "-b");
        PastryFactory combined = first + second;
#pragma warning disable CS8601
        combined = (PastryFactory)Delegate.Remove(combined, first)!;
        Pastry result = combined("test");
        _ = result.Name;
        combined -= second;
#pragma warning restore CS8601
        _ = combined is null;
    }
}
