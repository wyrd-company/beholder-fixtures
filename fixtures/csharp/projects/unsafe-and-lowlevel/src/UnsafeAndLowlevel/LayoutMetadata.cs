using System.Runtime.InteropServices;

namespace Workshop.LowLevel;

[StructLayout(LayoutKind.Sequential)]
public struct SequentialSample
{
    public int Id;
    public double Score;
    public byte Flags;
}

[StructLayout(LayoutKind.Sequential, Pack = 1)]
public struct PackedSample
{
    public byte Header;
    public int Value;
    public short Tail;
}

[StructLayout(LayoutKind.Sequential, Pack = 4)]
public struct PackedFourSample
{
    public byte Marker;
    public int Payload;
    public short Trailer;
}

[StructLayout(LayoutKind.Explicit)]
public struct UnionSample
{
    [FieldOffset(0)] public int IntValue;
    [FieldOffset(0)] public float FloatValue;
    [FieldOffset(0)] public uint UIntValue;
}

[StructLayout(LayoutKind.Explicit)]
public struct ExplicitOverlap
{
    [FieldOffset(0)] public long LongValue;
    [FieldOffset(0)] public double DoubleValue;
    [FieldOffset(8)] public int Extra;
}

[StructLayout(LayoutKind.Sequential)]
public unsafe struct FixedBufferSample
{
    public fixed byte Name[24];
    public int Length;
    public fixed int Slots[8];
}

[StructLayout(LayoutKind.Sequential)]
public struct MarshalledRecord
{
    [MarshalAs(UnmanagedType.I1)] public bool Active;

    [MarshalAs(UnmanagedType.LPStr)] public string? Label;

    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)] public int[]? Channels;

    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 16)] public string FixedText;
}

[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
public struct UnicodeRecord
{
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 12)] public string Name;

    public int Code;
}

public static class LayoutInspection
{
    public static int SizeOfSequential => Marshal.SizeOf<SequentialSample>();

    public static int SizeOfPacked => Marshal.SizeOf<PackedSample>();

    public static int SizeOfPackedFour => Marshal.SizeOf<PackedFourSample>();

    public static int SizeOfUnion => Marshal.SizeOf<UnionSample>();

    public static int SizeOfExplicitOverlap => Marshal.SizeOf<ExplicitOverlap>();

    public static int SizeOfFixedBuffer => Marshal.SizeOf<FixedBufferSample>();

    public static int SizeOfMarshalled => Marshal.SizeOf<MarshalledRecord>();

    public static int OffsetOfSequentialScore => (int)Marshal.OffsetOf<SequentialSample>(nameof(SequentialSample.Score));

    public static int OffsetOfSequentialFlags => (int)Marshal.OffsetOf<SequentialSample>(nameof(SequentialSample.Flags));

    public static int OffsetOfPackedValue => (int)Marshal.OffsetOf<PackedSample>(nameof(PackedSample.Value));

    public static int OffsetOfUnionFloat => (int)Marshal.OffsetOf<UnionSample>(nameof(UnionSample.FloatValue));

    public static int OffsetOfFixedLength => (int)Marshal.OffsetOf<FixedBufferSample>(nameof(FixedBufferSample.Length));

    public static unsafe int SizeOfSequentialUnsafe => sizeof(SequentialSample);

    public static unsafe int SizeOfPackedUnsafe => sizeof(PackedSample);

    public static unsafe int SizeOfUnionUnsafe => sizeof(UnionSample);

    public static unsafe int SizeOfFixedBufferUnsafe => sizeof(FixedBufferSample);

    public static int UnionIntBits(float value)
    {
        var union = new UnionSample { FloatValue = value };
        return union.IntValue;
    }

    public static float UnionFloatBits(int value)
    {
        var union = new UnionSample { IntValue = value };
        return union.FloatValue;
    }

    public static unsafe void FillFixedName(FixedBufferSample* sample, ReadOnlySpan<byte> source)
    {
        var count = Math.Min(source.Length, 24);
        for (var i = 0; i < count; i++)
        {
            sample->Name[i] = source[i];
        }

        sample->Length = count;
    }

    public static unsafe ReadOnlySpan<byte> ViewFixedName(FixedBufferSample* sample)
    {
        return new ReadOnlySpan<byte>(sample->Name, sample->Length);
    }

    public static unsafe void FillSlots(FixedBufferSample* sample, ReadOnlySpan<int> values)
    {
        var count = Math.Min(values.Length, 8);
        for (var i = 0; i < count; i++)
        {
            sample->Slots[i] = values[i];
        }
    }
}
