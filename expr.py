from abc import ABC, abstractmethod
import enum

# Classe base IntExpr
class IntExpr(ABC):
    def __init__(self, line):
        self._line = line

    @property
    def line(self):
        return self._line

    @abstractmethod
    def expr(self):
        pass

# Subclasse BinaryIntExpr
class BinaryIntExpr(IntExpr):
    class Op(enum.Enum):
        ADD = 1
        SUB = 2
        MUL = 3
        DIV = 4
        MOD = 5

    def __init__(self, line, left, op, right):
        super().__init__(line)
        self._left = left
        self._op = op
        self._right = right

    def expr(self):
        if self._op == BinaryIntExpr.Op.ADD:
            return self._left.expr() + self._right.expr()
        elif self._op == BinaryIntExpr.Op.SUB:
            return self._left.expr() - self._right.expr()
        elif self._op == BinaryIntExpr.Op.MUL:
            return self._left.expr() * self._right.expr()
        elif self._op == BinaryIntExpr.Op.DIV:
            return self._left.expr() / self._right.expr()
        elif self._op == BinaryIntExpr.Op.MOD:
            return self._left.expr() % self._right.expr()

# Subclasse ConstIntExpr
class ConstIntExpr(IntExpr):
    def __init__(self, line, value):
        super().__init__(line)
        self._value = value

    def expr(self):
        return self._value

# Subclasse NegIntExpr
class NegIntExpr(IntExpr):
    def __init__(self, line, expr):
        super().__init__(line)
        self._expr = expr

    def expr(self):
        return -self._expr.expr()

# Subclasse ReadIntExpr
class ReadIntExpr(IntExpr):
    def __init__(self, line):
        super().__init__(line)

    def expr(self):
        return int(input())
from typing import Dict

# Classe Memory 
class Memory:
    _memory: Dict[str, int] = {}

    @staticmethod
    def read(name: str) -> int:
        return Memory._memory.get(name, 0)  # Retorna 0 se a variável não estiver definida

    @staticmethod
    def write(name: str, value: int) -> None:
        Memory._memory[name] = value

# Subclasse Variable 
class Variable(IntExpr):
    def __init__(self, line: int, name: str):
        super().__init__(line)
        self._name = name

    def name(self) -> str:
        return self._name

    def value(self) -> int:
        return Memory.read(self._name)

    def setValue(self, value: int) -> None:
        Memory.write(self._name, value)

    def expr(self) -> int:
        return self.value()


# Classe base BoolExpr
class BoolExpr(ABC):
    def __init__(self, line: int):
        self._line = line

    @property
    def line(self) -> int:
        return self._line

    @abstractmethod
    def expr(self) -> bool:
        pass

# Subclasse ConstBoolExpr
class ConstBoolExpr(BoolExpr):
    def __init__(self, line: int, value: bool):
        super().__init__(line)
        self._value = value

    def expr(self) -> bool:
        return self._value

# Subclasse NotBoolExpr
class NotBoolExpr(BoolExpr):
    def __init__(self, line: int, expr: BoolExpr):
        super().__init__(line)
        self._expr = expr

    def expr(self) -> bool:
        return not self._expr.expr()

# Subclasse SingleBoolExpr
class SingleBoolExpr(BoolExpr):
    class Op(enum.Enum):
        EQUAL = 1
        NOT_EQUAL = 2
        LOWER = 3
        GREATER = 4
        LOWER_EQUAL = 5
        GREATER_EQUAL = 6

    def __init__(self, line: int, left: "IntExpr", op: Op, right: "IntExpr"):
        super().__init__(line)
        self._left = left
        self._op = op
        self._right = right

    def expr(self) -> bool:
        v1 = self._left.expr()
        v2 = self._right.expr()

        if self._op == SingleBoolExpr.Op.EQUAL:
            return v1 == v2
        elif self._op == SingleBoolExpr.Op.NOT_EQUAL:
            return v1 != v2
        elif self._op == SingleBoolExpr.Op.LOWER:
            return v1 < v2
        elif self._op == SingleBoolExpr.Op.LOWER_EQUAL:
            return v1 <= v2
        elif self._op == SingleBoolExpr.Op.GREATER:
            return v1 > v2
        elif self._op == SingleBoolExpr.Op.GREATER_EQUAL:
            return v1 >= v2
