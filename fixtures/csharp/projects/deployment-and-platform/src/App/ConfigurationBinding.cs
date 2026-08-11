using System.Diagnostics.CodeAnalysis;
using Acme.Deployment.Contracts;

namespace Acme.Deployment.App;

public static class ConfigurationBinding
{
    // Simple configuration binding — mimics Options pattern without external package.
    // Binds string dictionary values to PluginOptions via reflection.
    [RequiresUnreferencedCode("Binds configuration via reflection.")]
    public static PluginOptions BindFromDictionary(IReadOnlyDictionary<string, string> data)
    {
        var options = new PluginOptions();
        var type = typeof(PluginOptions);

        foreach (var prop in type.GetProperties())
        {
            if (!data.TryGetValue(prop.Name, out var raw))
            {
                continue;
            }

            if (prop.PropertyType == typeof(string))
            {
                prop.SetValue(options, raw);
            }
            else if (prop.PropertyType == typeof(int) && int.TryParse(raw, out var parsed))
            {
                prop.SetValue(options, parsed);
            }
            else if (prop.PropertyType == typeof(bool) && bool.TryParse(raw, out var flag))
            {
                prop.SetValue(options, flag);
            }
        }

        return options;
    }

    [RequiresUnreferencedCode("Binds configuration via reflection.")]
    public static T BindGeneric<T>(IReadOnlyDictionary<string, string> data) where T : new()
    {
        var instance = new T();
        var type = typeof(T);

        foreach (var prop in type.GetProperties())
        {
            if (!data.TryGetValue(prop.Name, out var raw))
            {
                continue;
            }

            if (prop.PropertyType == typeof(string))
            {
                prop.SetValue(instance, raw);
            }
            else if (prop.PropertyType == typeof(int) && int.TryParse(raw, out var parsed))
            {
                prop.SetValue(instance, parsed);
            }
        }

        return instance;
    }

    // Trim-aware variant — caller declares what members are preserved.
    public static PluginOptions BindTrimAware(
        IReadOnlyDictionary<string, string> data,
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicProperties)] Type optionsType)
    {
        var options = (PluginOptions)Activator.CreateInstance(optionsType)!;
        foreach (var prop in optionsType.GetProperties())
        {
            if (data.TryGetValue(prop.Name, out var raw) && prop.PropertyType == typeof(string))
            {
                prop.SetValue(options, raw);
            }
        }

        return options;
    }

    // nameof-based binding — compiler-checked property name.
    public static PluginOptions BindWithNameof(IReadOnlyDictionary<string, string> data)
    {
        var options = new PluginOptions();
        if (data.TryGetValue(nameof(PluginOptions.DisplayName), out var name))
        {
            options.DisplayName = name;
        }

        if (data.TryGetValue(nameof(PluginOptions.MaxItems), out var max) && int.TryParse(max, out var n))
        {
            options.MaxItems = n;
        }

        return options;
    }
}
