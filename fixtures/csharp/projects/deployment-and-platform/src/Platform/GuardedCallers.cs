using System.Runtime.Versioning;

namespace Acme.Deployment.Platform;

public static class GuardedCallers
{
    // Recognized guard: direct OperatingSystem.Is* call — analyzer suppresses CA1416.
    public static string CallWithRecognizedGuard()
    {
        if (OperatingSystem.IsLinux())
        {
            return PlatformApis.LinuxOnlyOperation();
        }

        if (OperatingSystem.IsWindows())
        {
            return PlatformApis.WindowsOnlyOperation();
        }

        if (OperatingSystem.IsLinux() || OperatingSystem.IsWindows())
        {
            return PlatformApis.CrossPlatformSupported();
        }

        return "fallback";
    }

    // SupportedOSPlatformGuard helper — recognized guard via attribute.
    [SupportedOSPlatformGuard("linux")]
    public static bool IsLinuxGuard() => OperatingSystem.IsLinux();

    [SupportedOSPlatformGuard("windows")]
    public static bool IsWindowsGuard() => OperatingSystem.IsWindows();

    public static string CallWithGuardAttribute()
    {
        if (IsLinuxGuard())
        {
            return PlatformApis.LinuxOnlyOperation();
        }

        if (IsWindowsGuard())
        {
            return PlatformApis.WindowsOnlyOperation();
        }

        return "fallback";
    }

    // OperatingSystem.IsOSPlatform variant — also recognized.
    public static string CallWithIsOSPlatform()
    {
        if (OperatingSystem.IsOSPlatform("Linux"))
        {
            return PlatformApis.LinuxOnlyOperation();
        }

        return "other";
    }

    // Unrecognized guard: custom helper without SupportedOSPlatformGuard attribute.
    // The analyzer does NOT recognize this, so the CA1416 warning remains.
    public static bool IsLinuxCustom() => true;

    public static string CallWithUnrecognizedGuard()
    {
        if (IsLinuxCustom())
        {
            // CA1416 expected here: unrecognized guard does not suppress.
            return PlatformApis.LinuxOnlyOperation();
        }

        return "unrecognized-fallback";
    }

    // Browser / mobile / AOT constraint: UnsupportedOSPlatform("browser") reachability.
    public static string CallBrowserUnsupported()
    {
        if (!OperatingSystem.IsBrowser())
        {
            return PlatformApis.NotSupportedOnBrowser();
        }

        return "browser-fallback";
    }

    // Flow through local variable that was guarded — analyzer tracks flow.
    public static string CallWithFlowVariable()
    {
        var isLinux = OperatingSystem.IsLinux();
        if (isLinux)
        {
            return PlatformApis.LinuxOnlyOperation();
        }

        return "not-linux";
    }

    // Verify attribute applied at type level flows to members.
    public static string CallAnchoredType()
    {
        if (OperatingSystem.IsLinux())
        {
            return LinuxAnchoredLibrary.Describe();
        }

        return "not-linux-anchored";
    }
}
