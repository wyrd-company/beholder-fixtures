namespace Bakery.TypesAndValues.Core.NullableValue;

// CS-CAN-023: nullable value types and lifted operations — Nullable<T> arithmetic,
// comparisons, conversions, coalescing, bool? logic, pattern matching, GetValueOrDefault, boxing.

public static class NullableValueTypes
{
    public static int? LiftedAdd(int? left, int? right) => left + right;

    public static int? LiftedMultiply(int? left, int? right) => left * right;

    public static bool LiftedEquals(int? left, int? right) => left == right;

    public static bool LiftedEqualsIsLifted(int? left, int? right)
    {
        bool result = left == right;
#pragma warning disable CS0183
        return result is bool;
#pragma warning restore CS0183
    }

    public static bool LiftedComparisonReturnsBool(int? left, int? right) => left > right;

    public static bool? LiftedToNullVsBoolean(int? left, int? right)
    {
        int? sum = left + right;
        bool cmp = left > right;
        int? leftNull = null;
        bool sumIsNullWhenLeftNull = (leftNull + 5) is null;
        int? nullLeft = null;
        int? nullRight = null;
        bool cmpIsFalseWhenBothNull = (nullLeft == nullRight) == true;
        _ = sum;
        _ = cmp;
        return sumIsNullWhenLeftNull && cmpIsFalseWhenBothNull ? true : null;
    }

    public static int Coalesce(int? value, int fallback) => value ?? fallback;

    public static int CoalesceAssign(ref int? target, int fallback) => target ??= fallback;

    public static bool? BoolLogic(bool? left, bool? right)
    {
        bool? and = left & right;
        bool? or = left | right;
        bool? xor = left ^ right;
        _ = and;
        _ = or;
        return xor;
    }

    public static bool PatternMatch(int? value) => value is int n && n > 3;

    public static bool PatternMatchNull(int? value) => value is null;

    public static int GetValueOrDefault(int? value) => value.GetValueOrDefault();

    public static int GetValueOrDefaultWithFallback(int? value, int fallback) =>
        value.GetValueOrDefault(fallback);

    public static bool HasValue(int? value) => value.HasValue;

    public static int ValueOrThrow(int? value) => value!.Value;

    public static object? BoxNullable(int? value) => value;

    public static bool BoxNullIsNullReference()
    {
        int? nothing = null;
        object? boxed = nothing;
        return boxed is null;
    }

    public static bool BoxNonNullIsBoxedInt()
    {
        int? value = 5;
        object? boxed = value;
        return boxed is int i && i == 5;
    }

    public static int? ConvertFromNonNullable(int value) => value;

    public static int? ConvertFromNullableToNonNullable(int? value) => value;

    public static T? GenericLifted<T>(T? value) where T : struct => value;

    public static T? GenericLiftedClass<T>(T? value) where T : class => value;

    public static T? GenericLiftedUnconstrained<T>(T? value) => value;

    public static T? LiftedViaGeneric<T>(T left, T right) where T : struct
    {
        // Demonstrate generic T? changing meaning by struct constraint vs class.
        T? a = left;
        T? b = right;
        _ = a;
        _ = b;
        return null;
    }

    public static T? LiftedViaGenericClass<T>(T left, T right) where T : class
    {
        T? a = left;
        T? b = right;
        _ = a;
        _ = b;
        return null;
    }

    public static bool? NullableBoolLogicTruthTable()
    {
        bool? t = true;
        bool? f = false;
        bool? n = null;
        bool? r1 = t & n;
        bool? r2 = f & n;
        bool? r3 = t | n;
        bool? r4 = f | n;
        return r1 is null && r2 == false && r3 == true && r4 is null;
    }

    public static void DemonstrateNestedNullableIsInvalid()
    {
        // int?? is invalid source; comment shows the diagnostic that would occur.
        // var nested = (int??)5; // error CS0453: The type 'int?' must be a non-nullable value type
        _ = typeof(int?);
    }

    public static int? LiftedUnaryMinus(int? value) => -value;

    public static int? LiftedIncrement(int? value) => value + 1;
}
