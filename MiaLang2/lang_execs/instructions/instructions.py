import enum
import io
import json
import keyword
from pprint import pformat, pprint
import tokenize as tokenizer
from tokenize import TokenInfo
import token as T
from typing import List, Optional, Tuple, Union

import MiaLang2.lang_enums as m_enums  # noqa: F401
import MiaLang2.lang_nodes as m_nodes  # noqa: F401
import MiaLang2.lang_types as m_types  # noqa: F401
import MiaLang2.lang_execs as m_execs  # noqa: F401


class VarInstruction:
    COUNT_OF_ARGS = 2
    
    def __init__(self, t_instruction: TokenInfo, t_args: List[TokenInfo], instruction_key: 'm_enums.KeywordsEnum'):
        self._instruction_key = instruction_key
        self._t_instruction = t_instruction
        self._t_args = t_args
        
        self.var_type_class: Union[m_types.IntType, None] = None
        self.var_type_obj = None
        self.var_id: str = None
        
        self.parse_tokens()
        
    def parse_tokens(self):
        v_type = self._t_args[0].string
        v_id = self._t_args[1].string
        self.var_type_class = m_enums.TypesEnum[v_type].get_type_class()
        self.var_type_obj = self.var_type_class()
        self.var_id = v_id
        pass
        
    def to_dict(self):
        return {
            'VarInstruction': {
                'KEY': repr(self._instruction_key),
                'VAR_TYPE': repr(self.var_type_obj),
                'VAR_ID': self.var_id
            }
        }