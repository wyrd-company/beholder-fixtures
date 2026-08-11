using System.Text.Json.Serialization;

namespace Acme.Deployment.Trimming;

[JsonSerializable(typeof(TrimSample))]
[JsonSerializable(typeof(List<TrimSample>))]
public partial class WorkshopJsonContext : JsonSerializerContext
{
}
