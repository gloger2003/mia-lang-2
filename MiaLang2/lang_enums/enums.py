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
import MiaLang2.lang_execs as m_execs   # noqa: F401


class KeywordsEnum(enum.Enum):
    var = 0
    
    @classmethod
    def is_keyword(cls, name: str) -> bool:
        try:
            cls[name]
            return True
        except KeyError:
            return False
    
    def get_instruction_class(self) -> Union['m_execs.VarInstruction', None]:
        mapping = {
            KeywordsEnum.var: m_execs.VarInstruction
        }
        return mapping.get(self)
    

class TypesEnum(enum.Enum):
    int = 0
    
    def get_type_class(self) -> Union['m_types.IntType', None]:
        mapping = {
            TypesEnum.int: IntType
        }
        return mapping.get(self)
    

class SingleOperatorsEnum(enum.Enum):
    # =
    assign = 0
    
    @classmethod
    def get_single_operator(cls, op_str: str) -> Optional['SingleOperatorsEnum']:
        mapping = {
            '=': cls.assign
        }
        return mapping.get(op_str)
    
    def get_operator_class(self) -> Union['AssignSingleOperator', None]:
        mapping = {
            SingleOperatorsEnum.assign: AssignSingleOperator
        }
        return mapping.get(self)