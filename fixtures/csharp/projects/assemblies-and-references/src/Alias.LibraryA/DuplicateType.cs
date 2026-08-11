namespace Acme.Aliased;

public sealed class DuplicateType
{
    public string Source => "Alias.LibraryA";
    public string Describe() => "DuplicateType from LibraryA";
    public int Value => 1;
}
