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
    // Constant overflow is compile-time error when checked, diagnsotic:
    //   const int bad = checked(int.MaxValue + 1); // CS0220 overflow
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

    // Dependency body retains compiled semantics even when called from checked context.
    // The callee's body was compiled as written (unchecked by default unless checked block).
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
