using Acme.Forwarding;

namespace Acme.Forwarding.Current;

public sealed class CurrentConsumer
{
    public string ConsumeViaFacade()
    {
        // This binary's source references the post-move Forwarding.Facade, which forwards
        // RelocatedType to Forwarding.Definition. The C# compiler follows TypeForwardedTo at
        // COMPILE time, so the emitted Forwarding.Consumer.Current binary references
        // Forwarding.Definition directly (its metadata names no RelocatedType in
        // Forwarding.Facade). No forward is followed at run time for this binary. The run-time
        // forward for a pre-move binary is demonstrated separately by Forwarding.Composition.
        var instance = new RelocatedType();
        return $"{instance.Describe()} via forwarding facade; Version={instance.Version}";
    }

    public string ReflectForwardingAssembly()
    {
        // Because the compiler already resolved the forward, RelocatedType simply resolves in
        // the assembly this binary references directly (Forwarding.Definition); there is no
        // facade forward to follow at run time here.
        var type = typeof(RelocatedType);
        return $"SourceReferencedFacade=Forwarding.Facade, RuntimeAssembly={type.Assembly.GetName().Name}";
    }
}
