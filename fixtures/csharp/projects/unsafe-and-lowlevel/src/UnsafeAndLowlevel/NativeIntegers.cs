namespace Workshop.LowLevel;

public static class NativeIntegers
{
    // 64-bit process constants using native-sized integers.
    public const nint DefaultCapacity = 32;
    public const nuint MaxBufferSize = 4096;

    public const nint MinOffset = -16;
    public const nuint Sentinel = 0xFFFF_FFFF;

    public static nint Add(nint left, nint right) => left + right;

    public static nuint Add(nuint left, nuint right) => left + right;

    public static nint Multiply(nint value, int factor) => value * factor;

    public static nuint Scale(nuint value, nuint factor) => value * factor;

    public static nint Negate(nint value) => -value;

    public static bool IsEven(nint value) => (value & 1) == 0;

    public static nint FromInt32(int value) => (nint)value;

    public static nuint FromUInt32(uint value) => (nuint)value;

    public static int ToInt32(nint value) => (int)value;

    public static uint ToUInt32(nuint value) => (uint)value;

    public static nint FromIntPtr(IntPtr pointer) => (nint)pointer;

    public static IntPtr ToIntPtr(nint value) => (IntPtr)value;

    public static nuint FromUIntPtr(UIntPtr pointer) => (nuint)pointer;

    public static UIntPtr ToUIntPtr(nuint value) => (UIntPtr)value;

    public static nint FromNuint(nuint value) => checked((nint)value);

    public static nuint FromNint(nint value) => checked((nuint)value);

    public static unsafe int SizeOfNint => sizeof(nint);

    public static unsafe int SizeOfNuint => sizeof(nuint);

    // Demonstrates native-sized integer identity alongside IntPtr/UIntPtr.
    public static string Describe(nint value) => $"nint:{value}";

    public static string Describe(nuint value) => $"nuint:{value}";

    public static string DescribeOverload(object _)
        => "object";

    public static nint CheckedAdd(nint left, nint right) => checked(left + right);

    public static nuint CheckedAdd(nuint left, nuint right) => checked(left + right);

    public static nint UncheckedAdd(nint left, nint right) => unchecked(left + right);

    public static nuint UncheckedAdd(nuint left, nuint right) => unchecked(left + right);

    public static bool TryCheckedAdd(nint left, nint right, out nint result)
    {
        try
        {
            result = checked(left + right);
            return true;
        }
        catch (OverflowException)
        {
            result = 0;
            return false;
        }
    }

    public static nint WrapOnOverflow(nint left, nint right) => unchecked(left + right);

    public static nint CheckedIncrement(nint value) => checked(value + 1);

    public static nuint CheckedIncrement(nuint value) => checked(value + 1);

    public static nint Subtract(nint left, nint right) => left - right;

    public static nuint Subtract(nuint left, nuint right) => left - right;

    public static nint Divide(nint left, nint right) => left / right;

    public static nint Remainder(nint left, nint right) => left % right;

    public static int Compare(nint left, nint right) => left.CompareTo(right);

    public static int Compare(nuint left, nuint right) => left.CompareTo(right);

    public static nint MaxValue => nint.MaxValue;

    public static nint MinValue => nint.MinValue;

    public static nuint NuintMaxValue => nuint.MaxValue;

    public static nuint NuintMinValue => nuint.MinValue;
}
