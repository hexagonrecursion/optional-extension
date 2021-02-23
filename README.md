# Q
# How to build py3-none-any wheels for a python project with an optional C extension?

[msgpack](https://pypi.org/project/msgpack/) includes an optional cython
extension. [Some users of the package want py3-none-any wheels of msgpack](https://github.com/ionrock/cachecontrol/issues/160#issue-240767043). I'm trying to figure out how to make
it possible to build wheels both with and without the optional extension.

# A
One possible solution is to use an environment variable in `setup.py` to decide
whether to set `ext_modules` to an empty list of a list of `setuptools.Extension`

# pyproject.toml
```toml
[build-system]
requires = ["setuptools", "wheel", "cython"]
build-backend = "setuptools.build_meta"
```

# setup.py
```py
from setuptools import setup, Extension
import os

if 'ONLY_PURE' in os.environ:
    ext_modules = []
else:
    module1 = Extension('helloworld', sources = ['helloworld.pyx'])
    ext_modules = [module1]
setup(ext_modules=ext_modules)
```

# setup.cfg
```cfg
[metadata]
name = mypackage
version = 0.0.1

[options]
py_modules = mypackage
```


# mypackage.py
```py
try:
    import helloworld
except ImportError:
    print('hello pure python')
```

# helloworld.pyx
```pyx
print("hello extension")
```

# To build with extension:
```shell
$ pip install build
...
$ python -m build
...
$ ls dist/
mypackage-0.0.1-cp39-cp39-linux_x86_64.whl  mypackage-0.0.1.tar.gz
```

# To build without extension
```shell
$ pip install build
...
$ ONLY_PURE='a nonempty string' python -m build
...
$ ls dist/
mypackage-0.0.1-py3-none-any.whl  mypackage-0.0.1.tar.gz
```
