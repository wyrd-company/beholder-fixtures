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
        // ProtectedInternalNote is declared protected internal; friend access reaches it
        // directly (no inheritance needed) because InternalsVisibleTo extends the internal
        // half of protected-internal accessibility to this assembly.
        return inv.ProtectedInternalNote;
    }
}
