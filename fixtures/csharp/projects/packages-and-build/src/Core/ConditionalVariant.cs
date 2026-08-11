// CS-CAN-100: conditional MSBuild properties/items and compiler constants — configuration, platform, custom property, Choose/When.
namespace Catalog.Packages;

public static class ConditionalVariant
{
#if DEBUG_CHOICE
    public const string ChosenBranch = "Debug";
#elif RELEASE_CHOICE
    public const string ChosenBranch = "Release";
#else
    public const string ChosenBranch = "Otherwise";
#endif

#if RELEASE_BUILD
    public const string ConfigName = "Release";
#else
    public const string ConfigName = "Debug";
#endif

#if EXPERIMENTAL
    public const string FeatureFlag = "ExperimentalOn";
#else
    public const string FeatureFlag = "ExperimentalOff";
#endif

    public static string DescribeConfiguration() => $"{ChosenBranch}/{ConfigName}/{FeatureFlag}";
}
