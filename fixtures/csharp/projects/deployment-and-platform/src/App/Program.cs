using Acme.Deployment.App;
using Acme.Deployment.Contracts;
using Acme.Deployment.Platform;
using Acme.Deployment.Trimming;

Console.WriteLine("DeploymentAndPlatform fixture");

Console.WriteLine($"Platform via guarded caller: {GuardedCallers.CallWithRecognizedGuard()}");
Console.WriteLine($"Platform with guard attribute: {GuardedCallers.CallWithGuardAttribute()}");
Console.WriteLine($"Platform conditioned: {PlatformConditionedOperations.DescribePlatform()}");
Console.WriteLine($"RID asset: {RuntimeIdentifierAssets.CurrentRidAsset()}");
Console.WriteLine($"RID publish: {RuntimeIdentifierAssets.DescribePublishPlatform()}");

Console.WriteLine($"Assembly location: {SingleFileAwareness.DescribeAssemblyLocation()}");
Console.WriteLine($"Base directory: {SingleFileAwareness.DescribeBaseDirectory()}");
Console.WriteLine($"Feature switch: {FeatureSwitches.DescribeSwitch()}");
Console.WriteLine($"AOT safe serialize: {AotCompatibility.SerializeTrimSafe(new TrimSample { Name = "demo" })}");

var sample = new TrimSample { Name = "harbor" };
Console.WriteLine($"Reflection nameof access: {ReflectionLinkage.AccessMemberByNameof(sample)}");
Console.WriteLine($"Nameof vs raw: {ReflectionLinkage.DescribeNameofVersusRaw()}");
Console.WriteLine($"Missing resolve: {ReflectionLinkage.TryResolveMissing(out _)}");

var config = new Dictionary<string, string>
{
    [nameof(PluginOptions.DisplayName)] = "Harbor Workshop",
    [nameof(PluginOptions.MaxItems)] = "42",
};

var bound = ConfigurationBinding.BindWithNameof(config);
Console.WriteLine($"Bound config: {bound.DisplayName}/{bound.MaxItems}");

Console.WriteLine($"Is plugin compile-referenced: {PluginLoadContext.IsPluginReferencedAtCompileTime()}");
Console.WriteLine($"Referenced assemblies: {string.Join(", ", PluginLoadContext.ReferencedAssemblyNames())}");

if (args.Length > 0)
{
    var pluginPath = args[0];
    var asm = PluginLoadContext.LoadPluginAssembly(pluginPath);
    foreach (var plugin in ReflectionLinkage.DiscoverPlugins(asm))
    {
        Console.WriteLine($"Plugin {plugin.Name}: {plugin.Execute("cargo")}");
    }
}
