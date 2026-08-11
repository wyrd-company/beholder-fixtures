/* _native_wrong.c — extension with deliberately wrong init symbol */
#include <Python.h>

static PyObject *wrong_hello(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    return PyUnicode_FromString("wrong-init-hello");
}

static PyMethodDef wrong_methods[] = {
    {"hello", wrong_hello, METH_NOARGS, "hello"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef wrong_def = {
    PyModuleDef_HEAD_INIT,
    "_native_wrong",
    "Extension with wrong init symbol",
    -1,
    wrong_methods,
    NULL, NULL, NULL, NULL
};

/* Intentionally wrong symbol: Python expects PyInit__native_wrong but we provide PyInit__native_wrong_typo */
PyMODINIT_FUNC PyInit__native_wrong_typo(void) {
    return PyModule_Create(&wrong_def);
}
