namespace ExpressionsFlow.CheckedShared;

public static class CheckedSharedOps
{
    // Project-wide checked: this addition is checked because CheckForOverflowUnderflow=true.
    public static int CheckedAdd(int a, int b) => a + b;

    public static int CheckedConvert(long value) => (int)value;

    // Local unchecked override within project-wide checked context.
    public static int UncheckedOverride(int a, int b) => unchecked(a + b);

    public static int UncheckedConvert(long value) => unchecked((int)value);
}
