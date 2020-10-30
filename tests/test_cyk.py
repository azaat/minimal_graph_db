from src.grammar_cnf import GrammarCNF
from tests.cfpq_test_helper import TEST_GRAMMARS


def test_1_word_accepts():
    cnf = GrammarCNF.from_text(TEST_GRAMMARS[0])
    word_accepts = 'aabb'
    assert cnf.contains(word_accepts) is True


def test_1_epsilon_accepts():
    cnf = GrammarCNF.from_text(TEST_GRAMMARS[0])
    word_epsilon = ''
    assert cnf.contains(word_epsilon) is True


def test_1_not_accepts():
    cnf = GrammarCNF.from_text(TEST_GRAMMARS[0])
    word_not_accepts = 'aabba'
    assert cnf.contains(word_not_accepts) is False


def test_2_accepts():
    cnf = GrammarCNF.from_text(TEST_GRAMMARS[1])
    assert cnf.contains('abab')
    assert cnf.contains('ab')


def test_2_epsilon_not_accepts():
    cnf = GrammarCNF.from_text(TEST_GRAMMARS[1])
    assert cnf.contains('') is False
