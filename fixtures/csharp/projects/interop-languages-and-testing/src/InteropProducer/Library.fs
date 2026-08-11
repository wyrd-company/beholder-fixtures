namespace Acme.InteropProducer

module Catalog =
    let catalogLabel = "catalog"
    let formatLabel (value: int) = sprintf "item:%d" value
    let applyTransform (f: System.Func<int, int>) (value: int) = f.Invoke(value)

type Widget(name: string, count: int) =
    member _.Name = name
    member _.Count = count
    member _.Item with get (index: int) = sprintf "%s-%d" name index
    member _.Describe([<System.Runtime.InteropServices.Optional; System.Runtime.InteropServices.DefaultParameterValue(null: obj)>] noteObj: obj) =
        match noteObj with
        | null -> sprintf "widget:%s:default" name
        | :? string as s -> sprintf "widget:%s:%s" name s
        | _ -> sprintf "widget:%s:default" name
    member _.DescribeString([<System.Runtime.InteropServices.Optional; System.Runtime.InteropServices.DefaultParameterValue(null: string)>] note: string) =
        if isNull note then sprintf "widget:%s:default" name else sprintf "widget:%s:%s" name note
    static member Create(name: string, [<System.Runtime.InteropServices.Optional; System.Runtime.InteropServices.DefaultParameterValue(0)>] count: int) = Widget(name, count)
    static member DefaultWidget = Widget("default", 0)

type Container(capacity: int) =
    member _.Capacity = capacity
    member _.Item
        with get (index: int) = index * capacity
        and set (index: int) (value: int) = ()
    static member Empty = Container(0)

type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float
    | Point

module Functional =
    let increment (x: int) = x + 1
    let asFunc = System.Func<int, int>(increment)
    let compose (f: System.Func<int, int>) (g: System.Func<int, int>) (x: int) = f.Invoke(g.Invoke(x))
