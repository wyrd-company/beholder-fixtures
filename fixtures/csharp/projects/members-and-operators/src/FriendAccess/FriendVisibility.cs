using Catalog.Core.Accessibility;

namespace Catalog.FriendAccess;

public static class FriendVisibility
{
    internal static void TouchInternal(InternalCatalogEntry entry, AccessModifiers target)
    {
        entry.InternalOnlyValue = 5;
        entry.Touch(target);
        target.InternalMethod();
    }

    internal static void DemonstrateEffectiveAccessibility(AccessModifiers target)
    {
        FriendDerivedAccess derived = new();
        derived.UseProtectedInternalUnion();
        target.InternalMethod();
    }
}
