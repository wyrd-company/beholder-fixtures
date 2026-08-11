namespace Catalog.CSharp11
{
    public readonly struct CheckedMeasure
    {
        public CheckedMeasure(int value) => Value = value;

        public int Value { get; }

        public static CheckedMeasure operator +(CheckedMeasure left, CheckedMeasure right) =>
            new CheckedMeasure(left.Value + right.Value);

        public static CheckedMeasure operator checked +(CheckedMeasure left, CheckedMeasure right) =>
            new CheckedMeasure(checked(left.Value + right.Value));

        public static CheckedMeasure operator -(CheckedMeasure left, CheckedMeasure right) =>
            new CheckedMeasure(left.Value - right.Value);

        public static CheckedMeasure operator checked -(CheckedMeasure left, CheckedMeasure right) =>
            new CheckedMeasure(checked(left.Value - right.Value));
    }

    public static class CheckedOperatorExercise
    {
        public static int SumChecked(CheckedMeasure left, CheckedMeasure right) =>
            checked(left + right).Value;
    }
}
