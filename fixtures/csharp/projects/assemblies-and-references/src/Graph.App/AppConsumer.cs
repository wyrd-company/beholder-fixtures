using Acme.Graph.Core;
using Acme.Graph.Middle;

namespace Acme.Graph.App;

public sealed class AppConsumer
{
    public string ConsumeTransitive()
    {
        // TransitType and CoreHelper are both visible here because MSBuild flows
        // project references transitively: Graph.App -> Graph.Middle -> Graph.Core makes
        // Graph.Core's public surface visible at compile time through Graph.Middle alone.
        var transit = new MiddleService().CreateTransit();
        TransitType direct = transit;
        return direct.Describe() + " via " + new MiddleService().Forward();
    }

    // The separate direct ProjectReference to Graph.Core in Graph.App.csproj sets
    // ReferenceOutputAssembly=false: it adds a build-ordering edge only and supplies no
    // compiler reference of its own. CoreHelper below still compiles because Graph.Core is
    // already visible transitively through Graph.Middle, not because of this build-only edge.
    public CoreHelper CreateHelperViaBuildOnlyEdge() => new CoreHelper();
}
