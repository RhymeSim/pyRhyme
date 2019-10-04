import h5py as h5


class PyRhyme:
    """
    Reading and maniputaling Rhyme outputs

    data structure:
    {
        'attr': {
            'problem_domain': <list int, int, int>,
            'num_components': <int>,
            'num_levels': <int>,
            'iteration': <int>,
            'time': <float>,
            'component_0': <str>,
            ...
        },
        'levels': {
            0: {
                'dx': <list float, float, float>,
                'ref_ratio': <float>,
                'prob_domain': <list int, int, int, int, int, int>,
                'boxes': {
                    'min': <int>,
                    'max': <int>,
                    0: {
                        'corner': <list int, int, int, int, int>
                        'offset': <list int, ..., int>, for different components
                    },
                    ...
                },
                'data': numpy.ndarray
            },
            ...
        }
    }
    """

    def __init__(self, path):
        """
        Initializing a PyRhyme object by:
        - Loading attributes
        """

        file = h5.File(path, 'r')
        file_attr = file['/'].attrs

        self.snap = { 'attr': {}, 'levels': {} }

        self.snap['attr']['problem_domain'] = file_attr.get('ProblemDomain')
        self.snap['attr']['num_components'] = file_attr.get('num_components')
        self.snap['attr']['num_levels'] = file_attr.get('num_levels')
        self.snap['attr']['iteration'] = file_attr.get('iteration')
        self.snap['attr']['time'] = file_attr.get('time')

        ncomp = self.snap['attr']['num_components']
        nlev = self.snap['attr']['num_levels']

        for i in range(self.snap['attr']['num_components']):
            self.snap['attr']['component_%d' % i] = file_attr.get('component_%d' % i)


        for l in range(self.snap['attr']['num_levels']):
            self.snap['levels'][l] = {}

            lev = file['/level_%d' % l]
            snap_lev = self.snap['levels'][l]

            if l == 0:
                snap_lev['prob_domain'] = tuple([ pd for pd in lev.attrs.get('prob_domain') ])

            snap_lev['dx'] = tuple([ float(x) for x in lev.attrs.get('dx') ])
            snap_lev['ref_ratio'] = float(lev.attrs.get('ref_ratio'))

            snap_lev['data'] = lev['data:datatype=0']

            # TODO: Raise an exception if ll is not integer
            ll = int(len(snap_lev['data']) / ncomp)

            snap_lev['boxes'] = { 'max': len(lev['boxes']) - 1 }

            offset = 0
            for bi, b in enumerate(lev['boxes']):
                snap_lev['boxes'][bi] = {
                    'corner': tuple([ b[i] for i in range(6) ]),
                    'offset': tuple([ ll * i + offset for i in range(ncomp) ])
                }

                bl = [ b[i+3] - b[i] + 1 for i in range(3) ]
                offset += bl[0] * bl[1] * bl[2]
