using System;
using System.Runtime.InteropServices;

namespace GenericsAndDispatch.CSharp9
{
    public abstract class DefaultBase
    {
        public abstract T Create<T>();
    }

    public class DefaultDerived : DefaultBase
    {
        public override T Create<T>() where T : default => default!;
    }

    public static class DefaultConstraint
    {
        public static T CreateDefault<T>() where T : struct => default;

        public static T OrDefault<T>(T? fallback) where T : struct => fallback ?? default;

        public static void Fill<T>(Span<T> span, T? value = default) where T : struct
        {
            T actual = value ?? default;
            for (int i = 0; i < span.Length; i++) span[i] = actual;
        }

        public static void Run()
        {
            int i = CreateDefault<int>();
            int j = OrDefault<int>(null);
            Span<int> buffer = stackalloc int[2];
            Fill(buffer);
            var derived = new DefaultDerived();
            int k = derived.Create<int>();
            _ = i; _ = j; _ = buffer[0]; _ = k;
        }
    }

    public class DefaultHost<T> where T : struct
    {
        public T Value { get; set; } = default;
        public T GetOrDefault(T? fallback = default) => fallback ?? default;
    }
}
