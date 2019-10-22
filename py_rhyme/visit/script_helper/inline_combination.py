import sys, re
from pprint import pprint

try:
    from visit import *
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


class InlineCombination():
    cycle = 0
    ncycles = 1

    def __init__(self, cycle=0, ncycles=1):
        self.cycle = int(cycle)
        self.ncycles = int(ncycles)

        self.modes = {
            'x': { 'desc': 'Command mode', 'actions': {
                'q': { 'desc': 'Quit', 'ex': 'xq',
                    'run': lambda v, _: sys.exit(0),
                },
                'v': { 'desc': 'Run a VisIt command', 'ex': 'xvExpressions()',
                    'run': lambda v, c: self.try_run_a_visit_command(c),
                },
                'r': { 'desc': 'Run a VisItAPI command', 'ex': 'xrget_metadata(print_it=True)',
                    'run': lambda v, c: self.try_run_a_visitapi_command(v, c),
                },
            }},
            'h': { 'desc': 'Help mode', 'actions': {
                'u': { 'desc': 'Print usage', 'ex': 'hu',
                    'run': lambda v, _: self.usage(),
                },
            }},
            'i': { 'desc': 'Info mode', 'actions': {
                'a': { 'desc': 'All windows', 'ex': 'ia',
                    'run': lambda v, _: v.get_metadata(print_it=True),
                },
                'w': { 'desc': 'Current woindow', 'ex': 'iw, iwcycle',
                    'run': lambda v, k: v.get_window_metadata(print_it=True, key=k),
                },
            }},
            't': { 'desc': 'Time mode', 'actions': {
                't': { 'desc': 'Find snapshot with closes time', 'ex': 'tt16.5',
                    'run': lambda v, t: v.time(float(t)),
                    'after': lambda v, _: v.reset_view(),
                },
            }},
            'c': { 'desc': 'Cycle mode', 'actions': {
                'n': { 'desc': 'Change cycle', 'ex': 'cn25',
                    'run': lambda v, n: v.cycle(int(n)),
                    'after': lambda v, n: self.set_cycle(int(n)),
                },
                'j': { 'desc': 'Previous cycle', 'ex': 'cj',
                    'run': lambda v, _: v.prev_cycle(),
                    'after': lambda v, n: self.set_cycle(self.cycle - 1),
                },
                'k': { 'desc': 'Next cycle', 'ex': 'ck',
                    'run': lambda v, _: v.next_cycle(),
                    'after': lambda v, n:  self.set_cycle(self.cycle + 1),
                },
                'p': { 'desc': 'Play', 'ex': 'cp, cp10',
                    'run': lambda v, l: self.play_cycles(v, l, reset_view=False),
                    'after': lambda v, _: v.cycle(self.cycle, reset_view=False),
                },
                'f': { 'desc': 'Play and follow the view', 'ex': 'cf, cf10',
                    'run': lambda v, l: self.play_cycles(v, l, reset_view=True),
                    'after': lambda v, _: v.cycle(self.cycle, reset_view=True),
                },
            }},
            'v': { 'desc': 'View mode', 'actions': {
                'r': { 'desc': 'Reset view', 'ex': 'vr',
                    'run': lambda v, _: v.reset_view(),
                },
                'x': { 'desc': 'Update x-axis title', 'ex': 'vxPos X',
                    'run': lambda v, t: v.redraw(xtitle=str(t)),
                    'after': lambda v, _: v.reset_view(),
                },
                'y': { 'desc': 'Update y-axis title', 'ex': 'vyPos Y',
                    'run': lambda v, t: v.redraw(ytitle=str(t)),
                    'after': lambda v, _: v.reset_view(),
                },
            }},
            'u': { 'desc': 'Unit mode', 'actions': {
                'x': { 'desc': 'Update x-axis unit', 'ex': 'uxMpc',
                    'run': lambda v, u: v.redraw(xunit=str(u)),
                    'after': lambda v, _: v.reset_view(),
                },
                'y': { 'desc': 'Update y-axis unit', 'ex': 'uyMpc',
                    'run': lambda v, u: v.redraw(yunit=str(u)),
                    'after': lambda v, _: v.reset_view(),
                },
            }},
        }


    def set_cycle(self, cycle):
        while cycle < 0 or cycle >= self.ncycles:
            cycle = cycle + self.ncycles if cycle < 0 else cycle - self.ncycles

        self.cycle = cycle


    def play_cycles(self, vis, ncycles_str='', reset_view=False):
        if ncycles_str:
            to_cycle = self.cycle + int(ncycles_str)
        else:
            to_cycle = self.ncycles

        for i in range(self.cycle, to_cycle):
            vis.cycle(i, reset_view=reset_view)


    def mode(self, mode, mode_desc):
        if len(mode) > 1:
            raise RuntimeError('Mode specifier should be a character!', md)

        if mode in self.modes:
            self.modes[mode]['desc'] = mode_desc
        else:
            self.modes[mode] = { 'desc': mode_desc, 'actions': {} }


    def action(self, md, act, act_desc, act_ex, run, before=None, after=None):

        if len(md) > 1:
            raise RuntimeError('Mode specifier should be a character!', md)
        if len(act) > 1:
            raise RuntimeError('Action specifier should be a character!', act)

        if md not in self.modes:
            self.modes[md] = { 'desc': '', 'actions': {} }

        actions = self.modes[md]['actions']

        if act not in actions:
            actions[act] = {}

        actions[act]['desc'] = act_desc
        actions[act]['ex'] = act_ex
        actions[act]['run'] = run

        if before:
            actions[act]['before'] = before

        if after:
            actions[act]['after'] = after


    def handle(self, vis, command_str):
        if len(command_str) < 2:
            print('Wrong command combination!', command_str)
            return

        mode = command_str[0]
        action = command_str[1]
        value = command_str[2:] if len(command_str) > 2 else None

        if mode not in self.modes:
            print('Unknown mode:', mode)
            return

        if action not in self.modes[mode]['actions']:
            print('Unknow action', action, 'in', 'mode')
            return


        if 'before' in self.modes[mode]['actions'][action]:
            self.modes[mode]['actions'][action]['before'](vis, value)

        self.modes[mode]['actions'][action]['run'](vis, value)

        if 'after' in self.modes[mode]['actions'][action]:
            self.modes[mode]['actions'][action]['after'](vis, value)


    def usage(self):
        print('Combine following modes and actions to execute a command:\n')

        for m in self.modes.keys():
            print('%-1s (%s)' % (m, self.modes[m]['desc']))
            acts = self.modes[m]['actions']
            for key, a in acts.items():
                print( '-%-7s: %-40s ex: %s' % (key, a['desc'], a['ex']))

            print('')


    def wait(self, vis):
        self.usage()

        while True:
            sys.stdout.write('>>> ')
            combination_str = str(sys.stdin.readline().replace('\n', ''))
            self.handle(vis, combination_str)


    def try_run_a_visit_command(self, command_str):
        try:
            ret = eval("__import__('visit')." + str(command_str))
            self.pretty_print(ret)
        except Exception as err:
            print(err)


    def try_run_a_visitapi_command(self, visitapi, command_str):
        if not re.match('.+\(.*\)$', command_str):
            print('Wrong command format!', command_str)
            return

        method_name = re.split('\(|\)', command_str)[0]
        args = re.split('\(|\)', command_str)[1]

        try:
            ret = eval("getattr(visitapi, '" + method_name + "')(" + args + ")")
            self.pretty_print(ret)
        except Exception as err:
            print(err)


    def pretty_print(self, v):
        if type(v) in [dict, list, tuple]:
            pprint(v)
        else:
            print(v)
