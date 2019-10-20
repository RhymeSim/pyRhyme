import sys


class InlineCombination():
    cycle = 0
    ncycles = 1

    def __init__(self, cycle=0, ncycles=1):
        self.cycle = int(cycle)
        self.ncycles = int(ncycles)

        self.modes = {
            'x': { 'desc': 'Command mode', 'actions': {
                'q': { 'desc': 'quit', 'ex': 'xq',
                    'run': lambda v, _: sys.exit(0)
                },
            }},
            't': { 'desc': 'Time mode', 'actions': {
                't': { 'desc': 'find snapshot with closes time', 'ex': 'tt16.5',
                    'run': lambda v, t: v.time(float(t)),
                },
            }},
            'c': { 'desc': 'Cycle mode', 'actions': {
                'n': { 'desc': 'change cycle', 'ex': 'cn25',
                    'run': lambda v, n: v.cycle(int(n)),
                    'after': lambda v, n: self.set_cycle(int(n))
                },
                'j': { 'desc': 'previous cycle', 'ex': 'cj',
                    'run': lambda v, _: v.prev_cycle(),
                    'after': lambda v, n: self.set_cycle(self.cycle - 1)
                },
                'k': { 'desc': 'next cycle', 'ex': 'ck',
                    'run': lambda v, _: v.next_cycle(),
                    'after': lambda v, n:  self.set_cycle(self.cycle + 1)
                },
                'p': { 'desc': 'play', 'ex': 'cp, cp10',
                    'run': lambda v, l: self.play_cycles(v, l),
                    'after': lambda v, _: v.cycle(self.cycle)
                },
            }},
        }


    def set_cycle(self, cycle):
        while cycle < 0 or cycle >= self.ncycles:
            cycle = cycle + self.ncycles if cycle < 0 else cycle - self.ncycles

        self.cycle = cycle


    def play_cycles(self, vis, ncycles_str=''):
        if ncycles_str:
            to_cycle = self.cycle + int(ncycles_str)
        else:
            to_cycle = self.ncycles

        for i in range(self.cycle, to_cycle):
            vis.cycle(i)


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
            raise RuntimeError('Wrong command combination format!', command_str)

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
        print('Combine following modes and actions to execute a command:')
        for m in self.modes.keys():
            print('%-8s: %s' % (m, self.modes[m]['desc']))
            acts = self.modes[m]['actions']
            for a in acts.keys():
                print( '-%-7s: %-40s e.g. %s' % (a, acts[a]['desc'], acts[a]['ex']))


    def wait(self, vis):
        self.usage()
        while True:
            combination_str = str(sys.stdin.readline().replace('\n', ''))
            self.handle(vis, combination_str)
