from typing import Optional
from expr import IntExpr, BoolExpr, Variable

# Classe base Command
class Command:
    def __init__(self, line: int):
        self._line = line
    
    @property
    def line(self) -> int:
        return self._line
    
    def execute(self):
        pass


class AssignCommand(Command):
    def __init__(self, line: int, var: Variable, expr: IntExpr):
        super().__init__(line)
        self._var = var
        self._expr = expr
    
    def execute(self):
        value = self._expr.expr()
        self._var.setValue(value)


class BlocksCommand(Command):
    def __init__(self, line: int):
        super().__init__(line)
        self._cmds = []

    def addCommand(self, cmd: Command):
        self._cmds.append(cmd)
    
    def execute(self):
        for cmd in self._cmds:
            cmd.execute()


class IfCommand(Command):
    def __init__(self, line: int, cond: BoolExpr, thenCmds: Command, elseCmds: Optional[Command] = None):
        super().__init__(line)
        self._cond = cond
        self._thenCmds = thenCmds
        self._elseCmds = elseCmds
    
    def execute(self):
        if self._cond.expr():
            self._thenCmds.execute()
        elif self._elseCmds:
            self._elseCmds.execute()


class OutputCommand(Command):
    def __init__(self, line: int, expr: IntExpr):
        super().__init__(line)
        self._expr = expr

    def execute(self):
        v = self._expr.expr()
        print(v)


class WhileCommand(Command):
    def __init__(self, line: int, cond: BoolExpr, cmds: Command):
        super().__init__(line)
        self._cond = cond
        self._cmds = cmds

    def execute(self):
        while self._cond.expr():
            self._cmds.execute()
