using System.Runtime.CompilerServices;

[assembly: InternalsVisibleTo("Friend.Consumer, PublicKey=002400000480000094000000060200000024000052534131000400000100010059261979CD569C01DED6C906BF000811E8C46FFCE39F26F26B2965CB8F6A0FE93B9B7A8477E58D3E2DA0E6BE42747CBEF8FFA17E07E0A9EDFF703C3899ADC26CA38BD3FC5CC3E6A740B82EF66E2A106BF413EA33C48E14E974141FE0B6242A400BEDC83EBEFE9789D079A7884CD3FFA764ABCC5FACD472A02D6D669DCE7AA0CD")]

namespace Acme.Friends;

public sealed class PublicFacade
{
    public string Label => "Friend.Producer public facade";
    internal static string InternalLabel => "secret-internal";
}

internal class InternalInventory
{
    public string Sku { get; init; } = "INV-001";
    internal int StockLevel { get; set; } = 42;
    internal string InternalNote => "internal note";

    // protected internal: InternalsVisibleTo extends the internal half of this
    // accessibility to the friend assembly, so a friend reaches it directly, with no
    // derived type required.
    protected internal string ProtectedInternalNote => "protected internal note";
}

internal interface IInternalContract
{
    string Execute();
}

internal sealed class InternalWorker : IInternalContract
{
    public string Execute() => "internal worker executed";
}
