using System.Runtime.InteropServices;

namespace Fixture.AttributesAndMetadata.Core.NonInvariant;

/// <summary>
/// CS-CAN-128: parameterizes pointer size, endianness, floating-point excess
/// precision, filesystem path/case behavior, and native-symbol lookup by the
/// x64 platform actually available to this corpus; non-x64 architecture and
/// endianness observations are excepted in the accepted plan overview as an
/// unavailable context.
/// </summary>
public static class PlatformAbiLatitude
{
    public static string DescribePointerSize() => $"native-int-size-bytes={nint.Size}";

    public static string DescribeEndianness() => $"is-little-endian={BitConverter.IsLittleEndian}";

    public static string DescribeFloatingExcessPrecision()
    {
        var computed = 0.1 + 0.2;
        return $"floating-result-class={(computed == 0.3 ? "exact" : "excess-or-rounded")}";
    }

    public static string DescribePathBehavior()
        => $"path-separator={Path.DirectorySeparatorChar} is-windows={OperatingSystem.IsWindows()}";

    public static string DescribeNativeLookup()
    {
        var loaded = NativeLibrary.TryLoad("libc", out var handle);
        if (loaded)
        {
            NativeLibrary.Free(handle);
        }

        return $"native-library-probe-attempted=true loaded={loaded}";
    }
}
