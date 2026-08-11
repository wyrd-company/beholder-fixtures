using Acme.Versioned;

namespace Acme.Versioned.ConsumerV2;

// Version-specific extra, distinct from the controlled shared consumer input in
// Versioned.Consumer.Shared: the two-argument OverloadSet.Execute overload and
// IApiContract.NewDefaultOperation only exist in Versioned.Api.V2, so calls to them are
// valid source in this V2-only consumer and would not be valid if shared with V1.
public sealed class VersionedConsumerExtras
{
    public string ConsumeNewOverload()
    {
        return OverloadSet.Execute("payload", 3);
    }

    public void ConsumeNewDefaultInterface(IApiContract contract) => contract.NewDefaultOperation();
}
