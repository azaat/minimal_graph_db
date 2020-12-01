from antlr4 import *
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import Tree
from antlr4.tree.Trees import Trees

from antlr.DbQlGrammarLexer import DbQlGrammarLexer
from antlr.DbQlGrammarParser import DbQlGrammarParser
from antlr.TraversalListener import TraversalListener
from graphviz import Digraph


def get_node_name():
    get_node_name.counter += 1
    return str(get_node_name.counter)


get_node_name.counter = 0


class VerboseListener(ErrorListener):
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        print(f"Error on line: {line} msg: {msg}")
        raise ParseCancellationException(f"line: {line} msg: {msg}")


def parse(input_str):
    return parse_to_tree(input_str) is not None


def parse_to_tree(input_str):
    in_stream = InputStream(input_str)
    lexer = DbQlGrammarLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = DbQlGrammarParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(VerboseListener())
    try:
        tree = parser.script()
        return tree, parser
    except ParseCancellationException:
        return None


def generate_dot(input_str, file, should_view:bool):
    tree, parser = parse_to_tree(input_str)
    if tree is not None:
        print("Parsing succeeded, generating DOT file")
        dot = Digraph()
        traverse(tree, file, dot, get_node_name())
        dot.render(file, view=should_view)
    else:
        print("Parsing unsuccessful, check previous error messages for more details")


def traverse(tree: Tree, file, dot, node_name):
    children = Trees.getChildren(tree)
    for child in children:
        node = Trees.getNodeText(tree, DbQlGrammarParser.ruleNames)
        child_node = Trees.getNodeText(child, DbQlGrammarParser.ruleNames)
        child_name = get_node_name()

        dot.node(node_name, node)
        dot.node(child_name, child_node)

        dot.edge(node_name, child_name)
        traverse(child, file, dot, child_name)
