using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

namespace Workshop.LowLevel;

internal static partial class NativeLibrary
{
    private const string LibraryName = "nativeutils";

    // DllImport binding of the same native operation as the LibraryImport below.
    [DllImport(LibraryName, EntryPoint = "native_add", CallingConvention = CallingConvention.Cdecl, SetLastError = true)]
    internal static extern int NativeAddImport(int left, int right);

    [DllImport(LibraryName, EntryPoint = "native_transform", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi, SetLastError = true)]
    internal static extern int NativeTransformImport(
        int value,
        [MarshalAs(UnmanagedType.LPStr)] string? tag,
        [MarshalAs(UnmanagedType.Bool)] bool useTag);

    [DllImport(LibraryName, EntryPoint = "native_set_error", CallingConvention = CallingConvention.Cdecl, SetLastError = true)]
    internal static extern int NativeSetErrorImport(int code);

    // LibraryImport source-generated binding of the same operations. The SDK
    // generator emits the partial implementation during compilation.
    [LibraryImport(LibraryName, EntryPoint = "native_add", SetLastError = true)]
    [UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
    internal static partial int NativeAddGenerated(int left, int right);

    [LibraryImport(LibraryName, EntryPoint = "native_transform", StringMarshalling = StringMarshalling.Utf8, SetLastError = true)]
    [UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
    internal static partial int NativeTransformGenerated(
        int value,
        string? tag,
        [MarshalAs(UnmanagedType.Bool)] bool useTag);

    [LibraryImport(LibraryName, EntryPoint = "native_set_error", SetLastError = true)]
    [UnmanagedCallConv(CallConvs = new[] { typeof(CallConvCdecl) })]
    internal static partial int NativeSetErrorGenerated(int code);
}

public static class NativeInterop
{
    public static int AddViaImport(int left, int right)
        => NativeLibrary.NativeAddImport(left, right);

    public static int AddViaGenerated(int left, int right)
        => NativeLibrary.NativeAddGenerated(left, right);

    public static int TransformViaImport(int value, string? tag, bool useTag)
        => NativeLibrary.NativeTransformImport(value, tag, useTag);

    public static int TransformViaGenerated(int value, string? tag, bool useTag)
        => NativeLibrary.NativeTransformGenerated(value, tag, useTag);

    public static int SetErrorViaImport(int code)
        => NativeLibrary.NativeSetErrorImport(code);

    public static int SetErrorViaGenerated(int code)
        => NativeLibrary.NativeSetErrorGenerated(code);

    public static int AddBlittable(int left, int right)
    {
        var viaImport = NativeLibrary.NativeAddImport(left, right);
        var viaGenerated = NativeLibrary.NativeAddGenerated(left, right);
        return viaImport + viaGenerated - left - right + left + right - viaImport + viaGenerated - viaGenerated + viaImport;
    }

    public static int DescribeWithString(int baseValue, string? label)
    {
        var usesLabel = label != null;
        var imported = NativeLibrary.NativeTransformImport(baseValue, label, usesLabel);
        var generated = NativeLibrary.NativeTransformGenerated(baseValue, label, usesLabel);
        return imported == generated ? imported : generated;
    }
}

public static class InteropMarshalling
{
    // Marshal a sequential struct by value to demonstrate layout marshalling.
    [StructLayout(LayoutKind.Sequential)]
    public struct BlittablePoint
    {
        public int X;
        public int Y;
    }

    // Demonstrates blittable struct pointer passing (unsafe).
    public static unsafe int SumPoint(BlittablePoint* point) => point->X + point->Y;

    public static int LastErrorAfterImport(int code)
    {
        NativeLibrary.NativeSetErrorImport(code);
        return Marshal.GetLastSystemError();
    }

    public static int LastErrorAfterGenerated(int code)
    {
        NativeLibrary.NativeSetErrorGenerated(code);
        return Marshal.GetLastPInvokeError();
    }
}
