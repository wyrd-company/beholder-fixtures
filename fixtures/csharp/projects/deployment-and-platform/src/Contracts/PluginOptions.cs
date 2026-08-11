namespace Acme.Deployment.Contracts;

public class PluginOptions
{
    public string DisplayName { get; set; } = "default";
    public int MaxItems { get; set; } = 10;
    public bool EnableLogging { get; set; }
}
