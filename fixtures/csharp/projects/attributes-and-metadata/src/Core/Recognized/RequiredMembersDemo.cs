using System.Diagnostics.CodeAnalysis;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// Declares required members alongside a constructor that satisfies them and
/// is marked <see cref="SetsRequiredMembersAttribute"/>, so callers may use
/// either that constructor or an object initializer.
/// </summary>
public class RequiredMembersShowcase
{
    public required string Name { get; init; }

    public required int Id { get; init; }

    [SetsRequiredMembers]
    public RequiredMembersShowcase(string name, int id)
    {
        Name = name;
        Id = id;
    }

    public RequiredMembersShowcase()
    {
    }
}

public static class RequiredMembersUsage
{
    public static RequiredMembersShowcase ViaConstructor() => new("via-constructor", 1);

    public static RequiredMembersShowcase ViaObjectInitializer() => new() { Name = "via-initializer", Id = 2 };
}
