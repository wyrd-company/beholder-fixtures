#nullable disable

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: nullable disabled / oblivious context. Annotations are not
// enforced and dereference warnings are not produced. This contrasts with
// NullableEnabled.cs (enabled) and NullableAnnotationsOnly.cs boundary.
public class NullableDisabled
{
    public string MaybeName { get; set; }

    public int NameLength()
    {
        // No warning here even though MaybeName could be null at runtime:
        // nullable analysis is disabled in this file.
        return MaybeName.Length;
    }
}
