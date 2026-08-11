// CS-CAN-013: consumes the linked SharedModel.cs with Core-specific symbol CORE_COMPILATION.
using Catalog.Packages.Shared;

namespace Catalog.Packages;

public sealed class LinkedConsumer
{
    public SharedModel Model { get; } = new();
    public string Tag => SharedModel.CompilationTag;
    public string Describe() => Model.Describe();
}
