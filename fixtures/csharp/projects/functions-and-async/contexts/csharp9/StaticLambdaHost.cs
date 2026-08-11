using System;
using System.Collections.Generic;

namespace Catalog.FunctionsAndAsync.CSharp9
{
    public static class StaticLambdaHost
    {
        public static Func<int, int> StaticLambda() => static x => x * 3;

        public static Func<int, int> StaticAnonymousMethod() => static delegate (int x) { return x + 1; };

        public static int InvokeStaticLocal(int value)
        {
            return Triple(value);

            static int Triple(int x) => x * 3;
        }

        public static async IAsyncEnumerable<int> AsyncStream(int count)
        {
            for (int i = 0; i < count; i++)
            {
                await System.Threading.Tasks.Task.Delay(1);
                yield return i;
            }
        }
    }
}
