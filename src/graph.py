from pygraphblas import BOOL, Matrix, lib, semiring
from pyformlang.cfg import CFG


class LabelGraph:
    def __init__(self):
        self.graph_dict = {}
        self.num_vert = 0
        self.vertices = set()
    
    def from_graph_dict(self, graph_dict, num_vert):
        self.graph_dict = graph_dict
        self.num_vert = num_vert
        return self

    def from_txt(self, path):
        def get_num_vertices(path):
            res = -1
            with open(path, 'r') as f:
                for line in f:
                    v, _, to = line.split()
                    res = max(res, int(v), int(to))
            return res + 1
        self.graph_dict = {}
        f = open(path, 'r')
        self.num_vert = get_num_vertices(path)
        for line in f:
            s, p, o = line.split(' ')
            if (p not in self.graph_dict):
                self.graph_dict[p] = Matrix.sparse(
                    BOOL, self.num_vert,
                    self.num_vert
                )
            self.graph_dict[p][int(s), int(o)] = True
            self.vertices.add(int(s))
            self.vertices.add(int(o))
        return self

    def get_edges(self, label):
        return zip(
            *self.graph_dict[label]
                 .select(lib.GxB_NONZERO)
                 .to_lists()[:2]
        )

    def get_reachable(matrix):
        return zip(
            *matrix.select(lib.GxB_NONZERO)
                   .to_lists()[:2]
        )

    def to_GrB_matrix(self):
        res = Matrix.sparse(BOOL, self.num_vert, self.num_vert)
        with semiring.LOR_LAND_BOOL:
            for label in self.graph_dict:
                res += self.graph_dict[label]
        return res


class RFA(LabelGraph):
    def __init__(self):
        LabelGraph.__init__(self)
        self.start_states = set()
        self.final_states = set()
        self.var_by_vertices = {}
    
    def from_cfg(self, cfg: CFG):
        # Computing size as the sum of production sizes (1 for head + n in boody)
        self.num_vert = sum(
            1 + len(p.body) for p in cfg.productions
        )

        index_p = 0
        for p in cfg.productions:
            if (p.head.value not in self.graph_dict):
                self.graph_dict[p.head.value] = Matrix.sparse(BOOL, self.num_vert, self.num_vert)
            
            if p.body != []:
                self.start_states.add(index_p)
            
            self.var_by_vertices[(index_p, index_p + len(p.body))] = p.head.value

            for body_sym in p.body:
                if body_sym.value not in self.graph_dict:
                    self.graph_dict[body_sym.value] = Matrix.sparse(BOOL, self.num_vert, self.num_vert)
                self.graph_dict[body_sym.value][index_p, index_p + 1] = True
                self.vertices.add(index_p)
                self.vertices.add(index_p + 1)
                index_p += 1
            self.final_states.add(index_p)
            self.vertices.add(index_p)

            index_p += 1
        return self


    
