using Acme.Versioned;

namespace Acme.Versioned.ConsumerV2;

public sealed class VersionedConsumer
{
    public string ConsumeConstants()
    {
        // Recompiled against V2: observes new constant values.
        return ApiConstants.ApiConstant + ":" + ApiConstants.ApiValue;
    }

    public string ConsumeOptionalDefault()
    {
        // New default baked: Greet() now compiles as Greet("WorldV2").
        return OptionalDefaults.Greet();
    }

    public string ConsumeNewOverload()
    {
        // Binds to added overload introduced in V2.
        return OverloadSet.Execute("payload", 3);
    }

    public string ConsumeNonVirtual()
    {
        WidgetBase w = new WidgetBase();
        // In V2 Describe is non-virtual, dispatch change vs V1 virtual call.
        return w.Describe();
    }

    public void ConsumeNewDefaultInterface(IApiContract contract) => contract.NewDefaultOperation();

    public void ConsumeInterface(IApiContract contract) => contract.LegacyOperation();
}
