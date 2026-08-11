// CS-CAN-124: intentionally omitted from solution but referenced via ProjectReference from Core.
// Project-reference truth vs solution membership: Core references this assembly though the solution does not list it.
namespace Catalog.Packages.OmittedLib;

public sealed class OmittedService
{
    public string Origin => "OmittedLib";
    public string Describe() => "Omitted but referenced";
}
