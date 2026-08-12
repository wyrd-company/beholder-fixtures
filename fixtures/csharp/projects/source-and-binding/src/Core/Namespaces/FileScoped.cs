using SourceBinding.Core.Namespaces.BlockScoped;

namespace SourceBinding.Core.Namespaces.FileScoped;

using System.Collections.Generic;

public sealed class FileScopedContainer
{
    public static string Describe() => BlockContainer.Describe() + "+file-scoped";

    public List<int> UseAfterScope() => new List<int> { 1, 2 };
}

public sealed class FileScopedHelper
{
    public static string Describe() => "file scoped helper";
}
