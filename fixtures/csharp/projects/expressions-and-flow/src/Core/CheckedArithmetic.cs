using ExpressionsFlow.CheckedShared;

namespace ExpressionsFlow.Core;

public readonly struct CheckedCounter
{
    public int Value { get; }

    public CheckedCounter(int value) => Value = value;

    public static CheckedCounter operator +(CheckedCounter left, CheckedCounter right) =>
        new(left.Value + right.Value);

    public static CheckedCounter operator checked +(CheckedCounter left, CheckedCounter right) =>
        new(checked(left.Value + right.Value));

    public static CheckedCounter operator -(CheckedCounter left, CheckedCounter right) =>
        new(left.Value - right.Value);

    public static CheckedCounter operator checked -(CheckedCounter left, CheckedCounter right) =>
        new(checked(left.Value - right.Value));

    public static CheckedCounter operator *(CheckedCounter left, int factor) =>
        new(left.Value * factor);

    public static CheckedCounter operator checked *(CheckedCounter left, int factor) =>
        new(checked(left.Value * factor));

    public static explicit operator int(CheckedCounter counter) => counter.Value;

    public static explicit operator checked int(CheckedCounter counter) => checked(counter.Value);
}

public static class CheckedArithmetic
{
    // Constant checked and unchecked arithmetic/conversion
    public const int ConstCheckedSum = checked(10 + 20);
    public const int ConstUncheckedWrap = unchecked(int.MaxValue + 1);
    public const int ConstCheckedConversion = checked((int)123L);
    public const int ConstUncheckedConversion = unchecked((int)4294967296L);
    public const int ConstCheckedAdd = checked(100 + 200);
    public const int ConstUncheckedAdd = unchecked(int.MaxValue + 10);

    public static int UseConsts() => ConstCheckedSum + ConstUncheckedWrap + ConstCheckedConversion + ConstUncheckedConversion;

    public static int ConstantCheckedOverflow()
    {
        checked
        {
            int max = int.MaxValue;
            try
            {
                return max + 1;
            }
            catch (OverflowException)
            {
                return -1;
            }
        }
    }

    public static int UncheckedWrap()
    {
        unchecked
        {
            int max = int.MaxValue;
            return max + 1;
        }
    }

    public static int RuntimeChecked(int a, int b)
    {
        checked
        {
            return a + b;
        }
    }

    public static int RuntimeUnchecked(int a, int b)
    {
        unchecked
        {
            return a + b;
        }
    }

    public static int CheckedConversion(long value)
    {
        checked
        {
            return (int)value;
        }
    }

    public static int UncheckedConversion(long value)
    {
        unchecked
        {
            return (int)value;
        }
    }

    // Constant operations exercised live
    public static int CheckedConstOperation() => checked(10 + 20);

    public static int UncheckedConstOperation() => unchecked(int.MaxValue + 1);

    public static int CheckedConstConversionLive() => checked((int)123L);

    public static int UncheckedConstConversionLive() => unchecked((int)4294967296L);

    // Decimal versus floating behavior: decimal overflow always throws; floating wraps to infinity
    public static decimal DecimalChecked(decimal a, decimal b) => checked(a + b);

    public static double FloatingWrap(double a, double b) => a + b;

    // Native-size architecture: nint/nuint range is platform-dependent (64-bit here)
    public static nint NativeAdd(nint a, nint b) => checked(a + b);

    // Local override of project option: checked region inside unchecked project still checks.
    // The Core project has no CheckForOverflowUnderflow, so defaults to unchecked runtime.
    // checked/unchecked blocks demonstrate local override.
    public static int LocalOverrideChecked(int a, int b)
    {
        unchecked
        {
            checked
            {
                return a + b;
            }
        }
    }

    // Dependency body retaining separately compiled semantics: call helper compiled in checked-project
    public static int CallCheckedDependency(int a, int b)
    {
        // CheckedSharedOps.CheckedAdd is compiled with CheckForOverflowUnderflow=true,
        // so it throws on overflow even when caller is unchecked.
        return CheckedSharedOps.CheckedAdd(a, b);
    }

    public static int CallCheckedDependencyViaCheckedContext(int a, int b)
    {
        checked
        {
            return CheckedSharedOps.CheckedAdd(a, b);
        }
    }

    public static int CallUncheckedDependencyFromChecked()
    {
        // CheckedSharedOps.UncheckedOverride is compiled with local unchecked override inside checked project,
        // so it wraps even though its project is checked.
        return CheckedSharedOps.UncheckedOverride(int.MaxValue, 1);
    }

    private static int UncheckedHelper(int a, int b) => unchecked(a + b);

    public static int CallUncheckedHelperChecked(int a, int b)
    {
        checked
        {
            return UncheckedHelper(a, b);
        }
    }

    // Paired checked/unchecked user operators
    public static CheckedCounter AddChecked(CheckedCounter a, CheckedCounter b) => checked(a + b);

    public static CheckedCounter AddUnchecked(CheckedCounter a, CheckedCounter b) => unchecked(a + b);

    public static int OperatorCheckedOverflow()
    {
        try
        {
            var a = new CheckedCounter(int.MaxValue);
            var b = new CheckedCounter(1);
            var _ = checked(a + b);
            return 0;
        }
        catch (OverflowException)
        {
            return -1;
        }
    }

    public static int OperatorUncheckedWrap()
    {
        var a = new CheckedCounter(int.MaxValue);
        var b = new CheckedCounter(1);
        var c = unchecked(a + b);
        return c.Value;
    }
}
