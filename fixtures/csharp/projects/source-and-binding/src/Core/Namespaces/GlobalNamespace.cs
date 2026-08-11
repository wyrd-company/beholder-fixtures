namespace SourceBinding.Core.Namespaces
{
    public sealed class GlobalNamespaceType
    {
        public static string Describe() => "global namespace type";
    }
}

namespace GlobalDemo
{
    public sealed class Consumer
    {
        public static string ViaGlobal()
        {
            return global::SourceBinding.Core.Namespaces.GlobalNamespaceType.Describe();
        }
    }
}
