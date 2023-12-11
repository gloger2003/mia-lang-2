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


class AssignSingleOperator:
    COUNT_OF_ARGS = 2
    VARIANT_ID_OP_VALUE = ('ID', '=','VALUE')
    VARIANT_ID_OP_ID = ('ID', '=', 'ID')
    
    def __init__(self, variant: Tuple[str], t1: TokenInfo, t_op: TokenInfo, t2: TokenInfo):
        self._t1 = t1
        self._t2 = t2
        self._t_op = t_op
        self._variant: Tuple[str] = variant
    
    def to_dict(self) -> dict:
        return {
            'AssignSignleOperator': {   
                'LINE': f'{self._t1.string} {self._t_op.string} {self._t2.string}',
                'VARIANT': f'<{self._variant[0]}> {self._t_op.string} <{self._variant[2]}>'
            }
        }
