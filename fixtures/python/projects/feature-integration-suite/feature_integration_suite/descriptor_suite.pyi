from typing import Generic, TypeVar, overload, Annotated

T = TypeVar("T")

class ManagedFieldStub(Generic[T]):
    @overload
    def __get__(self, instance: None, owner: type[object]) -> ManagedFieldStub[T]: ...
    @overload
    def __get__(self, instance: object, owner: type[object] | None = ...) -> T: ...
    def __set__(self, instance: object, value: T) -> None: ...
    def __delete__(self, instance: object) -> None: ...

# Intentional drift: stub exports ManagedFieldStub instead of ManagedField and lacks REGISTRY
# Runtime module exports ManagedField and REGISTRY, so checker and runtime diverge.

class IntegrationRecordStub(Generic[T]):
    managed: ManagedFieldStub[int]
    @overload
    def get_value(self, as_str: bool = ...) -> int: ...
    @overload
    def get_value(self, as_str: bool = ...) -> str: ...
    def get_value(self, as_str: bool = ...) -> int | str: ...

# Extra stub-only name
extra_stub_only: int
