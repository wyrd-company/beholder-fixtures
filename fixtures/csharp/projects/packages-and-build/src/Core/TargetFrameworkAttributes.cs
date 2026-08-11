// CS-CAN-014: target-framework attributes are SDK-generated (TargetFrameworkAttribute) and part of the assembly.
// This file surfaces the attribute via reflection.
using System;
using System.Reflection;
using System.Runtime.Versioning;

namespace Catalog.Packages;

public static class FrameworkInfo
{
    public static string? TargetFramework => Assembly.GetExecutingAssembly().GetCustomAttribute<TargetFrameworkAttribute>()?.FrameworkName;
    public static string? InformationalVersion => Assembly.GetExecutingAssembly().GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion;
}
