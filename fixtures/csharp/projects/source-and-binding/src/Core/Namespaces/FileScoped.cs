using SourceBinding.Core.Namespaces.BlockScoped;

namespace SourceBinding.Core.Namespaces.FileScoped;

public sealed class FileScopedContainer
{
    public static string Describe() => BlockContainer.Describe() + "+file-scoped";
}

public sealed class FileScopedHelper
{
    public static string Describe() => "file scoped helper";
}
