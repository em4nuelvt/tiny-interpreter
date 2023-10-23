from lexical import LexicalAnalysis,TokenType,tt2str


from syntatic import SyntaticAnalysis

if __name__ == '__main__':
    lex = LexicalAnalysis('exemplos/neg.tiny')
    syntactic = SyntaticAnalysis(lex)
    cmd = syntactic.start()
    cmd.execute()


""" if __name__ == '__main__':
    lex = LexicalAnalysis('exemplos/sum.tiny')
    token = lex.nextToken()
    while token.type != TokenType.TT_END_OF_FILE:
        print(f"Token: {token.token}, Type: {tt2str(token.type)}")
        token = lex.nextToken() """
