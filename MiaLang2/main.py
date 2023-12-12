import io
from .parser import Parser as Parser


def run_from_string(text: str, need_dump_nodes=False):
    data = text.encode()
    Parser(io.BytesIO(data), need_dump_nodes)


def run_from_bytes(bytes: bytes):
    raise NotImplementedError()


def run_from_file(file):
    raise NotImplementedError()


def run_from_filename(filename: str, need_dump_nodes=False):
    with open(filename, 'rb') as f:
        data = f.read()

    Parser(io.BytesIO(data), need_dump_nodes)
    
    
__all__ = [
    run_from_string.__name__,
    run_from_bytes.__name__,
    run_from_file.__name__,
    run_from_filename.__name__
]
    
    
if __name__ == '__main__':
    raise NotImplementedError()