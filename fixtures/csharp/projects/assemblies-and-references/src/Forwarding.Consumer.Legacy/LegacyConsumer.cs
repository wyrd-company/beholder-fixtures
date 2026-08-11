using Acme.Forwarding;

namespace Acme.Forwarding.Legacy;

public sealed class LegacyConsumer
{
    public string ConsumeDirect()
    {
        // Binary compiled before the move referenced RelocatedType in its original assembly.
        // After the move, if the original assembly had TypeForwardedTo, this still resolves.
        // Here legacy consumer references the definition directly (post-move location),
        // simulating a consumer rebuilt after the move.
        var instance = new RelocatedType();
        var nested = new RelocatedType.NestedPayload();
        return $"{instance.Describe()} + {nested.Label} via direct reference";
    }

    public string ReflectDeclaringAssembly()
    {
        var type = typeof(RelocatedType);
        return $"DeclaringAssembly={type.Assembly.GetName().Name}, Location={type.Assembly.Location}";
    }
}
