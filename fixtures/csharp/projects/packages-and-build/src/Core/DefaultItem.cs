// CS-CAN-012: default-globbed source — included implicitly by SDK glob **/*.cs without explicit Compile Include.
namespace Catalog.Packages;

public sealed class DefaultItem
{
    public string Name => "DefaultGlobbed";
    public int Value => 42;
}
