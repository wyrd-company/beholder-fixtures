using System.Runtime.CompilerServices;

[assembly: TypeForwardedTo(typeof(Acme.Forwarding.RelocatedType))]

namespace Acme.Forwarding.FacadeDocs;

// This is the post-move shape of the "Forwarding.Facade" identity: it contains no definition
// of RelocatedType and forwards to Forwarding.Definition instead. Forwarding.Facade.PreMove
// is the pre-move shape of that same identity, where RelocatedType was still defined here
// directly. The forwarding metadata lets binaries compiled against either shape locate the
// type: pre-move binaries via the type this facade used to define, post-move binaries via
// the facade forwarding to Forwarding.Definition.
public static class FacadeInfo
{
    public const string ForwardedTypeName = "Acme.Forwarding.RelocatedType";
    public const string ForwardTargetAssembly = "Forwarding.Definition";
}
