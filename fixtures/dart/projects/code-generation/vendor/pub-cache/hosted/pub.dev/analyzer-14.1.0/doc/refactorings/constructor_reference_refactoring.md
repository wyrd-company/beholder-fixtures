# ConstructorName and ConstructorReference Refactoring

This document proposes a constructor-focused AST cleanup:

- replace `ConstructorName` with a new constructor-reference node
- replace `ConstructorReference` with a new `ConstructorTearOff` node
- use `ConstructorSelector` wherever the AST currently models an optional `.` + constructor-name pair as separate `period` and `name` fields

The goal is to make the resolved AST more semantically honest without turning the entire tree into a semantic IR.

This is a compatibility-preserving migration, not an in-place breaking change.
Existing public nodes and properties remain available during the deprecation
period as compatibility projections. New nodes and new properties are the
primary generated model; old APIs are deprecated, non-generated projections
that preserve the old observable behavior.

Migration model reference: [Compatibility-Preserving AST Refactoring #63685](https://github.com/dart-lang/sdk/issues/63685).

For the resulting public API, see [API Shape After Refactoring](#api-shape-after-refactoring).

## 1. Problem Statement

The analyzer currently uses `ConstructorName` for a node that does not represent a declaration name.

It is the syntactic construct that identifies a constructor in source:

- a `NamedType`
- optionally followed by a named-constructor selector

Examples:

- `C`
- `C.named`
- `prefix.C<int>`
- `prefix.C<int>.named`

The name `ConstructorName` is misleading because it sounds like the declaration-side name of a constructor, similar to `ConstructorDeclaration.name` or `PrimaryConstructorName`.

At the same time, the existing `ConstructorReference` node is an expression node for constructor tear-offs such as `List.filled`. That name is also misleading, because the specification talks about constructor tear-offs, and because the node currently reuses `ConstructorName`, whose selector is optional.

There is also a deeper type-side mismatch: `ConstructorName.type` reuses `NamedType`, but in this context `NamedType.type` is intentionally `null`. That is a sign that the AST is reusing a node whose semantics do not quite fit the role; section 5 explains this problem in more detail.

This creates three design problems:

1. the shared non-expression node has a declaration-sounding name
2. the expression node has a reference-sounding name but models a construct whose selector should be required
3. the reused type child has a `TypeAnnotation` API that does not match this context

## 2. Current State

Today the public AST has:

```text
abstract final class ConstructorName
    implements AstNode, ConstructorReferenceNode {
  NamedType get type;
  Token? get period;
  SimpleIdentifier? get name;
}

abstract final class ConstructorReference
    implements Expression, CommentReferableExpression {
  ConstructorName get constructorName;
}
```

This shape has a few issues.

### `ConstructorName` is not a name

`ConstructorName` is not “the name of a constructor”. It includes the type and the optional named-constructor suffix. It is much closer to “a source-level reference to a constructor”.

### `SimpleIdentifier` is not the right node for the constructor name

The `name` child of `ConstructorName` is currently modeled as:

```text
SimpleIdentifier? get name;
```

This is also a semantic mismatch.

`SimpleIdentifier` is an expression node. In ordinary expression contexts, it can denote a value and can have a static type. But the constructor-name suffix in `C.named` is not evaluated as an expression. It is part of a constructor reference, not a value-producing expression in its own right.

So the current API reuses an expression node in a non-expression role. The reuse is structurally convenient, but semantically misleading, which is another reason to prefer `ConstructorSelector` for the optional `.` + name suffix.

### `NamedType` is not the right child node

The left side of a constructor reference looks type-like, but it is not quite an ordinary `TypeAnnotation`.

For example, in `A.named`:

- the `A` part is not an expression
- it is not a normal type annotation in source
- it does not always denote one `DartType`
- constructor lookup starts from a type-defining declaration plus optional type arguments

Today this mismatch appears in the API as a special case: `NamedType.type` is documented to be `null` when the `NamedType` is part of a constructor reference.

That special case is a design smell. It suggests that constructor references should use a dedicated node rather than reusing `NamedType`.

### `period` and `name` encode one concept as two fields

For valid source code, these fields represent one syntactic unit:

```text
.identifier
```

The analyzer already has a node for exactly this concept:

```text
abstract final class ConstructorSelector implements AstNode {
  Token get period;
  SimpleIdentifier get name;
}
```

To truly solve the problem of reusing an expression node in a non-expression role (as discussed above), `ConstructorSelector` should ideally use a `Token` for the name instead of a `SimpleIdentifier`. This keeps the node purely structural.

However, `ConstructorName`, `RedirectingConstructorInvocation`, and `SuperConstructorInvocation` still split this structure into two nullable fields.

### `ConstructorReference` does not encode tear-off structure precisely

The constructor tear-offs specification requires a selector for tear-offs:

- named tear-off: `C.name`
- unnamed tear-off: `C.new`

Plain `C` is a type literal, not a constructor tear-off.

So the expression node for constructor tear-offs should require a selector. The current `ConstructorReference` cannot express this directly because its child node allows the selector to be absent.

## 3. Design Principles

This refactoring follows these principles.

### Resolved AST should model high-value semantic distinctions

Most analyzer clients consume resolved AST. If an important semantic distinction is not modeled, clients must reconstruct it themselves.

Constructor tear-offs are a good example: they have dedicated language-spec semantics, they are not just ordinary property accesses, and clients often care about them directly.

### Shared source structure should still be reusable

Constructor invocations, redirects, `super` constructor calls, and constructor tear-offs all refer to constructors using closely related source structure.

The AST should share that structure where doing so remains semantically honest.

### Optional `.` + name should be modeled as `ConstructorSelector`

If the grammar concept is “optional constructor selector”, then the AST should have one nullable node for it, not two separate nullable fields. That gives the API clearer invariants and keeps recovery behavior localized to one node shape.

## 4. Proposed Design

### 4.1 Introduce `ConstructorTypeReference`

The left side of a constructor reference should be modeled by a new node instead of reusing `NamedType`.

```text
abstract final class ConstructorTypeReference implements AstNode {
  Element? get element;
  ImportPrefixReference? get importPrefix;
  Token get name;
  TypeArgumentList? get typeArguments;
}
```

This node is intentionally not a `TypeAnnotation`.

It represents the declaration-oriented, type-shaped syntax that appears in constructor references and constructor tear-offs, without claiming to denote a normal resolved `DartType`.

This eventually removes the need for the current
`NamedType.type == null if part of ConstructorReference` exception. During the
compatibility window, old `NamedType`-based APIs remain available as deprecated
projections and must keep that exception.

### 4.2 Introduce a replacement for `ConstructorName`

The current `ConstructorName` node should be replaced by a new primary
constructor-reference node. The preferred long-term name is
`ConstructorReference`, but during the compatibility window that name is still
occupied by the existing expression node, so the staged API needs a
non-conflicting name such as `ConstructorReference2`.

```text
abstract final class ConstructorReference2
    implements AstNode, ConstructorReferenceNode {
  ConstructorTypeReference get typeReference;
  ConstructorSelector? get selector;
}
```

The preferred final name matches what the node actually represents: a
source-level reference to a constructor, used by multiple enclosing constructs.
The old `ConstructorName` API remains available as a deprecated projection.

Examples:

- `C()` uses a constructor reference with `selector == null`
- `C.named()` uses a constructor reference with `selector.name2 == named`
- `factory A() = B.named;` uses a constructor reference

### 4.3 Introduce `ConstructorTearOff`

The current expression node named `ConstructorReference` should be replaced by
a new primary `ConstructorTearOff` node.

```text
abstract final class ConstructorTearOff
    implements Expression, CommentReferableExpression, ConstructorReferenceNode {
  ConstructorTypeReference get typeReference;
  ConstructorSelector get selector;
}
```

This encodes the language construct directly: it is an expression, it is specifically a constructor tear-off, and it always has a selector.

Examples:

- `C.named`
- `C.new`
- `prefix.C<int>.named`

This node should not allow `selector` to be absent, because `C` is not a constructor tear-off.

The old `ConstructorReference` expression API remains available as a deprecated
projection during the compatibility window.

### 4.4 Use `ConstructorSelector` for optional named-constructor suffixes

The following nodes should use `ConstructorSelector?` instead of separate nullable `period` and `name`/`constructorName` fields:

- the new constructor-reference node
- `RedirectingConstructorInvocation`
- `SuperConstructorInvocation`

Illustratively:

```text
abstract final class RedirectingConstructorInvocation
    implements ConstructorInitializer, ConstructorReferenceNode {
  Token get thisKeyword;
  ConstructorSelector? get constructorSelector;
  ArgumentList get argumentList;
}

abstract final class SuperConstructorInvocation
    implements ConstructorInitializer, ConstructorReferenceNode {
  Token get superKeyword;
  ConstructorSelector? get constructorSelector;
  ArgumentList get argumentList;
}
```

This matches what `EnumConstantArguments` already does today.

The old split fields remain available as deprecated projections. For example,
`RedirectingConstructorInvocation.period` and
`RedirectingConstructorInvocation.constructorName` are projected from
`constructorSelector`, and must keep the same observable behavior as before.

### 4.5 Keep the tear-off node structurally separate

`ConstructorTearOff` should not be modeled as:

```text
ConstructorReference get constructor;
```

with an invariant that `constructor.selector != null`.

That design would preserve code reuse, but it weakens the public API by making an important language invariant indirect.

The expression node should expose the required selector directly.

### 4.6 Keep `ConstructorElement` on the whole constructor reference

The resolved `ConstructorElement` should remain attached to the whole constructor-reference construct, not to its individual pieces.

That means:

- `ConstructorReference` should continue to implement `ConstructorReferenceNode`
- `ConstructorTearOff` should also implement `ConstructorReferenceNode`
- `ConstructorSelector` should remain purely structural
- `ConstructorTypeReference` should keep only type-side resolution, not constructor-side resolution

This matches the semantic structure of the language:

- `ConstructorTypeReference` identifies the referenced type declaration
- `ConstructorSelector` identifies the optional named-constructor suffix
- the resolved `ConstructorElement` belongs to the combination of those parts

So the constructor element should stay on the node that represents the complete constructor reference, just as it does today.

When instantiation is involved, the element should be the instantiated constructor element, not always the raw declaration element.

That means:

- if explicit type arguments are present, `element` should reflect them
- if type arguments are inferred, `element` should reflect the inferred instantiation
- clients that need the declaration element can use `element.baseElement`

This keeps the API aligned with the rest of analyzer resolution, where resolved elements usually represent the selected and instantiated member rather than only the raw declaration.

## 5. Why `ConstructorTypeReference` Should Not Be `NamedType`

It is tempting to keep reusing `NamedType` for the left side of constructor references, because the syntax is visually similar. However, doing so keeps the current semantic mismatch in the tree.

Problems with reusing `NamedType`:

- `NamedType` is a `TypeAnnotation`, but constructor references are not ordinary type annotations
- `NamedType.type` must stay `null` in this context, which makes the node behave differently from almost every other `NamedType`
- clients have to remember a special exception instead of trusting the node kind

`ConstructorTypeReference` is better because:

- it matches the actual role of the syntax
- it keeps constructor-specific semantics local to constructor-specific nodes
- it lets `NamedType` remain a real type-annotation node

This is a small increase in node count, but it removes a persistent source of API confusion.

## 6. Why `ConstructorReference` Is Better Than `ConstructorTarget`

`ConstructorTarget` is a possible alternative name for the current `ConstructorName`, but it is less precise.

Problems with `ConstructorTarget`:

- “target” suggests an invocation target or receiver target
- it does not naturally describe redirecting constructors or declaration-side references
- it is vague about whether the node is syntactic or semantic

`ConstructorReference` is better because:

- it describes what the node does in source
- it is neutral between invocation and non-invocation uses
- it matches existing analyzer terminology such as `CommentReference`

Once the old expression node is removed after its deprecation window, the
`ConstructorReference` name becomes available for the non-expression node that
actually deserves it.

## 7. Why Constructor Tear-Offs Need Their Own Node

The remaining question is whether constructor tear-offs should have their own expression node at all. They should, because the specification defines them as a distinct expression form with their own resolution and typing rules, and resolved-AST clients often care about them directly.

This is a narrower claim than a general move toward semantic member-reference nodes. Plain method tear-offs such as `obj.method` can still be represented by source-shaped nodes like `PropertyAccess` and `PrefixedIdentifier`; this document only regularizes the constructor-specific part of the AST.

## 8. Error Recovery

One motivation for split `period` and `name` fields is error recovery, because the parser may see a dangling `.`.

This refactoring should preserve recovery quality by using a `ConstructorSelector` with a synthetic `Token` when the name is missing, rather than by allowing `period != null` with no selector node.

This is already the general analyzer recovery style in other areas of the AST: syntactic structure is usually preserved by synthetic tokens/nodes rather than by dropping half of a construct.

## 9. Discussion: Why This Is Different From `ImportPrefixReference`

This refactoring should not be read as a general rule that every AST node must have a tightly typed semantic element.

`ImportPrefixReference` is a useful counterexample. In syntax such as `foo.MyClass`, the `foo.` part occupies a dedicated syntactic position for an import prefix. In valid code, that position can only denote an import prefix. However, in invalid code, the token `foo` may resolve to some other declaration, and analyzer clients may still want to navigate to that declaration.

That makes a loose `Element? get element` contract on `ImportPrefixReference` defensible:

- the node still accurately models the syntactic role
- the element can preserve navigation information even when the construct is invalid
- using `null` for every non-prefix resolution would lose information that some clients care about

The `ConstructorName` / `NamedType` problem is different. There, the mismatch exists even in valid code: a `NamedType` inside a constructor reference is not acting like an ordinary type annotation, which is why its `type` must be specially documented as `null` today.

So `ImportPrefixReference` and `ConstructorTypeReference` respond to different design pressures. The former keeps a loose `Element?` for navigation in invalid code; the latter avoids reusing a type-annotation node whose API does not fit this role even in valid code.

<a name="api-shape-after-refactoring"></a>
## 10. API Shape After Refactoring

Illustratively, the main constructor-related nodes should have this shape in
the compatibility window. Names shown as `*2` or otherwise suffixed are staging
names used when the preferred long-term name is still occupied by an existing
public API. After the deprecation window, the preferred names can be collapsed.

```text
abstract final class ConstructorReferenceNode implements AstNode {
  /// The resolved constructor element.
  ///
  /// When the enclosing type is instantiated explicitly or by inference, this
  /// is the instantiated constructor element. Clients that need the
  /// declaration element can use `element.baseElement`.
  ConstructorElement? get element;
}

// New node (replaces NamedType in this role)
abstract final class ConstructorTypeReference implements AstNode {
  Element? get element;
  ImportPrefixReference? get importPrefix;
  Token get name;
  TypeArgumentList? get typeArguments;
}

abstract final class ConstructorSelector implements AstNode {
  Token get period;

  // New primary API.
  Token get name2;

  // Legacy projection over `name2`.
  @Deprecated('Use name2 instead')
  SimpleIdentifier get name;
}

// New primary node. Preferred long-term name: ConstructorReference.
// During compatibility it needs a non-conflicting name because the old
// expression node named ConstructorReference still exists.
abstract final class ConstructorReference2
    implements AstNode, ConstructorReferenceNode {
  ConstructorTypeReference get typeReference;
  ConstructorSelector? get selector;
}

// Replacement for the old expression node named ConstructorReference.
abstract final class ConstructorTearOff
    implements Expression, CommentReferableExpression, ConstructorReferenceNode {
  ConstructorTypeReference get typeReference;
  ConstructorSelector get selector;
}

// Legacy node. Projection over ConstructorReference2.
@Deprecated('Use ConstructorReference2 instead')
abstract final class ConstructorName
    implements AstNode, ConstructorReferenceNode {
  NamedType get type;

  Token? get period;

  SimpleIdentifier? get name;
}

// Legacy expression node. Projection over ConstructorTearOff.
@Deprecated('Use ConstructorTearOff instead')
abstract final class ConstructorReference
    implements Expression, CommentReferableExpression, ConstructorReferenceNode {
  ConstructorName get constructorName;
}

abstract final class InstanceCreationExpression implements Expression {
  // New primary API.
  ConstructorReference2 get constructorReference;

  // Legacy projection.
  @Deprecated('Use constructorReference instead')
  ConstructorName get constructorName;

  ArgumentList get argumentList;
}

abstract final class ConstructorDeclaration implements AstNode {
  // ...
  // New primary API during compatibility.
  ConstructorReference2? get redirectedConstructor2;

  // Legacy projection.
  @Deprecated('Use redirectedConstructor2 instead')
  ConstructorName? get redirectedConstructor;
}

abstract final class RedirectingConstructorInvocation
    implements ConstructorInitializer, ConstructorReferenceNode {
  Token get thisKeyword;

  // New primary API.
  ConstructorSelector? get constructorSelector;

  // Legacy projections.
  @Deprecated('Use constructorSelector instead')
  Token? get period;

  @Deprecated('Use constructorSelector instead')
  SimpleIdentifier? get constructorName;

  ArgumentList get argumentList;
}

abstract final class SuperConstructorInvocation
    implements ConstructorInitializer, ConstructorReferenceNode {
  Token get superKeyword;

  // New primary API.
  ConstructorSelector? get constructorSelector;

  // Legacy projections.
  @Deprecated('Use constructorSelector instead')
  Token? get period;

  @Deprecated('Use constructorSelector instead')
  SimpleIdentifier? get constructorName;

  ArgumentList get argumentList;
}
```

The same new constructor-reference node would be reused by:

- `InstanceCreationExpression`
- `ConstructorDeclaration.redirectedConstructor2`

And `ConstructorSelector?` would be reused by:

- `RedirectingConstructorInvocation`
- `SuperConstructorInvocation`
- existing `EnumConstantArguments`

Legacy APIs must preserve their old behavior exactly. For example,
`ConstructorName.type` remains a `NamedType` projection during the deprecation
period, including old resolution behavior such as `NamedType.type == null` in
constructor-reference position. Similarly, projected `SimpleIdentifier`
children keep their old parent, traversal, child-entity, element, and static
type behavior.

This design eventually removes the need for `NamedType` documentation and
resolver logic to special-case constructor references, but only after the
legacy projection APIs are removed.

## 11. Migration Strategy

This is a compatibility-preserving staged migration. The preferred final API
can be reached only after the normal analyzer deprecation window. Until then,
new APIs are primary and generated, while old APIs are deprecated projections
implemented by hand where necessary.

### Steps

1. Add generated support for the new tree-view APIs described in
   `compatibility_preserving_ast_refactoring.md`.
2. Introduce `ConstructorTypeReference` API/impl and migrate the new primary
   constructor-related nodes to use it instead of `NamedType`.
3. Add the new primary replacement for `ConstructorName` using a non-conflicting
   staged name, such as `ConstructorReference2`.
4. Add the new primary `ConstructorTearOff` node as the replacement for the old
   expression node named `ConstructorReference`.
5. Add new primary properties for renamed or retyped properties, for example:
   - `InstanceCreationExpression.constructorReference`
   - `ConstructorDeclaration.redirectedConstructor2`
6. Replace `period` + `name` pairs in the new model with
   `ConstructorSelector?` where they represent an optional named-constructor
   suffix.
7. Keep the old APIs as projections. Deprecate legacy nodes themselves, but do
   not separately deprecate every property of an already deprecated node.
   Deprecate legacy properties on nodes that otherwise remain current:
   - deprecated legacy node `ConstructorName`
   - deprecated legacy node `ConstructorReference`
   - `ConstructorSelector.name`
   - `InstanceCreationExpression.constructorName`
   - `ConstructorDeclaration.redirectedConstructor`
   - `RedirectingConstructorInvocation.period` and `constructorName`
   - `SuperConstructorInvocation.period` and `constructorName`
8. Ensure every legacy projection preserves the old observable behavior exactly:
   old getters, old `AstVisitor` traversal, old `visitChildren`, old `parent`,
   old child entities, old element/static-type values, and old summary
   round-tripping.
9. Serialize the new real tree as the primary format. If a legacy projection
   cannot be reconstructed exactly from the new tree, serialize the additional
   legacy semantic state needed to preserve compatibility.
10. Update parser, resolver, summary reader/writer, printers, visitors, and
    tests to use the new primary model internally.
11. Migrate analyzer, analysis_server, linter, and SDK-owned tools to the new
    APIs.
12. Add compatibility notes to the analyzer changelog and migration guidance.
13. After the deprecation window, remove legacy projection APIs, collapse staged
    names to their preferred final names where appropriate, and remove
    `NamedType` special cases related to constructor references from
    documentation and resolver code.

## 12. Non-Goals

This document does not propose:

- a full semantic AST redesign
- replacing `PropertyAccess` / `PrefixedIdentifier` with semantic member reference nodes
- introducing a unified node for all function, method, and constructor tear-offs

Those are related design questions, but they are broader than this refactoring.
