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


class LineNode:
    def __init__(self, _tokens: List[TokenInfo]):
        self._tokens = _tokens
        self._instruction_node: InstructionNode = None
        self._expression_node: ExpressionNode = None
        self.parse_tokens()

    def __repr__(self) -> str:
        return repr(self.to_dict())

    def to_dict(self) -> dict:
        return {
            'LineNode': {
                'TOKENS': [k.string for k in self._tokens],
                'INST_NODE': self._instruction_node.to_dict() if self._instruction_node is not None else None,
                'EXPR_NODE': self._expression_node.to_dict() if self._expression_node is not None else None
            }
        }

    def parse_tokens(self):
        for i, t in enumerate(self._tokens):
            t_name = t.string
            t_line = t.line
            t_type = t.type
            
            # Что находится в этой строке: Инструкция или Выражение
            if i == 0:
                if m_enums.KeywordsEnum.is_keyword(t_name):
                    t_args = self._tokens[1:]
                    self._instruction_node = InstructionNode(t, t_args)
                else:
                    t_args = self._tokens[0:]
                    self._expression_node = ExpressionNode(t_args)


class ExpressionNode:
    def __init__(self, t_args: List[TokenInfo]) -> None:
        self._t_args = t_args
        
        self._operator_class: Union[m_classes.AssignSingleOperator, None] = None
        self._operator_obj: Union[m_classes.AssignSingleOperator, None] = None
        
        self.parse_tokens()
        
    def __repr__(self) -> str:
        return repr(self.to_dict())
    
    def parse_tokens(self):
        single_operator = None
        double_operator = None
        
        for i, t in enumerate(self._t_args):
            single_operator = m_enums.SingleOperatorsEnum.get_single_operator(t.string)
            if single_operator is not None:
                self._operator_class: m_classes.AssignSingleOperator = single_operator.get_operator_class()
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
        

class InstructionNode:
    def __init__(self, t: TokenInfo, t_args: List[TokenInfo]) -> None:
        self._t_instruction = t
        self._t_args = t_args
        self._instruction_class: Union[VarInstruction, None] = None
        self._instruction_obj: Union[VarInstruction, None] = None
        
        self.parse_tokens()
        
    def __repr__(self) -> str:
        return repr(self.to_dict())
    
    def parse_tokens(self):
        instruction_key = KeywordsEnum[self._t_instruction.string]
        self._instruction_class = instruction_key.get_instruction_class()
        t_args = self._t_args[:self._instruction_class.COUNT_OF_ARGS]
        self._instruction_obj = self._instruction_class(self._t_instruction, t_args, instruction_key)

    def to_dict(self) -> dict:
        return {
            'InstructionNode': {
                'INST': self._t_instruction.string,
                'ARGS': [k.string for k in self._t_args],
                'INST_OBJ': self._instruction_obj.to_dict() if self._instruction_obj is not None else None
            }
        }