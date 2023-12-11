import enum
import io
import json
import keyword
from pprint import pformat, pprint
import tokenize as tokenizer
from tokenize import TokenInfo
import token as T
from typing import List, Union

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
    
    def get_instruction_class(self) -> Union['VarInstruction', None]:
        mapping = {
            KEYWORDS.var: VarInstruction
        }
        return mapping.get(self)
    
    
class VarInstruction:
    COUNT_OF_ARGS = 2
    
    def __init__(self, t_instruction: TokenInfo, t_args: List[TokenInfo], instruction_key: KEYWORDS):
        self._instruction_key = instruction_key
        self._t_instruction = t_instruction
        self._t_args = t_args
        
    def to_dict(self):
        return {
            'VarInstruction': {
                'KEY': self._instruction_key,
                'ARGS': [k.string for k in self._t_args]
            }
        }


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
            'ExprNode': {
                'ARGS': [k.string for k in self._t_args]
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
        instruction_key = KEYWORDS[self._t_instruction.string]
        self._instruction_class = instruction_key.get_instruction_class()
        t_args = self._t_args[:self._instruction_class.COUNT_OF_ARGS]
        self._instruction_class = self._instruction_class(self._t_instruction, t_args, instruction_key)

    def to_dict(self) -> dict:
        return {
            'InstructionNode': {
                'INST': self._t_instruction.string,
                'ARGS': [k.string for k in self._t_args],
                'INST_OBJ': self._instruction_obj.to_dict() if self._instruction_obj is not None else None
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
        
with open('./dump.json', 'w') as f:     
    json.dump([k.to_dict() for k in line_nodes], f, ensure_ascii=False, indent=4)
