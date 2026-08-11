using Acme.Forwarding;

namespace Acme.Forwarding.Current;

public sealed class CurrentConsumer
{
    public string ConsumeViaFacade()
    {
        // Binary compiled after the move references the facade, which forwards to the definition.
        // At runtime the CLR follows the forwarding to Forwarding.Definition.
        var instance = new RelocatedType();
        return $"{instance.Describe()} via forwarding facade; Version={instance.Version}";
    }

    public string ReflectForwardingAssembly()
    {
        var type = typeof(RelocatedType);
        // Assembly where type is forwarded from vs where it is actually defined
        return $"RequestedAssembly=Forwarding.Facade, ActualAssembly={type.Assembly.GetName().Name}";
    }
}
