extern alias LibraryA;
extern alias LibraryB;

using LibraryA::Acme.Aliased;
using LibraryB_Aliased = LibraryB::Acme.Aliased;

namespace Acme.Aliased.Consumer;

public sealed class AliasedConsumer
{
    public string ConsumeBoth()
    {
        var a = new LibraryA::Acme.Aliased.DuplicateType();
        var b = new LibraryB::Acme.Aliased.DuplicateType();
        // Reference aliases LibraryA and LibraryB disambiguate the duplicate qualified name.
        return $"{a.Describe()} ({a.Value}) | {b.Describe()} ({b.Value})";
    }

    public string ConsumeViaGlobalAlias()
    {
        // Global alias would be ambiguous without extern alias: the unaliased
        // Acme.Aliased.DuplicateType would produce CS0433 if both references were
        // imported without an alias. Extern alias resolves it.
        var aliasedB = new LibraryB_Aliased.DuplicateType();
        return aliasedB.Source;
    }
}
