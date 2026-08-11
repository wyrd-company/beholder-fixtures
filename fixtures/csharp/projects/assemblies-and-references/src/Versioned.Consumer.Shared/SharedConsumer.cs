using Acme.Versioned;

namespace Acme.Versioned.Consumer;

// Controlled consumer input: this single source file is linked, unmodified, into both
// Versioned.Consumer.V1 (referencing Versioned.Api.V1) and Versioned.Consumer.V2
// (referencing Versioned.Api.V2). Recompiling this identical source against each producer
// version is what changes the observed binding below, not a change to the consumer source.
public sealed class SharedConsumer
{
    public string ConsumeConstants()
    {
        // ApiConstants.ApiConstant is a const, baked into IL at compile time: recompiling
        // this unchanged call against V1 vs V2 bakes in a different literal value.
        return ApiConstants.ApiConstant + ":" + ApiConstants.ApiValue;
    }

    public string ConsumeOptionalDefault()
    {
        // The optional-parameter default is also baked at the call site: recompiling this
        // unchanged no-arg call against V2 bakes in V2's default argument instead of V1's.
        return OptionalDefaults.Greet();
    }

    public string ConsumeOverload()
    {
        // The single-argument overload exists unchanged in both versions, so this call's
        // binding is stable across recompilation even though V2 adds a second overload.
        return OverloadSet.Execute("payload");
    }

    public string ConsumeVirtualDispatch()
    {
        // WidgetBase.Describe() is virtual in V1 and non-virtual in V2: the emitted call
        // instruction (callvirt vs call) and the returned literal both change on
        // recompilation against the other producer version, though this call site does not.
        WidgetBase w = new WidgetBase();
        return w.Describe();
    }

    public void ConsumeInterface(IApiContract contract) => contract.LegacyOperation();
}
