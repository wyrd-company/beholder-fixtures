namespace SourceBinding.CSharp10;

public static class EnhancedLineDemo
{
#line 100 "Mapped10.cs"
    public static int Mapped() => 100;
#line default

#line hidden
    public static int Hidden() => 1;
#line default

    // Enhanced #line with range (C#10) – demonstrates column mapping.
#line (10,1)-(11,1) 10 "Enhanced10.cs"
    public static int Enhanced() => 10;
#line default
}
