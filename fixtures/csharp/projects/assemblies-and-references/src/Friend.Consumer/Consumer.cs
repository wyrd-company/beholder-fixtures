using Acme.Friends;

namespace Acme.Friends.ConsumerLayer;

public sealed class FriendConsumer
{
    public string ConsumeInternal()
    {
        // Friend access: internal type and members are visible because of InternalsVisibleTo.
        var inventory = new InternalInventory { StockLevel = 99 };
        IInternalContract worker = new InternalWorker();
        return $"{inventory.Sku}:{inventory.StockLevel}:{worker.Execute()}:{PublicFacade.InternalLabel}";
    }

    public string ConsumeProtectedInternal()
    {
        var inv = new InternalInventory();
        // Access via derived type scenario: protected internal on internal type is visible to friend.
        return inv.StockLevel.ToString();
    }
}
