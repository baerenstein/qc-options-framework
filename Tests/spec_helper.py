from unittest.mock import patch
import sys
import datetime
from .mocks.algorithm_imports import *
from .mocks.algorithm_imports import __all__

def patch_imports():
    # Create algorithm imports mock
    algorithm_mock = type('MockAlgorithmImports', (), {
        name: globals()[name] 
        for name in __all__
    })
    
    # Create patches dictionary with globals
    module_dict = {
        'datetime': datetime,
        'AlgorithmImports': algorithm_mock,
    }
    
    return patch.dict('sys.modules', module_dict), patch.dict('builtins.__dict__', module_dict)

def patch_algorithm_imports():
    return patch_imports()