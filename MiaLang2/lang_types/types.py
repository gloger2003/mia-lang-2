import enum
import io
import json
import keyword
from pprint import pformat, pprint
import tokenize as tokenizer
from tokenize import TokenInfo
import token as T
from typing import List, Optional, Tuple, Union

import MiaLang2.lang_enums as m_enums       # noqa: F401
import MiaLang2.lang_nodes as m_nodes       # noqa: F401
import MiaLang2.lang_types as m_types       # noqa: F401
import MiaLang2.lang_classes as m_classes   # noqa: F401


class IntType:
    DEFAULT_VALUE = 0
    
    def __init__(self):
        self._value = __class__.DEFAULT_VALUE

    def __repr__(self) -> str:
        return f'<T:IntType({self._value})>'