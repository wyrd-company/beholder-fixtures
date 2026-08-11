using Acme.Friends;

namespace Acme.Friends.StrangerLayer;

public sealed class StrangerConsumer
{
    public string ConsumePublicOnly()
    {
        // Non-friend: only public types are accessible. InternalInventory is not visible here.
        var catalog = new PublicCatalog();
        var facade = new PublicFacade();
        return $"{catalog.Name}:{facade.Label}";
    }

    // The following would fail if uncommented, proving friend boundary:
    // private InternalInventory _blocked = new InternalInventory();
}
