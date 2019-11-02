class Expression:
    """

    """
    exprs = {}

    def __init__(self, base_variables):
        for i, v in enumerate(base_variables):
            self.exprs[v] = { 'id': i, 'tag': v, 'dot': 0 }
            self.exprs[v + '.'] = { 'id': i, 'tag': v + '.', 'dot': 1 }
            self.exprs[v + '..'] = { 'id': i, 'tag': v + '..', 'dot': 2 }


    def id(self, tag):
        if tag in self.exprs:
            return self.exprs[tag]['id']
        else:
            raise RuntimeError('Unknonw variable name!', tag)


    def dot(self, tag):
        if tag in self.exprs:
            return self.exprs[tag]['dot']
        else:
            raise RuntimeError('Unknonw variable name!', tag)
