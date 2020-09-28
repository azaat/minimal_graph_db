from src.grammar_cnf import GrammarCNF
CFG_BRACKETS = 'S -> a S b S\nS -> '


def test_brackets_word_accepts():
    cnf = GrammarCNF.from_text(CFG_BRACKETS)
    word_accepts = 'aabb'
    assert cnf.contains(word_accepts) is True


def test_brackets_epsilon_accepts():
    cnf = GrammarCNF.from_text(CFG_BRACKETS)
    word_epsilon = ''
    assert cnf.contains(word_epsilon) is True


def test_brackets_not_accepts():
    cnf = GrammarCNF.from_text(CFG_BRACKETS)
    word_not_accepts = 'aabba'
    assert cnf.contains(word_not_accepts) is False
