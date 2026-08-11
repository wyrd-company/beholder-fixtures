namespace Bakery.TypesAndValues.Core.Arrays;

// CS-CAN-022: arrays and covariance — one-dimensional, rectangular, jagged,
// inferred-bound, explicit-bound, reflection non-zero-bound, covariant conversion
// with store failure, System.Array contrast, nullability, zero length, shape identity.

public static class ArrayShapes
{
    public static int[] CreateOneDimensional() => new int[] { 1, 2, 3 };

    public static int[] CreateInferredBound() => new[] { 4, 5, 6 };

    public static int[] CreateExplicitBound() => new int[3] { 7, 8, 9 };

    public static int[,] CreateRectangular() => new int[2, 3] { { 1, 2, 3 }, { 4, 5, 6 } };

    public static int[][] CreateJagged()
    {
        return new[]
        {
            new[] { 1, 2 },
            new[] { 3, 4, 5 },
        };
    }

    public static int[,,] CreateThreeDimensional() => new int[2, 2, 2];

    public static Array CreateNonZeroBound()
    {
        return Array.CreateInstance(typeof(int), new[] { 3 }, new[] { 1 });
    }

    public static void ExerciseArrayVsSystemArray(int[] array)
    {
        Array asArray = array;
        bool isVector = asArray.GetType().IsArray && asArray.Rank == 1;
        _ = isVector;
        _ = asArray.Length;
        _ = array.Length;
    }

    public static int[] EmptyArray() => Array.Empty<int>();

    public static int[] ZeroLength() => new int[0];

    public static void CovariantConversionAndStoreFailure()
    {
        string[] strings = new[] { "a", "b", "c" };
        object[] objects = strings;
        _ = objects.Length == 3 && objects[0] as string == "a";

        try
        {
            objects[0] = "ok";
            object boxed = 42;
            objects[1] = boxed;
        }
        catch (ArrayTypeMismatchException)
        {
            _ = true;
        }
    }

    public static bool ShapeIdentity()
    {
        int[] vector = new[] { 1, 2 };
        int[,] rect = new int[1, 2];
        Array nonZero = CreateNonZeroBound();
        bool vectorIsVector = vector.GetType() == typeof(int[]);
        bool rectIsRect = rect.GetType() == typeof(int[,]);
        bool nonZeroLowerBound = nonZero.GetLowerBound(0) == 1;
        return vectorIsVector && rectIsRect && nonZeroLowerBound;
    }

    public static void CopyVsViewWithSpan(int[] source)
    {
        Span<int> view = source.AsSpan();
        view[0] = 99;
        bool viewMutates = source[0] == 99;

        int[] copy = source.ToArray();
        copy[0] = 1;
        bool copyIndependent = source[0] != copy[0] || copy.Length == source.Length;
        _ = viewMutates && copyIndependent;
    }

    public static string?[] NullableElementArray() => new string?[] { "a", null, "c" };

    public static int? ElementConversion(int?[] values)
    {
        int total = 0;
        foreach (int? value in values)
        {
            total += value ?? 0;
        }

        return total;
    }

    public static int SumRectangular(int[,] matrix)
    {
        int sum = 0;
        for (int i = 0; i < matrix.GetLength(0); i++)
        {
            for (int j = 0; j < matrix.GetLength(1); j++)
            {
                sum += matrix[i, j];
            }
        }

        return sum;
    }
}
