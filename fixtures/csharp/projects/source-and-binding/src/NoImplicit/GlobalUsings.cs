global using System;
global using System.Collections.Generic;
global using System.Linq;
global using static System.Math;
global using NoIntMap = System.Collections.Generic.Dictionary<int, string>;

namespace SourceBinding.NoImplicit;

public static class ExplicitGlobalUsings
{
    // Binds only through explicit global using; SDK implicit usings are disabled in this project.
    public static List<string> BuildList() => new List<string> { "explicit" };

    public static NoIntMap BuildMap() => new NoIntMap { [1] = "one" };

    public static double ViaStatic() => Abs(-2.0);

    public static int ViaLinq(IEnumerable<int> values) => values.Sum();
}
