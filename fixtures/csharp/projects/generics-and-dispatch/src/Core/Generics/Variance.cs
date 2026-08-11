namespace GenericsAndDispatch.Core.Generics;

public interface IProducer<out T>
{
    T Produce();
}

public interface IConsumer<in T>
{
    void Consume(T value);
}

public interface ITransformer<in TIn, out TOut>
{
    TOut Transform(TIn value);
}

public delegate T Factory<out T>(int seed);

public delegate void Sink<in T>(T value);

public class Producer<T> : IProducer<T>
{
    private readonly T _value;
    public Producer(T value) => _value = value;
    public T Produce() => _value;
}

public class Consumer<T> : IConsumer<T>
{
    public T? Last { get; private set; }
    public void Consume(T value) => Last = value;
}

public class Animal
{
    public string Name { get; init; }
    public Animal(string name) => Name = name;
}

public sealed class Dog : Animal
{
    public Dog(string name) : base(name) { }
}

public static class VarianceExercises
{
    public static void Run()
    {
        // Covariant interface conversion: producer of Dog is producer of Animal.
        IProducer<Dog> dogProducer = new Producer<Dog>(new Dog("pup"));
        IProducer<Animal> animalProducer = dogProducer;
        Animal produced = animalProducer.Produce();

        // Contravariant interface conversion: consumer of Animal accepts Dog.
        IConsumer<Animal> animalConsumer = new Consumer<Animal>();
        IConsumer<Dog> dogConsumer = animalConsumer;
        dogConsumer.Consume(new Dog("spot"));

        // Variant delegates: method group, overload, pattern, runtime cast.
        Factory<Dog> dogFactory = CreateDog;
        Factory<Animal> animalFactory = dogFactory;
        Animal factoryAnimal = animalFactory(1);

        Sink<Animal> animalSink = ConsumeAnimal;
        Sink<Dog> dogSink = animalSink;
        dogSink(new Dog("rex"));

        // Runtime variance cast.
        object boxedProducer = new Producer<Dog>(new Dog("box"));
        var covariantCast = (IProducer<Animal>)boxedProducer;

        // Overload selection prefers variant delegate target.
        string byProducer = Describe(dogProducer);
        string byConsumer = Describe(animalConsumer);

        // Pattern matching respects variance.
        string patternResult = animalProducer is IProducer<Animal> ? "producer" : "none";

        // Method group variance.
        Factory<Dog> byMethodGroup = static seed => new Dog($"dog-{seed}");

        _ = produced;
        _ = factoryAnimal;
        _ = covariantCast;
        _ = byProducer;
        _ = byConsumer;
        _ = patternResult;
        _ = byMethodGroup;
    }

    private static Dog CreateDog(int seed) => new($"dog-{seed}");

    private static void ConsumeAnimal(Animal animal) => _ = animal.Name;

    private static string Describe(IProducer<Animal> producer) => producer.Produce().Name;

    private static string Describe(IConsumer<Animal> consumer) => consumer is Consumer<Animal> c ? c.Last?.Name ?? "empty" : "unknown";
}
