from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            "suite_native._native_impl",
            sources=["suite_native/_native_impl.c"],
        ),
        Extension(
            "suite_native._native_impl_abi3",
            sources=["suite_native/_native_impl_abi3.c"],
            py_limited_api=True,
            define_macros=[("Py_LIMITED_API", "0x030A0000")],
        ),
    ]
)
