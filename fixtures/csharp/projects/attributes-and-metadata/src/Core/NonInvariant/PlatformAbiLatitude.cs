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

    public static string DescribeNativeIntRange()
        // Parameterized by pointer width; on this x64 host the native
        // integer range matches Int64's, but that is never asserted as a
        // portable constant.
        => $"native-int-max={nint.MaxValue} native-int-min={nint.MinValue}";

    [StructLayout(LayoutKind.Sequential)]
    private struct PaddedLayout
    {
        public byte Flag;
        public long Value;
    }

    public static string DescribeLayoutPadding()
    {
        // Padding inserted between differently sized fields is
        // platform/ABI-determined; only the resulting managed size is
        // observed, never asserted as a fixed cross-platform constant.
        var size = Marshal.SizeOf<PaddedLayout>();
        return $"padded-layout-size-bytes={size}";
    }

    public static string DescribeFilesystemCaseAndNewlineLatitude()
    {
        var newline = Environment.NewLine;

        // Filesystem case-folding is host-determined: on a case-insensitive
        // volume a case-toggled spelling of an existing directory still
        // resolves, on a case-sensitive one it does not. The result is
        // parameterized by the running platform's filesystem and never
        // asserted as a portable constant.
        var baseDir = AppContext.BaseDirectory
            .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        var toggled = ToggleAsciiLetterCase(baseDir);
        var caseFolds = !string.Equals(toggled, baseDir, StringComparison.Ordinal)
            && Directory.Exists(toggled);

        return $"newline-length={newline.Length} newline-is-lf={newline == "\n"} "
            + $"alt-separator={Path.AltDirectorySeparatorChar} filesystem-case-folds={caseFolds}";
    }

    private static string ToggleAsciiLetterCase(string value)
    {
        var chars = value.ToCharArray();
        for (var i = 0; i < chars.Length; i++)
        {
            var c = chars[i];
            if (char.IsAsciiLetterUpper(c))
            {
                chars[i] = char.ToLowerInvariant(c);
            }
            else if (char.IsAsciiLetterLower(c))
            {
                chars[i] = char.ToUpperInvariant(c);
            }
        }

        return new string(chars);
    }

    public static string DescribeMemoryReorderingLatitude()
    {
        var flag = 0;

        // Whether the runtime or CPU may reorder surrounding memory
        // operations absent this barrier is never asserted; only that the
        // barrier API is available and usable.
        Volatile.Write(ref flag, 1);
        var observed = Volatile.Read(ref flag);
        return $"memory-reordering-barrier-observed-value={observed}";
    }
}
