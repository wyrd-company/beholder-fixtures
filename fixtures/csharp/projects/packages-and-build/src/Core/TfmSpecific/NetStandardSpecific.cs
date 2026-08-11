// CS-CAN-101: netstandard2.1-specific compilation input — only included when TargetFramework == netstandard2.1.
#if NETSTANDARD2_1
namespace Catalog.Packages.TfmSpecific;

public sealed class TfmSpecificFeatureStandard
{
    public string Target => "netstandard2.1";
    public int ApiLevel => 21;
}
#endif
