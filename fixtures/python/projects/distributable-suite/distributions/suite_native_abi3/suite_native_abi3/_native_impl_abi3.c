#define Py_LIMITED_API 0x030A0000
#include <Python.h>

/* Compiled against the CPython stable ABI (Py_LIMITED_API 3.10) so the built
 * wheel carries the abi3 wheel tag and loads on any CPython >= 3.10. */

static PyObject *hello_abi3(PyObject *self, PyObject *args) {
    return PyUnicode_FromString("hello abi3");
}

static PyMethodDef methods[] = {
    {"hello_abi3", hello_abi3, METH_NOARGS, "Return abi3 greeting"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_native_impl_abi3",
    NULL,
    -1,
    methods,
};

PyMODINIT_FUNC PyInit__native_impl_abi3(void) {
    return PyModule_Create(&moduledef);
}
