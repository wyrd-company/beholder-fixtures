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
        // WidgetBase.Describe() is declared virtual in Versioned.Api.V1 and non-virtual in
        // Versioned.Api.V2 -- a producer member-shape change. Recompiling this unchanged call
        // against each producer binds to that version's Describe(), and the returned literal
        // changes ("WidgetBase V1 virtual" vs "WidgetBase V2 non-virtual"), though this call
        // site does not change. The producer's virtual-versus-non-virtual member shape and the
        // observed return value are the recompilation-visible differences.
        WidgetBase w = new WidgetBase();
        return w.Describe();
    }

    public void ConsumeInterface(IApiContract contract) => contract.LegacyOperation();
}
