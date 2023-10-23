from enum import Enum

# TokenType Definition
class TokenType(Enum):
    # Specials
    TT_UNEXPECTED_EOF = -2
    TT_INVALID_TOKEN = -1
    TT_END_OF_FILE = 0

    # Symbols
    TT_SEMICOLON = 1    # ;
    TT_ASSIGN = 2        # =

    # Logic operators
    TT_EQUAL = 3         # ==
    TT_NOT_EQUAL = 4     # !=
    TT_LOWER = 5         # <
    TT_LOWER_EQUAL = 6   # <=
    TT_GREATER = 7       # >
    TT_GREATER_EQUAL = 8 # >=

    # Arithmetic operators
    TT_ADD = 9           # +
    TT_SUB = 10           # -
    TT_MUL = 11         # *
    TT_DIV = 12          # /
    TT_MOD = 13          # %
    TT_POT = 14

    # Keywords
    TT_PROGRAM = 15      # program
    TT_WHILE = 16        # while
    TT_DO = 17           # do
    TT_DONE = 18         # done
    TT_IF = 19         # if
    TT_THEN = 20         # then
    TT_ELSE = 21         # else
    TT_OUTPUT = 22       # output
    TT_TRUE = 23       # true
    TT_FALSE = 24        # false
    TT_READ = 25        # read
    TT_NOT = 26         # not

    # Others
    TT_NUMBER = 27       # number
    TT_VAR = 28         # variable


def tt2str(token_type):
    return token_type.name

class Lexeme:
    def __init__(self, token: str, type: TokenType) -> None:
        self.token = token
        self.type = type



# SymbolTable Definition
class SymbolTable:

    st: dict = {
        # simbolos
        ';': TokenType.TT_SEMICOLON,
        '=': TokenType.TT_ASSIGN,

        # operadores logicos
        '==': TokenType.TT_EQUAL,
        '!=': TokenType.TT_NOT_EQUAL,
        '<':  TokenType.TT_LOWER,
        '<=': TokenType.TT_LOWER_EQUAL,
        '>':  TokenType.TT_GREATER,
        '>=': TokenType.TT_GREATER_EQUAL,

        # operadores aritmeticos
        '+': TokenType.TT_ADD,
        '-': TokenType.TT_SUB,
        '*': TokenType.TT_MUL,
        '/': TokenType.TT_DIV,
        '%': TokenType.TT_MOD,
        '^': TokenType.TT_POT,

        # palavras-chave
        'program': TokenType.TT_PROGRAM,
        'while': TokenType.TT_WHILE,
        'do': TokenType.TT_DO,
        'done': TokenType.TT_DONE,
        'if': TokenType.TT_IF,
        'then': TokenType.TT_THEN,
        'else': TokenType.TT_ELSE,
        'output': TokenType.TT_OUTPUT,
        'true': TokenType.TT_TRUE,
        'false': TokenType.TT_FALSE,
        'read': TokenType.TT_READ,
        'not': TokenType.TT_NOT,
    }

    def contains(self, token: str) -> bool:
        return token in self.st

    def find(self, token: str) -> TokenType:
        if self.contains(token):
            return self.st.get(token)
        else:
            return TokenType.TT_VAR


#State Machine
class LexicalAnalysis:
    def __init__(self, filename: str) -> None:
        try:
            self.input = open(filename, 'r')
        except FileNotFoundError as fe:
            raise Exception(
                'O arquivo {} não foi encontrado!'.format(filename))

        self.st = SymbolTable()
        self.line = 1

    def getChar(self) -> str:
        try:
            return self.input.read(1)
        except:
            raise ValueError("Erro ao ler o arquivo!")

    def nextToken(self) -> Lexeme:

        lex = Lexeme("", TokenType.TT_END_OF_FILE)
        state = 1

        while state != 7 and state != 8:
            c = self.getChar()

            # if(c.isalpha()):
            #     print("c: ", c)
            # else:
            #     print("c: ", ord(c))

            # print("state: ", state)

            match state:
                case 1:
                    if c == ' ' or c == '\r' or c == '\t':
                        state = 1
                    elif c == '\n':
                        self.line += 1
                        state = 1
                    elif c == '#':
                        state = 2
                    elif c == '=' or c == '<' or c == '>':
                        lex.token += c
                        state = 3
                    elif c == '!':
                        lex.token += c
                        state = 4
                    elif c == ';' or c == '+' or c == '-' or c == '*' or c == '/' or c == '%' or c=='^':
                        lex.token += c
                        state = 7
                    elif c.isalpha() or c == '_':
                        lex.token += c
                        state = 5
                    elif c.isdigit():
                        lex.token += c
                        state = 6
                    elif c == '':
                        lex.type = TokenType.TT_END_OF_FILE
                        state = 8
                    else:
                        lex.token += c
                        lex.type = TokenType.TT_INVALID_TOKEN
                        state = 8
                case 2:
                    if c == '\n':
                        self.line += 1
                        state = 1
                    elif c == '':
                        lex.type = TokenType.TT_END_OF_FILE
                        state = 8
                    else:
                        state = 2
                case 3:
                    if c == '=':
                        lex.token += c
                        state = 7
                    else:
                        self.input.seek(self.input.tell() - 1)
                        state = 7
                case 4:
                    if c == '=':
                        lex.token += c
                    elif c == '':
                        lex.type = TokenType.TT_UNEXPECTED_EOF
                        state = 8
                    else:
                        lex.type = TokenType.TT_INVALID_TOKEN
                        state = 8
                case 5:
                    if c.isalpha() or c.isdigit() or c == '_':
                        lex.token += c
                        state = 5
                    else:
                        self.input.seek(self.input.tell() - 1)
                        state = 7
                case 6:
                    if c.isdigit():
                        lex.token += c
                        state = 6
                    else:
                        self.input.seek(self.input.tell() - 1)
                        lex.type = TokenType.TT_NUMBER
                        state = 8
                case _:
                    print(lex.token)
                    print(state)
                    raise ValueError("Unreachable")

        if state == 7:
            lex.type = self.st.find(lex.token)

        return lex