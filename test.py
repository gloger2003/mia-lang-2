import enum
import io
import keyword
from pprint import pprint
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
    


class LineNode:
    def __init__(self, _tokens: List[TokenInfo]):
        self._tokens = _tokens
        self._instruction_node: InstructionNode = None
        self._expr_node: ExprNode = None
        self._id_node: IdNode = None
        self.parse_tokens()

    def parse_tokens(self):
        for t in self._tokens:
            tname = t.string
            tline = t.line
            ttype = t.type
            
            if KEYWORDS.is_keyword(tname):
                self._instruction_node = InstructionNode()
                
            
        
    def __repr__(self) -> str:
        return f'LineNode({[k.string for k in self._tokens]} | INST={self._instruction_node} | EXPR={self._expr_node})'
        

class ExprNode:
    def __init__(self) -> None:
        pass
    
    
class ValueNode:
    def __init__(self) -> None:
        pass


class IdNode:
    def __init__(self) -> None:
        pass
    

class InstructionNode:
    def __init__(self, t) -> None:
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
        
pprint(line_nodes, width=10)
