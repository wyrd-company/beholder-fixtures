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
