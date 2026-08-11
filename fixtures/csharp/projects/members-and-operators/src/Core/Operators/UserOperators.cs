namespace Catalog.Core.Operators;

public readonly struct Measure : IComparable<Measure>, IEquatable<Measure>
{
    public Measure(int value) => Value = value;

    public int Value { get; }

    public static Measure operator +(Measure left, Measure right) =>
        new(left.Value + right.Value);

    public static Measure operator -(Measure left, Measure right) =>
        new(left.Value - right.Value);

    public static Measure operator *(Measure left, int factor) =>
        new(left.Value * factor);

    public static bool operator ==(Measure left, Measure right) =>
        left.Value == right.Value;

    public static bool operator !=(Measure left, Measure right) =>
        left.Value != right.Value;

    public static bool operator <(Measure left, Measure right) =>
        left.Value < right.Value;

    public static bool operator >(Measure left, Measure right) =>
        left.Value > right.Value;

    public static bool operator <=(Measure left, Measure right) =>
        left.Value <= right.Value;

    public static bool operator >=(Measure left, Measure right) =>
        left.Value >= right.Value;

    public static bool operator true(Measure value) => value.Value > 0;

    public static bool operator false(Measure value) => value.Value <= 0;

    public static implicit operator Measure(int value) => new(value);

    public static explicit operator int(Measure value) => value.Value;

    public int CompareTo(Measure other) => Value.CompareTo(other.Value);

    public bool Equals(Measure other) => Value == other.Value;

    public override bool Equals(object? obj) => obj is Measure other && Equals(other);

    public override int GetHashCode() => Value.GetHashCode();
}

public readonly struct SignedMeasure
{
    public SignedMeasure(int value) => Value = value;

    public int Value { get; }

    public static SignedMeasure operator +(SignedMeasure left, SignedMeasure right) =>
        new(left.Value + right.Value);

    public static SignedMeasure operator checked +(SignedMeasure left, SignedMeasure right) =>
        new(checked(left.Value + right.Value));
}

public static class NullableLiftedOperators
{
    public static Measure? AddNullable(Measure? left, Measure? right) => left + right;
}

public interface IAdditive<T> where T : IAdditive<T>
{
    static abstract T operator +(T left, T right);
}

public readonly struct Vector2 : IAdditive<Vector2>
{
    public Vector2(int x, int y)
    {
        X = x;
        Y = y;
    }

    public int X { get; }
    public int Y { get; }

    public static Vector2 operator +(Vector2 left, Vector2 right) =>
        new(left.X + right.X, left.Y + right.Y);

    static Vector2 IAdditive<Vector2>.operator +(Vector2 left, Vector2 right) =>
        left + right;
}

public static class OperatorExercise
{
    public static bool Evaluate(Measure left, Measure right)
    {
        Measure sum = left + right;
        Measure diff = left - right;
        Measure scaled = left * 2;
        Measure converted = 4;
        int raw = (int)converted;
        Measure? lifted = (Measure?)left + (Measure?)right;
        return sum > diff && IsTruthy(scaled) && IsTruthy(converted) && lifted is not null && raw > 0;
    }

    public static bool IsTruthy(Measure value) => value ? true : false;
}
