#!/usr/bin/env python

from __future__ import print_function

import argparse

import mdsynthesis


def attach_future_universe(sim, topology=None, trajectory=None):
    sim.universedef.topology = topology
    sim.universedef.trajectory = trajectory


def _is_quoted(value):
    if not value:
        return False
    single = value[0] == value[-1] == "'"
    double = value[0] == value[-1] == '"'
    return single or double


def _unquote(value):
    if _is_quoted(value):
        return value[1:-1]
    return value


def _category(value):
    transformed = value.split('=', 1)
    if len(transformed) != 2:
        raise argparse.ArgumentTypeError('Categories must follow the form '
                                         '"key=value". "{}" is not a valid '
                                         'input.'.format(value))

    if _is_quoted(transformed[1]):
        transformed[1] = _unquote(transformed[1])
    else:
        try:
            val = float(transformed[1])
        except ValueError:
            pass
        else:
            transformed[1] = val

    return transformed


def _selection(value):
    try:
        name, selection = value.split('=', 1)
    except ValueError:
        raise argparse.ArgumentError('Selections must follow the form '
                                     'name="selection string". "{}" is not a '
                                     'valid input'.format(value))
    selection = _unquote(selection)
    return name, selection


def _user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', '-c', type=_category, action='append',
                        help='Categories formatted as "key=value".')
    parser.add_argument('--tag', '-t', action='append',
                        help='Tag to attach to the simulation.')
    parser.add_argument('--topology', '-s',
                        help='Topology file. Does not have to exist already.')
    parser.add_argument('--trajectory', '-f',
                        help='Trajectory file. Does not have to exist already.')
    parser.add_argument('--selection', '-a', type=_selection, action='append',
                        help=('Selection string formatted as '
                              'name="selection sting".'))
    parser.add_argument('path')
    args = parser.parse_args()
    args.category = dict(args.category) if args.category else {}
    args.selection = dict(args.selection) if args.selection else {}
    return args


def summarize(sim):
    print('Sim:', sim.name)
    print('path:', sim.path)
    print('')
    
    if sim.tags:
        print('Tags')
        print('----')
        for tag in sim.tags:
            print('*', tag)
    else:
        print('No tag attached.')
    print('')

    if sim.categories.keys():
        print('Categories')
        print('----------')
        for name in sim.categories:
            print('*', name, '=', sim.categories[name])
    else:
        print('No category attached.')
    print('')

    if sim.data.keys():
        print('Data')
        print('----')
        for name in sim.data:
            print('*', name)
    else:
        print('No data attached.')
    print('')

    print('Universe')
    print('--------')
    print('* topology:', sim.universedef.topology)
    print('* trajectory:', sim.universedef.trajectory)
    print('')

    if sim.atomselections.keys():
        print('Selections')
        print('----------')
        for name in sim.atomselections.keys():
            print('*', name, '=', sim.atomselections[name])
    else:
        print('No atom selection attached.')
    print('')
    


def cli():
    args = _user_input()
    sim = mdsynthesis.Sim(args.path, tags=args.tag, categories=args.category)
    attach_future_universe(sim,
                           topology=args.topology,
                           trajectory=args.trajectory)
    for name, selection in args.selection.items():
        sim.atomselections.add(name, selection)

    summarize(sim)


if __name__ == '__main__':
    cli()
