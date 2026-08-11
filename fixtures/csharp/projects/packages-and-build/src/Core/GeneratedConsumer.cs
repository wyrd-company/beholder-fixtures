// CS-CAN-014: consumes the pre-compile MSBuild-generated source as a real compilation unit.
using Catalog.Packages;

namespace Catalog.Packages;

public sealed class GeneratedConsumer
{
    public string Value => BuildTimeConstants.GeneratedValue;
    public string Generator => BuildTimeConstants.GeneratorName;
}
