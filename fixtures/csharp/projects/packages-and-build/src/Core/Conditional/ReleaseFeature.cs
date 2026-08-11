// CS-CAN-012 conditional source: included only when Configuration == Release.
// CS-CAN-100 configuration condition.
#if RELEASE_BUILD
namespace Catalog.Packages.Conditional;

public sealed class ReleaseFeature
{
    public string Mode => "Release";
}
#endif
