using Acme.Forwarding;

namespace Acme.Forwarding.Legacy;

public sealed class LegacyConsumer
{
    public string ConsumeDirect()
    {
        // This consumer is built against Forwarding.Facade.PreMove, which defines
        // RelocatedType directly under the assembly name "Forwarding.Facade" -- the
        // pre-move shape of that identity. The post-move Forwarding.Facade project later
        // replaces that definition with TypeForwardedTo metadata pointing at
        // Forwarding.Definition, so a binary built against this pre-move shape is the
        // "before the move" half of the forwarding pair.
        var instance = new RelocatedType();
        var nested = new RelocatedType.NestedPayload();
        return $"{instance.Describe()} + {nested.Label} via pre-move Facade binary";
    }

    public string ReflectDeclaringAssembly()
    {
        var type = typeof(RelocatedType);
        return $"DeclaringAssembly={type.Assembly.GetName().Name}, Location={type.Assembly.Location}";
    }
}
