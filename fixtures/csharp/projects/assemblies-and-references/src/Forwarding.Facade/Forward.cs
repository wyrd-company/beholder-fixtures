using System.Runtime.CompilerServices;

[assembly: TypeForwardedTo(typeof(Acme.Forwarding.RelocatedType))]

namespace Acme.Forwarding.FacadeDocs;

// Facade assembly contains no definition of RelocatedType; it forwards to Forwarding.Definition.
// The forwarding metadata allows binaries compiled against the facade to load the type
// from the definition assembly at runtime. This mirrors a type moved between assemblies.
public static class FacadeInfo
{
    public const string ForwardedTypeName = "Acme.Forwarding.RelocatedType";
    public const string ForwardTargetAssembly = "Forwarding.Definition";
}
