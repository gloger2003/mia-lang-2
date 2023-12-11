import io
from .parser import Parser as __Parser


def run_from_string(text: str, need_dump_nodes=False):
    data = text.encode()
    __Parser(io.BytesIO(data), need_dump_nodes)


def run_from_bytes(bytes: bytes):
    raise NotImplementedError()


def run_from_file(file):
    raise NotImplementedError()


def run_from_filename(filename: str, need_dump_nodes=False):
    with open(filename, 'rb') as f:
        data = f.read()

    __Parser(io.BytesIO(data), need_dump_nodes)
    
    
if __name__ == '__main__':
    raise NotImplementedError()