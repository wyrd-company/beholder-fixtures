using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

namespace Workshop.LowLevel;

public unsafe struct FixedPacket
{
    public const int DataLength = 32;
    public const int ValueLength = 8;

    public fixed byte Data[32];
    public fixed int Values[8];
    public int Tag;
    public int Count;
}

public unsafe struct FixedHeader
{
    public fixed char Name[24];
    public int Version;
}

public static unsafe class PointerOperations
{
    public static int* Offset(int* pointer, int offset) => pointer + offset;

    public static int Distance(int* first, int* second) => (int)(second - first);

    public static void Increment(ref int* pointer) => pointer++;

    public static void Decrement(ref int* pointer) => pointer--;

    public static void* ToVoidPointer(int* pointer) => pointer;

    public static IntPtr ToIntPtr(int* pointer) => (IntPtr)pointer;

    public static int* FromIntPtr(IntPtr pointer) => (int*)pointer;

    public static byte* ToBytePointer(void* pointer) => (byte*)pointer;

    public static int Read(int* pointer) => *pointer;

    public static void Write(int* pointer, int value) => *pointer = value;

    public static int ReadAt(int* pointer, int index) => pointer[index];

    public static void WriteAt(int* pointer, int index, int value) => pointer[index] = value;

    public static int Sum(Span<int> span)
    {
        fixed (int* p = span)
        {
            var total = 0;
            for (var i = 0; i < span.Length; i++)
            {
                total += p[i];
            }

            return total;
        }
    }

    public static void Scale(int* pointer, int length, int factor)
    {
        for (var i = 0; i < length; i++)
        {
            pointer[i] *= factor;
        }
    }

    public static int AddressOf(ref int value)
    {
        fixed (int* p = &value)
        {
            return *p;
        }
    }

    public static void Fill(FixedPacket* packet, byte value)
    {
        for (var i = 0; i < FixedPacket.DataLength; i++)
        {
            packet->Data[i] = value;
        }
    }

    public static void FillValues(FixedPacket* packet, int value)
    {
        for (var i = 0; i < FixedPacket.ValueLength; i++)
        {
            packet->Values[i] = value;
        }
    }

    public static int ReadFixedData(FixedPacket* packet, int index) => packet->Data[index];

    public static int ReadFixedValue(FixedPacket* packet, int index) => packet->Values[index];

    public static int SumPinnedArray(int[] array)
    {
        fixed (int* p = array)
        {
            var total = 0;
            for (var i = 0; i < array.Length; i++)
            {
                total += p[i];
            }

            return total;
        }
    }

    public static int SumStackAllocInt(int length)
    {
        var ptr = stackalloc int[length];
        for (var i = 0; i < length; i++)
        {
            ptr[i] = i;
        }

        var total = 0;
        for (var i = 0; i < length; i++)
        {
            total += ptr[i];
        }

        return total;
    }

    public static int SumStackAllocSpan(int length)
    {
        Span<int> span = stackalloc int[length];
        for (var i = 0; i < span.Length; i++)
        {
            span[i] = i * 2;
        }

        var total = 0;
        foreach (var v in span)
        {
            total += v;
        }

        return total;
    }

    public static int SumStackAllocBytes(int length)
    {
        Span<byte> span = stackalloc byte[length];
        span.Fill(0xAB);
        var total = 0;
        foreach (var b in span)
        {
            total += b;
        }

        return total;
    }
}

public static unsafe class FunctionPointers
{
    public static int Add(int left, int right) => left + right;

    public static int Multiply(int left, int right) => left * right;

    [UnmanagedCallersOnly(CallConvs = new[] { typeof(CallConvCdecl) })]
    public static int UnmanagedAdd(int left, int right) => left + right;

    [UnmanagedCallersOnly]
    public static int UnmanagedMultiply(int left, int right) => left * right;

    public static int InvokeManaged(delegate* managed<int, int, int> function, int left, int right)
        => function(left, right);

    public static int InvokeUnmanaged(delegate* unmanaged[Cdecl]<int, int, int> function, int left, int right)
        => function(left, right);

    public static int InvokeUnmanagedStdcall(delegate* unmanaged[Stdcall]<int, int, int> function, int left, int right)
        => function(left, right);

    public static delegate* managed<int, int, int> ManagedAddPointer => &Add;

    public static delegate* managed<int, int, int> ManagedMultiplyPointer => &Multiply;

    public static delegate* unmanaged[Cdecl]<int, int, int> UnmanagedAddPointer => &UnmanagedAdd;

    public static int CallManagedAdd(int left, int right)
    {
        delegate* managed<int, int, int> ptr = &Add;
        return ptr(left, right);
    }

    public static int CallUnmanagedAdd(int left, int right)
    {
        delegate* unmanaged[Cdecl]<int, int, int> ptr = &UnmanagedAdd;
        return ptr(left, right);
    }

    public static void ConsumeBlittableCallback(delegate* unmanaged[Cdecl]<int, int> callback, int value)
    {
        callback(value);
    }
}
