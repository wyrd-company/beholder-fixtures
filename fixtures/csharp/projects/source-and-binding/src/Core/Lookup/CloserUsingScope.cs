using DemoA;

namespace SourceBinding.Core.Lookup.Closer
{
    // Compilation-unit scope imports DemoA. With no closer using directive,
    // the unqualified simple name Widget binds to DemoA.Widget.
    public static class OuterUsingScope
    {
        public static string ViaOuter() => Widget.Describe(); // DemoA.Widget => "A"
    }

    namespace Inner
    {
        using DemoB;

        // A closer namespace-scoped using directive imports DemoB. Name resolution
        // stops at this nearer scope, so the unqualified Widget binds to DemoB.Widget
        // and the outer compilation-unit using DemoA is never consulted. The closer
        // using scope demonstrably wins over the farther one.
        public static class InnerUsingScope
        {
            public static string ViaInner() => Widget.Describe(); // DemoB.Widget => "B"
        }
    }
}
