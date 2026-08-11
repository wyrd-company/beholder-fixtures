namespace SourceBinding.Core.Namespaces.BlockScoped
{
    public sealed class BlockContainer
    {
        public static string Describe() => "block-scoped";
    }

    namespace NestedBlock
    {
        public sealed class NestedItem
        {
            public static string Describe() => "nested block";
        }
    }
}
