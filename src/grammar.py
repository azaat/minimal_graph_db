from pyformlang.cfg import CFG, Variable, Terminal, Production, Epsilon
from pyformlang.regular_expression import Regex


# Counter function used to create unique variable names
def get_new_var_num():
    get_new_var_num.calls += 1
    return get_new_var_num.calls
get_new_var_num.calls = 0

EPS_SYM = 'eps'


# An extension of pyformlang CFG class for grammars with regex in the body
class CFGWrapper(CFG):
    def __init__(self,
                 variables=None,
                 terminals=None,
                 start_symbol=None,
                 productions=None):
        super(CFGWrapper, self).__init__(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )


    @staticmethod
    def regex_to_grammar_productions(regex, head):
        _var_dict = {}
        production_set = set()

        # Getting an NFA from regex
        enfa = regex.to_epsilon_nfa()
        enfa = enfa.minimize()
        transitions = enfa._transition_function._transitions
        
        for state in enfa.states:
            _var_dict[state] = Variable(
                # Creating new CFG variable with unique name
                '%s#REGEX#%s' % (head.value, get_new_var_num())
            )

        for head_state in transitions:
            # Adding productions from head to start states
            for start_state in enfa.start_states:
                start_p = Production(head, [_var_dict[start_state]])
                production_set.add(start_p)

            # Getting productions from NFA transitions
            for sym in list(transitions[head_state]):
                body_state = transitions[head_state][sym]
                inner_head = _var_dict[head_state]
                inner_body = []


                if sym.value == EPS_SYM:
                    inner_body.append(Epsilon())
                elif sym.value.isupper():
                    inner_body.append(Variable(sym))
                else:
                    inner_body.append(Terminal(sym))

                inner_body.append(_var_dict[body_state])
                production_set.add(
                    Production(inner_head, inner_body)
                )

                if transitions[head_state][sym] in enfa.final_states:
                    eps_p = Production(_var_dict[body_state], [])
                    production_set.add(eps_p)
        return production_set


    @staticmethod
    def from_text(text, start_symbol=Variable("S")):
        lines = text.splitlines()
        production_set = set()

        special_symbols = ['.', '\\', '+', '|', '(', ')']

        # productions
        for l in lines:
            pr = l.split(' -> ')
            head = Variable(pr[0])
            body_str = pr[1].rstrip('\n')
            #if any(sym in special_symbols for sym in body_str):
                # pyformlang doesn't accept '?' quantifier, transforming to alternative expression
            body_str = body_str.replace('?', f'|{EPS_SYM}')
            
            production_set |= CFGWrapper.regex_to_grammar_productions(
                Regex(body_str),
                head
            )
            

        return CFG(
            start_symbol=start_symbol,
            productions=production_set
        )
