#%%
try:
    import numpy
except ImportError:
    print('OpenCV bindings requires "numpy" package.')
    print('Install it via command:')
    print('    pip install numpy')
    raise

try:
    import pyodbc
except ImportError:
    print('OpenCV bindings requires "pyodbc" package.')
    print('Install it via command:')
    print('    pip install pyodbc')
    raise

try:
    import pandas
except ImportError:
    print('OpenCV bindings requires "pandas" package.')
    print('Install it via command:')
    print('    pip install pandas')
    raise

try:
    import logging
except ImportError:
    print('OpenCV bindings requires "logging" package.')
    print('Install it via command:')
    print('    pip install logging')
    raise

from AS_SQL.SQL import DB

__all__ = ['DB']