from setuptools import setup, Extension
import os

if 'ONLY_PURE' in os.environ:
    ext_modules = []
else:
    module1 = Extension('helloworld', sources = ['helloworld.pyx'])
    ext_modules = [module1]
setup(ext_modules=ext_modules)
