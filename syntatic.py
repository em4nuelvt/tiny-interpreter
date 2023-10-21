from lexical import TokenType
from expr import *
from command import *

class SyntaticAnalysis:
    def __init__(self, lex):
        self.m_lex = lex
        self.m_current = lex.nextToken()

    def start(self):
        cmd = self.proc_program()
        self.eat(TokenType.TT_END_OF_FILE)
        return cmd

    def advance(self):
        self.m_current = self.m_lex.nextToken()

    def eat(self, token_type):
        if token_type == self.m_current.type:
            self.advance()
        else:
            self.show_error()

    def show_error(self):
        print(f"{self.m_lex.line:02}: ", end="")
        if self.m_current.type == TokenType.TT_INVALID_TOKEN:
            print(f"Lexema inválido [{self.m_current.token}]")
        elif self.m_current.type in [TokenType.TT_UNEXPECTED_EOF, TokenType.TT_END_OF_FILE]:
            print("Fim de arquivo inesperado")
        else:
            print(f"Lexema não esperado [{self.m_current.token}]")
        exit(1)

    def proc_program(self):
        self.eat(TokenType.TT_PROGRAM)
        cmd = self.proc_cmdlist()
        return cmd

    def proc_cmdlist(self):
        line = self.m_lex.line
        cmds = BlocksCommand(line)

        cmd = self.proc_cmd()
        cmds.addCommand(cmd)
        

        while self.m_current.type in [TokenType.TT_VAR, TokenType.TT_OUTPUT, TokenType.TT_IF, TokenType.TT_WHILE]:
            cmd = self.proc_cmd()
            cmds.addCommand(cmd)

        return cmds

    def proc_cmd(self):
        cmd = None
        if self.m_current.type == TokenType.TT_VAR:
            cmd = self.proc_assign()
        elif self.m_current.type == TokenType.TT_OUTPUT:
            cmd = self.proc_output()
        elif self.m_current.type == TokenType.TT_IF:
            cmd = self.proc_if()
        elif self.m_current.type == TokenType.TT_WHILE:
            cmd = self.proc_while()
        else:
            self.show_error()

        self.eat(TokenType.TT_SEMICOLON)
        return cmd

    def proc_assign(self):
        line = self.m_lex.line
        var = self.proc_var()
        self.eat(TokenType.TT_ASSIGN)
        expr = self.proc_intexpr()
        cmd = AssignCommand(line, var, expr)
        return cmd

    def proc_output(self):
        self.eat(TokenType.TT_OUTPUT)
        line = self.m_lex.line
        expr = self.proc_intexpr()
        cmd = OutputCommand(line, expr)
        return cmd

    def proc_if(self):
        self.eat(TokenType.TT_IF)
        line = self.m_lex.line
        cond = self.proc_boolexpr()
        self.eat(TokenType.TT_THEN)
        then_cmds = self.proc_cmdlist()
        else_cmds = None
        if self.m_current.type == TokenType.TT_ELSE:
            self.advance()
            else_cmds = self.proc_cmdlist()
        self.eat(TokenType.TT_DONE)
        cmd = IfCommand(line, cond, then_cmds, else_cmds)
        return cmd

    def proc_while(self):
        self.eat(TokenType.TT_WHILE)
        line = self.m_lex.line
        expr = self.proc_boolexpr()
        self.eat(TokenType.TT_DO)
        cmds = self.proc_cmdlist()
        self.eat(TokenType.TT_DONE)
        cmd = WhileCommand(line, expr, cmds)
        return cmd

    def proc_boolexpr(self):
        if self.m_current.type == TokenType.TT_FALSE:
            self.advance()
            return ConstBoolExpr(self.m_lex.line, False)
        elif self.m_current.type == TokenType.TT_TRUE:
            self.advance()
            return ConstBoolExpr(self.m_lex.line, True)
        elif self.m_current.type == TokenType.TT_NOT:
            self.advance()
            line = self.m_lex.line
            expr = self.proc_boolexpr()
            return NotBoolExpr(line, expr)
        else:
            line = self.m_lex.line
            left = self.proc_intterm()

            op = SingleBoolExpr.Op.EQUAL
            if self.m_current.type == TokenType.TT_EQUAL:
                op = SingleBoolExpr.Op.EQUAL
                self.advance()
            elif self.m_current.type == TokenType.TT_NOT_EQUAL:
                op = SingleBoolExpr.Op.NOT_EQUAL
                self.advance()
            elif self.m_current.type == TokenType.TT_LOWER:
                op = SingleBoolExpr.Op.LOWER
                self.advance()
            elif self.m_current.type == TokenType.TT_GREATER:
                op = SingleBoolExpr.Op.GREATER
                self.advance()
            elif self.m_current.type == TokenType.TT_LOWER_EQUAL:
                op = SingleBoolExpr.Op.LOWER_EQUAL
                self.advance()
            elif self.m_current.type == TokenType.TT_GREATER_EQUAL:
                op = SingleBoolExpr.Op.GREATER_EQUAL
                self.advance()
            else:
                self.show_error()

            right = self.proc_intterm()
            expr = SingleBoolExpr(line, left, op, right)
            return expr

    def proc_intexpr(self):
        is_negative = False
        if self.m_current.type == TokenType.TT_ADD:
            self.advance()
        elif self.m_current.type == TokenType.TT_SUB:
            self.advance()
            is_negative = True

        if is_negative:
            line = self.m_lex.line
            tmp = self.proc_intterm()
            left = NegIntExpr(line, tmp)
        else:
            left = self.proc_intterm()

        while self.m_current.type in [TokenType.TT_ADD, TokenType.TT_SUB, TokenType.TT_MUL, TokenType.TT_DIV, TokenType.TT_MOD]:
            line = self.m_lex.line

            if self.m_current.type == TokenType.TT_ADD:
                op = BinaryIntExpr.Op.ADD
                self.advance()
            elif self.m_current.type == TokenType.TT_SUB:
                op = BinaryIntExpr.Op.SUB
                self.advance()
            elif self.m_current.type == TokenType.TT_MUL:
                op = BinaryIntExpr.Op.MUL
                self.advance()
            elif self.m_current.type == TokenType.TT_DIV:
                op = BinaryIntExpr.Op.DIV
                self.advance()
            else:
                op = BinaryIntExpr.MOD
                self.advance()

            right = self.proc_intterm()
            left = BinaryIntExpr(line, left, op, right)

        return left

    def proc_intterm(self):
        if self.m_current.type == TokenType.TT_VAR:
            return self.proc_var()
        elif self.m_current.type == TokenType.TT_NUMBER:
            return self.proc_const()
        else:
            self.eat(TokenType.TT_READ)
            line = self.m_lex.line
            expr = ReadIntExpr(line)
            return expr

    def proc_var(self):
        tmp = self.m_current.token
        self.eat(TokenType.TT_VAR)
        line = self.m_lex.line
        var = Variable(line, tmp)
        return var

    def proc_const(self):
        tmp = self.m_current.token
        self.eat(TokenType.TT_NUMBER)
        line = self.m_lex.line
        value = int(tmp)
        expr = ConstIntExpr(line, value)
        return expr
