using Catalog.Core.Accessibility;

namespace Catalog.ExternalAccess;

public static class ExternalVisibility
{
    public static void TouchPublicOnly(AccessModifiers target)
    {
        target.PublicMethod();
        _ = target.PublicProperty;
    }

    public static void DemonstrateEffectiveAccessibility(AccessModifiers target)
    {
        ExternalDerivedAccess derived = new();
        derived.UseProtectedInternalUnion();
        target.PublicMethod();
    }
}
