namespace Acme.Aliased;

public sealed class DuplicateType
{
    public string Source => "Alias.LibraryB";
    public string Describe() => "DuplicateType from LibraryB";
    public int Value => 2;
}
