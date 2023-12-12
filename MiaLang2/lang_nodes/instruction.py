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


class InstructionNode:
    def __init__(self, t: TokenInfo, t_args: List[TokenInfo]) -> None:
        self._t_instruction = t
        self._t_args = t_args
        self._instruction_class: m_execs.AbstractInstruction = None
        self._instruction_obj: m_execs.AbstractInstruction = None
        
        self.parse_tokens()
        
    # def __repr__(self) -> str:
    #     return repr(self.to_dict())
    
    def parse_tokens(self):
        instruction_key = m_enums.KeywordsEnum[self._t_instruction.string]
        self._instruction_class = instruction_key.get_instruction_class()
        t_args = self._t_args[:self._instruction_class.COUNT_OF_ARGS]
        self._instruction_obj = self._instruction_class(self, self._t_instruction, t_args)

    def to_dict(self) -> dict:
        return {
            'InstructionNode': {
                'INST': self._t_instruction.string,
                'ARGS': [k.string for k in self._t_args],
                'INST_OBJ': self._instruction_obj.to_dict() if self._instruction_obj is not None else None
            }
        }