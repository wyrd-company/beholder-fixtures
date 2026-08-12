using System;

namespace SourceBinding.Core.Nested
{
    // Nested type identity and same-named namespace scenario.
    public sealed class ContainerHost
    {
        public sealed class Nested
        {
            public static string Describe() => "ContainerHost.Nested";
        }
    }
}

// Same-named namespace/nested-type contrast is split across assemblies:
// Core provides SourceBinding.Core.Nested.ContainerHost.Nested via nested type (above),
// Extensions provides the same qualified name via namespace path
// (see src/Extensions/NestedContainerHost/NestedViaNamespace.cs).

namespace SourceBinding.Core.Nested
{
    public class Outer<TOuter>
    {
        public TOuter OuterValue { get; set; } = default!;

        public class Inner<TInner>
        {
            public TOuter OuterCaptured { get; set; } = default!;
            public TInner InnerValue { get; set; } = default!;

            public string Describe() => $"{typeof(TOuter).Name}+{typeof(TInner).Name}";
        }

        // Generic arity independence: Outer has 1 parameter, Inner has 1, combined arity 2.
        public Inner<int> CreateInner(int inner) => new Inner<int> { OuterCaptured = OuterValue, InnerValue = inner };
    }

    public class GenericArityDemo
    {
        // Different arities with same simple name (via generic overload).
        public class Pair<T> { }
        public class Pair<T, U> { }

        public static string DescribeArity()
        {
            var one = new Pair<int>();
            var two = new Pair<int, string>();
            // Metadata naming uses backtick, but source identity is arity-based.
            return $"{one.GetType().Name}/{two.GetType().Name}";
        }
    }

    public static class NestedReflection
    {
        public static Type OpenOuter() => typeof(Outer<>);
        public static Type ClosedOuter() => typeof(Outer<int>);
        public static Type ClosedInner() => typeof(Outer<int>.Inner<string>);

        public static string DescribeInaccessible()
        {
            var nested = typeof(Outer<int>.Inner<string>);
            return nested.FullName ?? "unknown";
        }
    }

    // Inaccessible container: private nested type is not accessible outside OuterWithPrivate.
    public class OuterWithPrivate
    {
        private sealed class PrivateInner
        {
            public static string Describe() => "private inner";
        }

        public static string ViaReflection()
        {
            var type = typeof(PrivateInner);
            return type.Name;
        }
    }

    // Effective exposure: public nested type inside private container has effective private accessibility.
    public class EffectiveExposureHost
    {
        private sealed class HiddenContainer
        {
            public sealed class VisibleInner
            {
                public static string Describe() => "visible via hidden";
            }
        }

        public static Type GetExposedType() => typeof(HiddenContainer.VisibleInner);
    }
}
