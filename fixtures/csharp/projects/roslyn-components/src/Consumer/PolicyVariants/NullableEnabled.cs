#nullable enable

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: nullable enable context. Nullable warnings are active; the
// dereference below is guarded, and the ! operator suppresses the warning
// at the call site.
public sealed class NullableEnabled
{
    public string? MaybeName { get; set; }

    public int NameLength()
    {
        if (MaybeName is null)
        {
            return 0;
        }

        return MaybeName.Length;
    }

    public string RequireName(string? input) => input!;

    // Flow attribute demonstration: [NotNullWhen] influences null-state analysis.
    public bool TryGetName([System.Diagnostics.CodeAnalysis.NotNullWhen(true)] out string? name)
    {
        name = MaybeName;
        return name is not null;
    }
}
