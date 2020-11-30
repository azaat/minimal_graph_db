from antlr4 import *
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorListener import ErrorListener
from antlr.DbQlGrammarLexer import DbQlGrammarLexer
from antlr.DbQlGrammarParser import DbQlGrammarParser


class VerboseListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseCancellationException(f"line: {line} msg: {msg}")


def parse(input_str):
    in_stream = InputStream(input_str)
    lexer = DbQlGrammarLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = DbQlGrammarParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(VerboseListener())
    try:
        parser.script()
        print(parser.getNumberOfSyntaxErrors())
        return True
    except ParseCancellationException:
        return False



