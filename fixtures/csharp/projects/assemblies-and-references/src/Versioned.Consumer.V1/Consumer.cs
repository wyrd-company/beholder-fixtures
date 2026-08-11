using Acme.Versioned;

namespace Acme.Versioned.ConsumerV1;

public sealed class VersionedConsumer
{
    public string ConsumeConstants()
    {
        // Constants are baked at compile time: ApiConstants.ApiConstant is inlined as literal "v1-constant".
        // Running this consumer against V2 implementation without recompilation would still observe stale "v1-constant".
        return ApiConstants.ApiConstant + ":" + ApiConstants.ApiValue;
    }

    public string ConsumeOptionalDefault()
    {
        // Optional default baked at call site: Greet() is compiled as Greet("WorldV1").
        return OptionalDefaults.Greet();
    }

    public string ConsumeOverload()
    {
        // Resolves to single overload available in V1.
        return OverloadSet.Execute("payload");
    }

    public string ConsumeVirtual()
    {
        WidgetBase w = new WidgetBase();
        return w.Describe();
    }

    public void ConsumeRemovedMember()
    {
        var demo = new RemovedMemberDemo();
        demo.ToBeRemovedInV2(); // Present in V1, would throw MissingMethodException if run against V2
    }

    public void ConsumeInterface(IApiContract contract) => contract.LegacyOperation();
}
