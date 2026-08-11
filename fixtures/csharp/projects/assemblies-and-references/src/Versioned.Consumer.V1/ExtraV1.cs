using Acme.Versioned;

namespace Acme.Versioned.ConsumerV1;

// Version-specific extra, distinct from the controlled shared consumer input in
// Versioned.Consumer.Shared: RemovedMemberDemo.ToBeRemovedInV2 exists only in
// Versioned.Api.V1, so a call to it is valid source in this V1-only consumer and would not
// be valid if that call were part of the input shared with V2.
public sealed class VersionedConsumerExtras
{
    public void ConsumeRemovedMember()
    {
        var demo = new RemovedMemberDemo();
        demo.ToBeRemovedInV2();
    }
}
