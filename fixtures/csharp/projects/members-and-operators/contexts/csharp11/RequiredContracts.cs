using System.Diagnostics.CodeAnalysis;

namespace Catalog.CSharp11
{
    public class RequiredBase
    {
        public required int Seed { get; set; }

        public required string Label { get; init; }
    }

    public sealed class RequiredDerived : RequiredBase
    {
        public required int Offset { get; set; }
    }

    public sealed record RequiredRecord
    {
        public required int Count { get; init; }

        public required string Name { get; init; }
    }

    public sealed class RequiredWithDefault
    {
        public required int Value { get; set; } = 1;
    }

    public class RequiredLabelBase
    {
        public string Caption { get; set; } = string.Empty;
    }

    public sealed class RequiredHiddenMember : RequiredLabelBase
    {
        public new required string Caption { get; set; }
    }

    public sealed class RequiredConstructorHost
    {
        public required int Count { get; init; }

        public required string Name { get; init; }

        [SetsRequiredMembers]
        public RequiredConstructorHost(int count, string name)
        {
            Count = count;
            Name = name;
        }
    }

    public static class RequiredFactory
    {
        public static RequiredRecord Create()
        {
            return new RequiredRecord
            {
                Count = 2,
                Name = "crate",
            };
        }

        public static RequiredRecord Copy(RequiredRecord source) => source with { Count = 4 };
    }

    public sealed class GenericRequiredHost<T> where T : new()
    {
        public required T Payload { get; set; }

        public T CreateDefault() => new T();
    }
}
