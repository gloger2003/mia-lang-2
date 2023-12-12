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


class LineNode:
    def __init__(self, _tokens: List[TokenInfo]):
        self._tokens = _tokens
        self._instruction_node: m_nodes.InstructionNode = None
        self._expression_node: m_nodes.ExpressionNode = None
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
                    self._instruction_node = m_nodes.InstructionNode(t, t_args)
                else:
                    t_args = self._tokens[0:]
                    self._expression_node = m_nodes.ExpressionNode(t_args)