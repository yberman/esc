#!/usr/bin/env python

import argparse
import itertools

def flags():
    parser = argparse.ArgumentParser(
        description='Generate sat problem corresponding to ESC for n gons on m points.')
    parser.add_argument('--ngon', dest='ngon_size', type=int, required=True)
    parser.add_argument('--points', dest='number_points', type=int, required=True)
    return parser.parse_args()

class Cnf:
    """
    Cnf boolean expression
    
    Currently simply prints DIMACS format to stdout. 
    """

    def __init__(self):
        self.variable_names = {}

    def v(self, *args):
        if len(args) == 1:
            args = args[0]
        variable_names = self.variable_names
        if args not in variable_names:
            variable_names[args] = len(variable_names) + 1
            print('c', variable_names[args], args)
        return variable_names[args]

    def clause(self, *c):
        c = list(c)
        c.append(0)
        print(' '.join(str(lit) for lit in c))


def four_point_axioms(cnf, n):
    '''
    Clauses to force valid configurations as specified in`Computer
    Solution to the 17-Point Erdos-Szkeres Problem` by Peters and Szekeres
    in formula (2.3).
    '''
    for (a, b, c, d) in itertools.combinations(range(n), 4):
        s1 = cnf.v("trip", a, b, c)
        s2 = cnf.v("trip", a, b, d)
        s3 = cnf.v("trip", a, c, d)
        s4 = cnf.v("trip", b, c, d)

        cnf.clause(-s1, +s2, -s3)
        cnf.clause(+s1, -s2, +s3)
        cnf.clause(-s1, +s3, -s4)
        cnf.clause(+s1, -s3, +s4)


def cc(size, first, pen, final, cups=False):
    """
    String representation of a cap or a cup.
    """
    struct = "cup" if cups else "cap"
    return "%s(size=%s, first=%s, pen=%s, final=%s)" % (struct, size, first, pen, final)

def caps(cnf, n, max_cap, cups=False):
    """Definitions variables for caps (cups)"""
    v = cnf.v
    for p1, p2, p3 in itertools.combinations(range(n), 3):
        cnf.clause(-v("trip", p1, p2, p3), v(cc(3, p1, p2, p3, False)))
        cnf.clause(v("trip", p1, p2, p3), v(cc(3, p1, p2, p3, True)))

    for size in range(3, max_cap + 1):
        for first, pen, final in itertools.combinations(range(n), 3):
            if final - first + 1 < size or pen - first + 2 < size:
                cnf.clause(-v(cc(size, first, pen, final, cups)))
                continue
            cnf.clause(-v(cc(size, first, pen, final, cups)), v(cc(size, first, None, final, cups)))
            if size == 3:
                # don't need inductive definition
                continue
            for m in range(first+1, pen):
                cnf.clause(-v(cc(size-1, first, m, pen, cups)), -v(cc(3, m, pen, final, cups)), v(cc(size, first, pen, final, cups)))


def caps_cups(cnf, n, max_cap, max_cup):
    caps(cnf, n, max_cap)
    caps(cnf, n, max_cup, cups=True)

def no_ngons(cnf, num_pts, ngon):
    v = cnf.v
    for first, final in itertools.combinations(range(num_pts), 2):
        cnf.clause(-v(cc(ngon, first, None, final, True)))
        cnf.clause(-v(cc(ngon, first, None, final, False)))
        for upper_size in range(3, ngon):
            lower_size = ngon + 2 - upper_size
            assert upper_size + lower_size == ngon + 2
            cnf.clause(-v(cc(upper_size, first, None, final, False)), -v(cc(lower_size, first, None, final, True)))

def main():
    FLAGS = flags()
    cnf = Cnf()

    num_pts = FLAGS.number_points
    ngon = FLAGS.ngon_size

    four_point_axioms(cnf, num_pts)
    caps_cups(cnf, num_pts, max_cap=ngon, max_cup=ngon)
    no_ngons(cnf, num_pts, ngon)


if __name__ == '__main__':
    main()
