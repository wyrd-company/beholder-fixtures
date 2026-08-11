using Acme.Graph.Core;
using Acme.Graph.Middle;

namespace Acme.Graph.App;

public sealed class AppConsumer
{
    public string ConsumeTransitive()
    {
        // TransitType is reachable transitively via Middle, even though the direct
        // reference to Core is build-only (ReferenceOutputAssembly=false).
        var transit = new MiddleService().CreateTransit();
        TransitType direct = transit;
        return direct.Describe() + " via " + new MiddleService().Forward();
    }

    // This would fail if we tried to directly instantiate Core without the
    // transitive path, but the build-only edge still provides compile-time visibility:
    public CoreHelper CreateHelperViaBuildOnlyEdge() => new CoreHelper();
}
