import enum
import io
import keyword
from pprint import pformat, pprint
import tokenize as tokenizer
from tokenize import TokenInfo
import token as T
from typing import List

code = b"""
var int a;
a = 10;
"""

# [ - LSQB
# ] - RSQB
# { - LBRACE
# } - RBRACE
# ( - LPAR
# ) - RPAR
# ; - SEMI
# = - EQUAL
# , - COMMA

class KEYWORDS(enum.Enum):
    var = 0
    
    @classmethod
    def is_keyword(cls, name: str) -> bool:
        try:
            cls[name]
            return True
        except KeyError:
            return False
    
    
class VarInstruction:
    def __init__(self, t_instruction: TokenInfo, t_args: List[TokenInfo]):
        self._t_instruction = t_instruction
        self._t_args = t_args


class LineNode:
    def __init__(self, _tokens: List[TokenInfo]):
        self._tokens = _tokens
        self._instruction_node: InstructionNode = None
        self._expr_node: ExprNode = None
        self._id_node: IdNode = None
        self.parse_tokens()

    def __repr__(self) -> str:
        return repr(self.to_dict())

    def to_dict(self) -> dict:
        return {
            f'LineNode({[k.string for k in self._tokens]}': {
                'INST': self._instruction_node.to_dict() if self._instruction_node is not None else None,
                'EXPR': self._expr_node.to_dict() if self._expr_node is not None else None
            }
        }

    def parse_tokens(self):
        for i, t in enumerate(self._tokens):
            t_name = t.string
            t_line = t.line
            t_type = t.type
            
            # Что находится в этой строке: Инструкция или Выражение
            if i == 0:
                if KEYWORDS.is_keyword(t_name):
                    t_args = self._tokens[i:]
                    self._instruction_node = InstructionNode(t, t_args)
                else:
                    t_args = self._tokens[i:]
                    self._expr_node = ExprNode(t, t_args)
                

class ExprNode:
    def __init__(self, t_id: TokenInfo, t_args: List[TokenInfo]) -> None:
        self._t_id = t_id
        self._t_args = t_args
        
    def __repr__(self) -> str:
        return repr(self.to_dict())
        
    def to_dict(self) -> dict:
        return {
            'ExprNode': {'ARGS': [k.string for k in self._t_args]}
        }


class InstructionNode:
    def __init__(self, t: TokenInfo, t_args: List[TokenInfo]) -> None:
        self._t_instruction = t
        self._t_args = t_args
        
    def __repr__(self) -> str:
        return repr(self.to_dict())

    def to_dict(self) -> dict:
        return {
            'InstructionNode': {
                'INST': self._t_instruction.string,
                'ARGS': [k.string for k in self._t_args]    
            }
        }
        
    
class ValueNode:
    def __init__(self) -> None:
        pass


class IdNode:
    def __init__(self) -> None:
        pass
    

    

f_readline = io.BytesIO(code).readline

tokens = tokenizer.tokenize(f_readline)
tokens = [t for t in tokens if t.exact_type not in (T.NL, T.NEWLINE, T.ENCODING, T.ENDMARKER)]

for t in tokens:
    print(t.string, T.tok_name[t.exact_type])
    

line_nodes = []
line_tokens = []
for t in tokens:
    if t.exact_type == T.SEMI:
        line_nodes.append(LineNode(line_tokens))
        line_tokens = []
        continue
    line_tokens.append(t)
        
        
pprint([k.to_dict() for k in line_nodes], width=10)
