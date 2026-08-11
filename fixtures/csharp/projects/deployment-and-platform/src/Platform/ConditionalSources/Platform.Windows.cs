namespace Acme.Deployment.Platform;

public static class PlatformConditionedOperations
{
    // This file is included only when building on Windows (MSBuild IsOSPlatform('Windows')).
    public static string DescribePlatform() => "windows-conditioned";

#if RID_WIN_X64
    public static string DescribeArchitecture() => "win-x64";
#else
    public static string DescribeArchitecture() => "win-generic";
#endif

    public static string WindowsSpecificHelper() => "windows-helper";
}
