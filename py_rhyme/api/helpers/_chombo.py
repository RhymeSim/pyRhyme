def _attrs(f):
    h5_attrs = f['/'].attrs

    attrs = {}
    attrs['ProblemDomain'] = tuple(
        map(lambda x: int(x), h5_attrs.get('ProblemDomain'))
    )
    attrs['num_components'] = ncomps = int(h5_attrs.get('num_components'))
    attrs['num_levels'] = int(h5_attrs.get('num_levels'))
    attrs['iteration'] = int(h5_attrs.get('iteration'))
    attrs['time'] = float(h5_attrs.get('time'))
    attrs['components'] = [
        h5_attrs.get('component_%d' % i).decode('ascii')
        for i in range(ncomps)
    ]

    return attrs


def _levels(f):
    levels = {}

    nlevels = f['/'].attrs.get('num_levels')

    for l in range(nlevels):
        levels[l] = _level(f, l)

    return levels


def _level(f, l):
    level = {}

    h5_level = f['/level_%d' % l]
    ncomp = f['/'].attrs.get('num_components')

    if l == 0:
        level['prob_domain'] = tuple(
            map(lambda x: int(x), h5_level.attrs.get('prob_domain')[0])
        )

    level['dx'] = tuple(map(lambda x: float(x), h5_level.attrs.get('dx')))
    level['ref_ratio'] = float(h5_level.attrs.get('ref_ratio'))


    level['data'] = h5_level['data:datatype=0']
    level['len_data'] = len(level['data']) / ncomp

    level['boxes'] = {}

    offset = 0
    for bi, b in enumerate(h5_level['boxes']):
        level['boxes'][bi] = {
            'corner': tuple(map(lambda x: int(x), b)),
            'offset': [level['len_data'] * i + offset for i in range(ncomp)]
        }

        bl = [b[i+3] - b[i] + 1 for i in range(3)]
        offset += bl[0] * bl[1] * bl[2]

    return level
