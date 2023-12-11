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


# LineNodesType = List[lang_nodes.LineNode]


class Parser:
    IGNORED_TOKEN_TYPES = (T.NL, T.NEWLINE, T.ENCODING, T.ENDMARKER)
    
    def __init__(self, io_buffer: io.BytesIO, need_dump_nodes=False):
        self._io_buffer: io.BytesIO = io_buffer
        self._tokens: List[TokenInfo] = []
        self._line_nodes: List[m_nodes.LineNode] = []
        self._filtered_tokens: List[m_nodes.LineNode] = []
        
        self._parse()
        
        if need_dump_nodes:
            self._dump_nodes()
            
    def _dump_nodes(self):
        with open('./dump.json', 'w') as f:
            data = [k.to_dict() for k in self._line_nodes]
            data = {'__MAIN__': data}
            json.dump(data, f, ensure_ascii=False, indent=4)
            pprint(data, width=10)
    
    def _parse(self):
        tokens = tokenizer.tokenize(self._io_buffer.readline)
        tokens = list(tokens)
        # clear_tokens = [t for t in tokens if t.exact_type not in (T.NL, T.NEWLINE, T.ENCODING, T.ENDMARKER)]
        filter_ = filter(lambda t: t.exact_type not in __class__.IGNORED_TOKEN_TYPES, tokens)
        filtered_tokens = list(filter_)

        for t in tokens:
            print(t.string, T.tok_name[t.exact_type])
            
        line_nodes = []
        line_tokens = []                                                                                                                                                                                                                                                          
        for t in filtered_tokens:
            if t.exact_type == T.SEMI:
                line_nodes.append(m_nodes.LineNode(line_tokens))
                line_tokens = []
                continue
            line_tokens.append(t)
        
        self._line_nodes = line_nodes
        self._tokens = tokens
        self._filtered_tokens = filtered_tokens
        
    def get_tokens_copy(self) -> List[TokenInfo]:
        return self._tokens.copy()
    
    def get_filtered_tokens_copy(self) -> List[TokenInfo]:
        return self._filtered_tokens.copy()
    
    def get_line_nodes_copy(self) -> List[m_nodes.LineNode]:
        return self._line_nodes.copy()
    
    def get_tokens(self) -> List[TokenInfo]:
        return self._tokens
    
    def get_filtered_tokens(self) -> List[TokenInfo]:
        return self._filtered_tokens
    
    def get_line_nodes(self) -> List[m_nodes.LineNode]:
        return self._line_nodes