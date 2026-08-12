using Bakery.TypesAndValues.Nullable.AnnotatedApi;
using Bakery.TypesAndValues.Nullable.ObliviousLegacy;

namespace Bakery.TypesAndValues.Nullable.Consumer;

public static class AnonymousCrossAssembly
{
    public static void ObserveDistinctIdentities()
    {
        var local = new { Name = "a", Count = 1 };
        object annotated = AnnotatedAnonymous.CreateShape();
        object legacy = LegacyAnonymous.CreateShape();

        bool localVsAnnotated = local.GetType() != annotated.GetType();
        bool localVsLegacy = local.GetType() != legacy.GetType();
        bool annotatedVsLegacy = annotated.GetType() != legacy.GetType();

        _ = localVsAnnotated && localVsLegacy && annotatedVsLegacy;
    }

    public static (Type Local, Type Annotated, Type Legacy) GetTypes()
    {
        var local = new { Name = "a", Count = 1 };
        return (local.GetType(), AnnotatedAnonymous.GetShapeType(), LegacyAnonymous.GetShapeType());
    }
}
