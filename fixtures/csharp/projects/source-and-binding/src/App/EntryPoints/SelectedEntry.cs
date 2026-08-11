using SourceBinding.Core.Lexical;
using SourceBinding.Core.Namespaces.Open;
using SourceBinding.Library;

namespace SourceBinding.App.Entry;

public sealed class SelectedEntry
{
    // Selected via StartupObject in App.csproj.
    public static int Main(string[] args)
    {
        _ = args.Length;
        _ = LexicalIdentity.EscapedIdentifiers();
        _ = ContributionA.Describe();
        _ = LibrarySurface.Describe();
        return 0;
    }
}
