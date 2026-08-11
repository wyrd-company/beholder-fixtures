/* _native_limited.c — limited-API / stable-ABI extension */
#define Py_LIMITED_API 0x030A0000
#include <Python.h>

static PyObject *limited_hello(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    return PyUnicode_FromString("limited-hello");
}

static PyObject *limited_add(PyObject *self, PyObject *args) {
    long a, b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b)) return NULL;
    return PyLong_FromLong(a + b);
}

static PyMethodDef limited_methods[] = {
    {"hello", limited_hello, METH_NOARGS, "Limited-API hello"},
    {"add", limited_add, METH_VARARGS, "Add two ints via limited API"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef limited_def = {
    PyModuleDef_HEAD_INIT,
    "_native_limited",
    "Limited-API extension (Py_LIMITED_API 0x030A0000) for stable ABI",
    -1,
    limited_methods,
    NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__native_limited(void) {
    return PyModule_Create(&limited_def);
}

/* Notes for reviewers:
 * - Built with -DPy_LIMITED_API=0x030A0000, so only limited-API symbols are available.
 * - Minimum macro version 0x030A0000 corresponds to Python 3.10.
 * - Unavailable APIs (e.g., PyLongObject internals, PyUnicode internal) are not accessible.
 * - Third-party native dependency: none; uses only CPython headers.
 * - Free-threaded incompatibility: stable ABI abi3 extension is incompatible with free-threaded builds that require newer ABI.
 */
