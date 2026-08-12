using System;

namespace GenericsAndDispatch.CSharp8
{
    public static class NullableConstraints
    {
        public static string NeedNullableClass<T>(T? value) where T : class => value == null ? "null" : value.ToString()!;

        public static T? Wrap<T>(T? value) where T : class => value;

        public static string Describe<T>(T? value) where T : class => value == null ? "empty" : value.ToString()!;

        public static void Run()
        {
            string a = NeedNullableClass<string>("text");
            string b = NeedNullableClass<string>(null);
            string? wrapped = Wrap<string>("hi");
            string described = Describe<string>(wrapped);
            _ = a; _ = b; _ = described;
        }
    }

    public class NullableHost<T> where T : class
    {
        public T? Value { get; set; }
        public string Read() => Value == null ? "null" : Value.ToString()!;
    }
}
