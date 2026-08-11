namespace Acme.Deployment.Platform;

public static class RuntimeIdentifierAssets
{
    public static string CurrentRidAsset()
    {
#if RID_LINUX_X64
        return "assets/native/linux-x64/libnative.so";
#elif RID_WIN_X64
        return "assets/native/win-x64/native.dll";
#else
        return "assets/native/unknown";
#endif
    }

    public static string DescribePublishPlatform()
    {
#if RID_LINUX_X64
        return "linux-x64-publish";
#elif RID_WIN_X64
        return "win-x64-publish";
#else
        return "generic-publish";
#endif
    }
}
