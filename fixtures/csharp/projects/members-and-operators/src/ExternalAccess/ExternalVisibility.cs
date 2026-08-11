using Catalog.Core.Accessibility;

namespace Catalog.ExternalAccess;

public static class ExternalVisibility
{
    public static void TouchPublicOnly(AccessModifiers target)
    {
        target.PublicMethod();
        _ = target.PublicProperty;
    }
}
