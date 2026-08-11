using Catalog.Core.Fields;

namespace Catalog.ConstantsConsumer;

public static class ConstantReader
{
    public static int ReadBakedConstants()
    {
        return SharedLimits.DefaultCapacity + FieldContracts.TableWidth;
    }
}
