using System.Runtime.Versioning;

namespace Acme.Deployment.Platform;

public static class PlatformApis
{
    [SupportedOSPlatform("linux")]
    public static string LinuxOnlyOperation() => "linux-result";

    [SupportedOSPlatform("windows")]
    public static string WindowsOnlyOperation() => "windows-result";

    [SupportedOSPlatform("linux")]
    [SupportedOSPlatform("windows")]
    public static string CrossPlatformSupported() => "linux-or-windows";

    [UnsupportedOSPlatform("browser")]
    public static string NotSupportedOnBrowser() => "not-browser";

    [SupportedOSPlatform("linux")]
    public class LinuxOnlyService
    {
        public string Describe() => "linux-service";
    }

    [SupportedOSPlatform("windows")]
    public class WindowsOnlyService
    {
        public string Describe() => "windows-service";
    }

    [SupportedOSPlatform("browser")]
    public static string BrowserSpecific() => "browser";

    [UnsupportedOSPlatform("browser")]
    [UnsupportedOSPlatform("ios")]
    public static string DesktopOnly() => "desktop";
}

[SupportedOSPlatform("linux")]
public class LinuxAnchoredLibrary
{
    public static string Describe() => "anchored-to-linux";
}

[UnsupportedOSPlatform("browser")]
public static class BrowserGuardedApis
{
    public static string RequireBrowserUnsupportedContext() => "needs-not-browser";
}
