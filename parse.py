import sys
from lex import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() # init current and peek

    # return true if current token matches
    def checkToken(self, kind):
        return kind == self.currToken.kind

    # return true if next token matches
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # try to match current token. if not, error. Advances the the current token
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.currToken.kind.name)
        self.nextToken()

    # advances the current token
    def nextToken(self):
        self.currToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # parsing all
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def nl(self):
        print("NEWLINE")
        self.match(TokenType.NEWLINE) # require at least 1 newline
        while(self.checkToken(TokenType.NEWLINE)): # allow more
            self.nextToken()
    
    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")
        self.expression()

        # one comparison operator and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.currToken.text)

        # can have 0 or more comparison operator and expression
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    # True if curr token is comparison operator
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)
    
    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")
        self.term()

        # 0 or more +/- and expressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()
    
    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        # can have 0 or more *// expressions
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()
    
    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()        
        self.primary()
    
    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.currToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.currToken.text)

    def statement(self):
        # check first token to identify statement type

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # zero or more statements
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        
        #"WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # zero or more statements
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)
        
        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("STAEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STAEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        
        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)
        
        else:
            self.abort("Invalid statement at" + self.currToken.text + "(" + self.currToken.kind.name + ")")
        self.nl()