from pygraphblas import BOOL, Matrix, lib


class LabelGraph:
    def __init__(self):
        self.graph_dict = {}
        self.num_vert = 0
    
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
        return self

    def get_edges(self, label):
        return zip(
            *self.graph_dict[label]
                 .select(lib.GxB_NONZERO)
                 .to_lists()[:2]
        )

    def to_GrB_matrix(self):
        res = Matrix.sparse(BOOL, self.num_vert, self.num_vert)
        for label in self.graph_dict:
            res += self.graph_dict[label]
        return res
