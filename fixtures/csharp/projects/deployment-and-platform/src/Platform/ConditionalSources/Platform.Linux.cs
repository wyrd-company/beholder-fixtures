namespace Acme.Deployment.Platform;

public static class PlatformConditionedOperations
{
    // This file is included only when building on Linux (MSBuild IsOSPlatform('Linux')).
    // The Windows counterpart lives in Platform.Windows.cs.
    public static string DescribePlatform() => "linux-conditioned";

#if RID_LINUX_X64
    public static string DescribeArchitecture() => "linux-x64";
#else
    public static string DescribeArchitecture() => "linux-generic";
#endif

    public static string LinuxSpecificHelper() => "linux-helper";
}
