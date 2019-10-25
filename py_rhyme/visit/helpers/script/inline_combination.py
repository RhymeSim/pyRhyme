import sys, re, StringIO, contextlib

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
            'q': { 'desc': 'Command mode', 'actions': {
                'q': { 'desc': 'Quit', 'ex': 'xq',
                    'run': lambda v, _: sys.exit(0),
                },
                'r': { 'desc': 'Run a VisItAPI or VisIt command', 'ex': 'xvreset_view(), xvExpressions()',
                    'run': lambda v, c: self.try_run_a_command(v, c),
                },
                'v': { 'desc': 'Reset view', 'ex': 'vr',
                    'run': lambda v, _: v.reset_view(),
                },
                's': { 'desc': 'Save window', 'ex': 'qs',
                    'run': lambda v, d: v.save(dir=d),
                },
            }},
            'h': { 'desc': 'Help mode', 'actions': {
                'u': { 'desc': 'Print usage', 'ex': 'hu',
                    'run': lambda v, _: self.usage(),
                },
                'm': { 'desc': 'Print metadata', 'ex': 'ia',
                    'run': lambda v, _: v.get_metadata(print_it=True),
                },
                'w': { 'desc': 'Print current woindow info', 'ex': 'iw, iwcycle',
                    'run': lambda v, k: v.get_window_metadata(print_it=True, key=k),
                },
                'v': { 'desc': 'Print valid variables', 'ex': 'iv',
                    'run': lambda v, _: v.get_window_metadata(print_it=True, key='variables'),
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
                'f': { 'desc': 'Play and reset the view', 'ex': 'cf, cf10',
                    'run': lambda v, l: self.play_cycles(v, l, reset_view=True),
                    'after': lambda v, _: v.cycle(self.cycle, reset_view=True),
                },
                'r': { 'desc': 'Record snapshots', 'ex': 'cr, cr10',
                    'run': lambda v, l: self.play_cycles(v, l, reset_view=True, save_it=True),
                    'after': lambda v, _: v.cycle(self.cycle, reset_view=True),
                },
            }},
            'x': { 'desc': 'X-axis mode', 'actions': {
                'u': { 'desc': 'Update unit', 'ex': 'xuMpc',
                    'run': lambda v, u: v.redraw(xunit=str(u)),
                    'after': lambda v, _: v.reset_view(),
                },
                't': { 'desc': 'Update title', 'ex': 'xtPosition X',
                    'run': lambda v, t: v.redraw(xtitle=str(t)),
                    'after': lambda v, _: v.reset_view(),
                },
                's': { 'desc': 'Update scaling', 'ex': 'xslinear',
                    'run': lambda v, s: v.redraw(xscale=str(s)),
                    'after': lambda v, _: v.reset_view(),
                },
            }},
            'y': { 'desc': 'Y-axis mode', 'actions': {
                'u': { 'desc': 'Update unit', 'ex': 'yuMpc',
                    'run': lambda v, u: v.redraw(yunit=str(u)),
                    'after': lambda v, _: v.reset_view(),
                },
                't': { 'desc': 'Update title', 'ex': 'ytPosition Y',
                    'run': lambda v, t: v.redraw(ytitle=str(t)),
                    'after': lambda v, _: v.reset_view(),
                },
                's': { 'desc': 'Update scaling', 'ex': 'yslog',
                    'run': lambda v, s: v.redraw(yscale=str(s)),
                    'after': lambda v, _: v.reset_view(),
                },
            }},
        }


    def set_cycle(self, cycle):
        while cycle < 0 or cycle >= self.ncycles:
            cycle = cycle + self.ncycles if cycle < 0 else cycle - self.ncycles

        self.cycle = cycle


    def play_cycles(self, vis, ncycles_str='', reset_view=False, save_it=False):
        if ncycles_str:
            to_cycle = self.cycle + int(ncycles_str)
        else:
            to_cycle = self.ncycles

        for i in range(self.cycle, to_cycle):
            vis.cycle(i, reset_view=reset_view)
            if save_it:
                vis.save()


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
        value = command_str[2:].strip() if len(command_str) > 2 else None

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


    def try_run_a_command(self, visitapi, command_str):
        # Have you ever seen something more unsage than this?! Wow..

        if not command_str:
            print('No command is given!')
            return

        if re.match('.+\(.*\)$', command_str):
            method_name = re.split('\(|\)', command_str)[0]
            args = re.split('\(|\)', command_str)[1]
        else:
            method_name = 'non_existing_method_name'
            args = ''


        errors = []

        try:
            # VisItAPI Command
            print(eval("getattr(visitapi, '" + method_name + "')(" + args + ")"))
        except Exception as err:
            try:
                # VisIt Command
                print(eval("__import__('visit')." + command_str))
            except Exception as err:
                errors.append(err)
                try:
                    # Python Command -- exec
                    with stdoutIO() as s:
                        exec(str(command_str))

                    print s.getvalue()
                except Exception as err:
                    errors.append(err)
                    for e in errors:
                        print e


@contextlib.contextmanager
def stdoutIO(stdout=None):
    sysstdout = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = sysstdout
