// CS-CAN-100: conditional MSBuild properties/items and compiler constants with Choose/When.
namespace Catalog.Packages.ConditionalVariant;

public static class Variant
{
#if EXPERIMENTAL
    public const string Feature = "Experimental";
#elif STABLE
    public const string Feature = "Stable";
#else
    public const string Feature = "Unknown";
#endif

#if RELEASE_BUILD
    public const string Config = "Release";
#else
    public const string Config = "Debug";
#endif

#if PLATFORM_X64
    public const string Platform = "x64";
#else
    public const string Platform = "AnyCPU";
#endif

#if RID_LINUX_X64
    public const string Rid = "linux-x64";
#else
    public const string Rid = "default-rid";
#endif

    public static string Describe() => $"{Feature}/{Config}/{Platform}/{Rid}";
}
