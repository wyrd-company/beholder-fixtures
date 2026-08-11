// CS-CAN-101: net10.0-specific compilation input — only included when TargetFramework == net10.0.
#if NET10_0
namespace Catalog.Packages.TfmSpecific;

public sealed class TfmSpecificFeature
{
    public string Target => "net10.0";
    public int ApiLevel => 10;
}
#endif
