using Catalog.Core.Accessibility;

namespace Catalog.FriendAccess;

public sealed class FriendDerivedAccess : AccessModifiers
{
    public void UseProtectedInternalUnion() => ProtectedInternalMethod();
}
