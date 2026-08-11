extern alias LibraryA;

using Acme.Aliased;

namespace Acme.Aliased.Consumer;

public sealed class AliasedConsumer
{
    public string ConsumeBoth()
    {
        var a = new LibraryA::Acme.Aliased.DuplicateType();
        // Alias.LibraryB.csproj carries no Aliases metadata, so its reference keeps the
        // default "global" alias and DuplicateType resolves unaliased and unambiguously to
        // LibraryB's type: LibraryA's custom-only alias removed it from the global alias
        // set, so there is no duplicate-reference ambiguity to resolve here.
        var b = new DuplicateType();
        return $"{a.Describe()} ({a.Value}) | {b.Describe()} ({b.Value})";
    }

    public string ConsumeViaGlobalAlias()
    {
        // Custom-versus-global contrast: LibraryA is reachable only through its custom
        // "LibraryA" extern alias (above), while LibraryB is reachable through the default
        // "global" reference alias, so this call needs no extern alias declaration at all.
        var viaGlobal = new DuplicateType();
        return viaGlobal.Source;
    }
}
