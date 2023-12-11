import enum
import io
import json
import keyword
from pprint import pformat, pprint
import tokenize as tokenizer
from tokenize import TokenInfo
import token as T
from typing import List, Optional, Tuple, Union

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


class TypesEnum(enum.Enum):
    int = 0
    
    def get_type_class(self) -> Union['IntType', None]:
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


class IntType:
    DEFAULT_VALUE = 0
    
    def __init__(self):
        self._value = __class__.DEFAULT_VALUE

    def __repr__(self) -> str:
        return f'<T:IntType({self._value})>'
    
    
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
    
    
class VarInstruction:
    COUNT_OF_ARGS = 2
    
    def __init__(self, t_instruction: TokenInfo, t_args: List[TokenInfo], instruction_key: KEYWORDS):
        self._instruction_key = instruction_key
        self._t_instruction = t_instruction
        self._t_args = t_args
        
        self.var_type_class: Union[IntType, None] = None
        self.var_type_obj = None
        self.var_id: str = None
        
        self.parse_tokens()
        
    def parse_tokens(self):
        v_type = self._t_args[0].string
        v_id = self._t_args[1].string
        self.var_type_class = TypesEnum[v_type].get_type_class()
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
                if KEYWORDS.is_keyword(t_name):
                    t_args = self._tokens[1:]
                    self._instruction_node = InstructionNode(t, t_args)
                else:
                    t_args = self._tokens[0:]
                    self._expression_node = ExpressionNode(t_args)
                

class ExpressionNode:
    def __init__(self, t_args: List[TokenInfo]) -> None:
        self._t_args = t_args
        
        self._operator_class: Union[AssignSingleOperator, None] = None
        self._operator_obj: Union[AssignSingleOperator, None] = None
        # self._t1 = None
        # self._t2 = 
        
        self.parse_tokens()
        
    def __repr__(self) -> str:
        return repr(self.to_dict())
    
    def parse_tokens(self):
        single_operator = None
        double_operator = None
        
        for i, t in enumerate(self._t_args):
            single_operator = SingleOperatorsEnum.get_single_operator(t.string)
            if single_operator is not None:
                self._operator_class: AssignSingleOperator = single_operator.get_operator_class()
                self._operator_obj = self._operator_class(
                    self._operator_class.VARIANT_ID_OP_VALUE,
                    self._t_args[i - 1], t, self._t_args[i + 1]
                )
            elif double_operator is not None:
                break
        
        if single_operator is not None:
            SingleOperatorsEnum.get_operator_class()
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
        instruction_key = KEYWORDS[self._t_instruction.string]
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
    data = [k.to_dict() for k in line_nodes]
    data = {'__MAIN__': data}
    json.dump(data, f, ensure_ascii=False, indent=4)
    pprint(data, width=10)
