// CS-CAN-095: package graph and asset separation consumption.
// CS-CAN-097: contentFiles source-distributed asset is emitted into this assembly.
// Per-TFM package items differ: net10.0 has direct/transitive/content assets; netstandard2.1 shows distinct compilation shape without those assets (CS-CAN-101).
#if NET10_0
using Acme.CoreLib;
using Acme.TransitiveLib;
using Acme.ContentPackage; // contentFiles type emitted into consumer on net10.0
#endif

namespace Catalog.Packages;

public sealed class PackageConsumers
{
#if NET10_0
    // Direct PackageReference (compile + runtime) — Acme.CoreLib (only on net10.0)
    public CoreWidget CreateCoreWidget() => new CoreWidget { Label = "direct" };

    // Transitive PackageReference — Acme.CoreLib via Acme.TransitiveLib (only on net10.0)
    public TransitiveWidget CreateTransitiveWidget() => new TransitiveWidget { Label = "transitive" };
#else
    // netstandard2.1 has no direct/transitive package graph; distinct compilation inputs per TFM.
    public string CreateCoreWidget() => "netstandard-no-package";
    public string CreateTransitiveWidget() => "netstandard-no-transitive";
#endif

    // BuildTransitive assets flow via Acme.BuildTools (MSBuild props/targets imported transitively) — net10.0 only.
    public bool IsBuildToolsImported
    {
        get
        {
#if BUILD_TOOLS_IMPORTED
            return true;
#else
            return false;
#endif
        }
    }

    // Analyzer assets do not affect runtime; their presence is via PrivateAssets/analyzers separation.
    // The analyzer package Acme.Analyzer contributes only analyzers; no runtime type is referenced here.

#if NET10_0
    // CS-CAN-097: contentFiles-distributed C# source is compiled as part of this assembly on net10.0.
    public ContentPayload CreateContentPayload() => new ContentPayload { Text = "from-contentFiles" };

    public string DescribeContentPayloadFile()
    {
        return typeof(ContentPayload).Assembly.GetName().Name ?? "unknown";
    }
#else
    public string CreateContentPayload() => "netstandard-no-content";
    public string DescribeContentPayloadFile() => "netstandard";
#endif
}
