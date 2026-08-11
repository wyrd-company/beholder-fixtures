using Catalog.Core.Accessibility;

namespace Catalog.ExternalAccess;

public sealed class ExternalDerivedAccess : AccessModifiers
{
    public void UseProtectedInternalUnion() => ProtectedInternalMethod();
}
