// CS-CAN-012 + CS-CAN-100: conditional source for custom MSBuild property EnableExperimentalFeature.
#if EXPERIMENTAL
namespace Catalog.Packages.Conditional;

public sealed class ExperimentalFeature
{
    public string Flag => "Experimental";
}
#endif
