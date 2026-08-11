// CS-CAN-106: resources and strongly typed accessors.
using System.Globalization;
using System.Resources;
using Catalog.Packages.Properties;

namespace Catalog.Packages;

public sealed class ResourcesConsumer
{
    // Typed accessor generated from Strings.resx via ResXFileCodeGenerator (Strings.Designer.cs)
    public string TypedGreeting => Strings.Greeting;
    public string TypedFarewell => Strings.Farewell;

    // Raw string-key lookup via ResourceManager
    public string RawLookup(string key, CultureInfo? culture = null)
    {
        var manager = new ResourceManager("Catalog.Packages.Resources.Strings", typeof(Strings).Assembly);
        return manager.GetString(key, culture ?? CultureInfo.InvariantCulture) ?? $"(missing:{key})";
    }

    public string LocalizedGreeting => Strings.ResourceManager.GetString("Greeting", new CultureInfo("fr")) ?? Strings.Greeting;

    // Satellite assembly is produced for fr; manifest name is Catalog.Packages.Resources.Strings.
    public string ManifestName => "Catalog.Packages.Resources.Strings";

    public bool TryGetSatelliteAssembly(CultureInfo culture, out System.Reflection.Assembly? satellite)
    {
        try
        {
            satellite = typeof(Strings).Assembly.GetSatelliteAssembly(culture);
            return true;
        }
        catch
        {
            satellite = null;
            return false;
        }
    }
}
