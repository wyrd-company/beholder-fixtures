using System.Linq.Expressions;

namespace ExpressionsFlow.Core;

public static class ExpressionTrees
{
    // Delegate versus Expression tree conversion from equivalent lambda
    public static Func<int, int> AsDelegate() => x => x + 1;

    public static Expression<Func<int, int>> AsExpression() => x => x + 1;

    // Captured variable
    public static Expression<Func<int, int>> Capture(int factor)
    {
        return x => x * factor;
    }

    // Quoted nested lambda (lambda inside expression tree)
    public static Expression<Func<int, Func<int, int>>> QuotedNested()
    {
        return x => (int y) => x + y;
    }

    // Inspection
    public static string Inspect(Expression<Func<int, int>> expr)
    {
        return expr.Body.NodeType.ToString();
    }

    // Compile and invoke
    public static int CompileAndRun(Expression<Func<int, int>> expr, int arg)
    {
        var fn = expr.Compile();
        return fn(arg);
    }

    // IQueryable contrast: provider interpretation versus delegate semantics
    public static int QueryableCount()
    {
        IQueryable<int> source = new[] { 1, 2, 3 }.AsQueryable();
        Expression<Func<int, bool>> predicate = x => x > 1;
        // Provider builds expression tree from predicate; Count with predicate uses filtered enumeration
        return source.Where(predicate).Count();
    }

    public static int EnumerableCount()
    {
        IEnumerable<int> source = new[] { 1, 2, 3 };
        Func<int, bool> predicate = x => x > 1;
        return source.Where(predicate).Count();
    }

    public static string ExpressionVsDelegateIdentity()
    {
        Expression<Func<int, int>> expr = x => x + 1;
        Func<int, int> del = x => x + 1;
        return $"{expr.NodeType}:{del(5)}";
    }

    public static Expression<Func<int, int>> AddExpression(int constant) => x => x + constant;

    public static BinaryExpression BodyAsBinary(Expression<Func<int, int>> expr) => (BinaryExpression)expr.Body;

    public static int ExecuteTree(int input, int addend)
    {
        var expr = AddExpression(addend);
        return CompileAndRun(expr, input);
    }

    // Unsupported statement, async, dynamic, optional/named/ref, conditional-access, pattern, tuple
    // and newer constructs as diagnostics are illustrated as comments:
    //   Expression<Func<int,int>> bad = x => { return x; }; // CS0832 statement body not convertible
    //   Expression<Func<Task<int>>> asyncBad = async () => 1; // CS1989 async not convertible
    //   Expression<Func<dynamic,int>> dyn = x => x; // dynamic not supported
    //   Expression<Func<int,int>> opt = (int x = 5) => x; // optional parameter not convertible
    //   Expression<Func<string?,int?>> cond = s => s?.Length; // conditional-access not convertible in expression tree
    //   Expression<Func<object,string>> pat = o => o is string s ? s : ""; // pattern may be version-dependent
    //   Expression<Func<(int,int),int>> tup = t => t.Item1; // tuple element access is supported but construction may lag
    // Those shapes are not present as live code.
}
