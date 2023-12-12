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


class ExpressionNode:
    def __init__(self, t_args: List[TokenInfo]) -> None:
        self._t_args = t_args
        
        self._operator_class: Union[m_execs.AssignSingleOperator, None] = None
        self._operator_obj: Union[m_execs.AssignSingleOperator, None] = None
        
        self.parse_tokens()
        
    def __repr__(self) -> str:
        return repr(self.to_dict())
    
    def parse_tokens(self):
        single_operator = None
        double_operator = None
        
        for i, t in enumerate(self._t_args):
            single_operator = m_enums.SingleOperatorsEnum.get_single_operator(t.string)
            if single_operator is not None:
                self._operator_class: m_execs.AssignSingleOperator = single_operator.get_operator_class()
                self._operator_obj = self._operator_class(
                    self._operator_class.VARIANT_ID_OP_VALUE,
                    self._t_args[i - 1], t, self._t_args[i + 1]
                )
            elif double_operator is not None:
                break
        
        if single_operator is not None:
            m_enums.SingleOperatorsEnum.get_operator_class()
        pass
        
    def to_dict(self) -> dict:
        return {
            'ExpressionNode': {
                'ARGS': [k.string for k in self._t_args],
                'OPERATOR': self._operator_obj.to_dict() if self._operator_obj is not None else None
            }
        }