using System;
using System.Collections.Generic;

namespace ExpressionsFlow.CSharp12
{
    public static class CollectionExpressions
    {
        public static int[] Array() => [1, 2, 3];

        public static int[] Empty() => [];

        public static List<int> List() => [1, 2, 3];

        public static int SpanLength()
        {
            Span<int> span = [10, 20, 30];
            return span.Length;
        }

        public static int[] Spread(int[] a, int[] b) => [.. a, .. b];

        private static IEnumerable<int> Source()
        {
            yield return 10;
            yield return 20;
        }

        public static int[] WithSpread() => [1, .. Source(), 3];
    }
}
