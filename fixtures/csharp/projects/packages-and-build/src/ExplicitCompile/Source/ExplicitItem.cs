// CS-CAN-012: explicit inclusion with EnableDefaultCompileItems=false — only files with explicit Compile Include are compiled.
namespace Catalog.Packages.Explicit;

public sealed class ExplicitItem
{
    public string Note => "Explicitly included when defaults disabled";
}
