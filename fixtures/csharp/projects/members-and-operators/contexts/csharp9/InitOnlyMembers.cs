namespace Catalog.CSharp9
{
    public sealed class InitOnlyMembers
    {
        public int Count { get; init; }

        public string Label { get; init; } = "stock";

        public int this[int index]
        {
            get => Count + index;
            init => Count = value - index;
        }
    }

    public static class InitOnlyFactory
    {
        public static InitOnlyMembers Create()
        {
            return new InitOnlyMembers
            {
                Count = 3,
                Label = "crate",
                [2] = 5,
            };
        }
    }
}
