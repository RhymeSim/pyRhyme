import os, glob, re
import h5py


def _open(path):
    dataset = {
        'state': {
            'active': 0
        },
        'info': {
            'num_of_files': 1,
        },
    }

    matches = re.findall('[0-9]{5}', path)
    ls = glob.glob(path.replace(matches[-1], '*')) if matches else [path]

    iopen = dataset['state']['active'] = ls.index(path)
    dataset['info']['num_of_files'] = len(ls)

    for i, p in enumerate(ls):
        dataset[i] = {}
        dataset[i]['path'] = p
        dataset[i]['opened'] = False

    dataset[iopen]['h5'] = _open_individual_h5(path)
    dataset[iopen]['opened'] = True

    return dataset


def _open_individual_h5(path):
    h5 = {}

    f = h5py.File(path, 'r')

    h5['file'] = f
    h5['attr'] = __read_attributes(f)
    h5['levels'] = __read_levels(f)

    return h5


def __read_attributes(f):
    atts = {}

    h5_atts = f['/'].attrs

    atts['ProblemDomain'] = tuple(map(lambda x: int(x), h5_atts.get('ProblemDomain')))
    ncomp = atts['num_components'] = int(h5_atts.get('num_components'))
    atts['num_levels'] = int(h5_atts.get('num_levels'))
    atts['iteration'] = int(h5_atts.get('iteration'))
    atts['time'] = float(h5_atts.get('time'))

    atts['comp'] = [h5_atts.get('component_%d' % i).decode('ascii') for i in range(ncomp)]

    return atts


def __read_levels(f):
    levels = {}

    for l in range(int(f['/'].attrs.get('num_levels'))):
        levels[l] = __read_level(f, l)

    return levels


def __read_level(f, l):
    level = {}

    ncomp = f['/'].attrs.get('num_components')
    h5_level = f['/level_%d' % l]

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
