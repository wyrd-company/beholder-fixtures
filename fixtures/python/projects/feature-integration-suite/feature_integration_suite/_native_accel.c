#include <Python.h>

static PyObject *native_fast_add(PyObject *self, PyObject *args) {
    long a, b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b)) {
        return NULL;
    }
    return PyLong_FromLong(a + b);
}

static PyObject *native_fast_multiply(PyObject *self, PyObject *args) {
    long a, b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b)) {
        return NULL;
    }
    return PyLong_FromLong(a * b);
}

static PyMethodDef methods[] = {
    {"fast_add", native_fast_add, METH_VARARGS, "Native fast add"},
    {"fast_multiply", native_fast_multiply, METH_VARARGS, "Native fast multiply"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moddef = {
    PyModuleDef_HEAD_INIT,
    "_native_accel",
    "Native accelerator for PY-CAN-INT-008",
    -1,
    methods
};

PyMODINIT_FUNC PyInit__native_accel(void) {
    return PyModule_Create(&moddef);
}
