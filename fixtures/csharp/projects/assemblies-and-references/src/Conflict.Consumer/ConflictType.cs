namespace Acme.Conflict;

// This source type collides with Conflict.External.Acme.Conflict.CollidingType.
// The source definition wins; the compiler emits CS0436 warning:
// "The type CollidingType in Conflict.Consumer/ConflictType.cs conflicts with the imported type ..."
public sealed class CollidingType
{
    public string Source => "Conflict.Consumer local source (wins)";
    public string Describe() => "CollidingType from local source wins over reference with CS0436";
}

public sealed class ConflictConsumer
{
    public string ConsumeLocalWins()
    {
        // Unqualified reference resolves to the local source type, not the imported reference type.
        var local = new CollidingType();
        return local.Describe() + " -> " + local.Source;
    }

    public string ConsumeReferenceViaAliasWorkaround()
    {
        // If we needed the reference type, we would disambiguate via extern alias (see Alias.Consumer).
        // This file demonstrates the warning form; the alias form is covered by Alias.Consumer.
        return new CollidingType().Source;
    }
}
