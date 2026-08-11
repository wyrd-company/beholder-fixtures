using Acme.ReferenceAssemblyDemo;

namespace Acme.ReferenceAssemblyDemo.Consumer;

public sealed class RefConsumer
{
    public string UseReferenceFeature()
    {
        // Compiles against the reference assembly produced by ReferenceAssembly.Producer
        // (obj/.../ref/*.dll which contains only public surface, no private/internal members).
        // At runtime it binds to the implementation assembly.
        var feature = new ReferenceFeature();
        return $"{feature.Message}: {feature.Compute(21)}";
    }

    public string ProbePack() => FrameworkPackProbe.DescribePack();
}

public static class Program
{
    // Runnable entry point: this consumer compiles against the project reference assembly
    // (public surface only) and, when run, executes against the implementation assembly and
    // the installed net10.0 implementation pack, which also carries the internal/private
    // members the reference assembly omits.
    public static void Main()
    {
        var consumer = new RefConsumer();
        System.Console.WriteLine(consumer.UseReferenceFeature());
        System.Console.WriteLine(consumer.ProbePack());
    }
}
