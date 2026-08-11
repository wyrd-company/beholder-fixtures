from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            "suite_native._native_impl",
            sources=["suite_native/_native_impl.c"],
        ),
    ]
)
