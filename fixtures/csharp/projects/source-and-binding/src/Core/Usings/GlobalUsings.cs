global using System;
global using System.Collections.Generic;
global using static System.Math;
global using ProjectIntMap = System.Collections.Generic.Dictionary<int, string>;
global using SourceBinding.Core.Namespaces.Open;

namespace SourceBinding.Core.Usings;

public static class GlobalUsingSurface
{
    // Binds via explicit global using plus SDK implicit usings (Core has ImplicitUsings enable).
    public static List<int> BuildViaImplicit() => new List<int> { 1, 2, 3 };

    public static ProjectIntMap BuildViaAlias() => new ProjectIntMap { [7] = "seven" };

    public static double ViaStaticImport() => Abs(-4.5);

    // Collision via Using item customization is shown in NoImplicit project.
}
