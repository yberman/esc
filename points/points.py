"""
points.py -- sets of points.

Has convenient methods for testing for convex polygons.
"""
import collections
import itertools
import math
import random

class Points:
    def __init__(self):
        # the underlying points in xy-coordinates
        self.points = []
        self.sig = {}
        self.length = -1
        self.is_clean = False
        self.vec_cache = None
        self.proj_cache = None

    def dirty(self):
        self.sig.clear()
        self.length = -1
        self.is_clean = False
        self.vec_cache = None
        self.proj_cache = None

    def clean(self):
        if self.is_clean:
            return
        self.points.sort()
        i_points = list(enumerate(self.points))
        for t1, t2, t3 in itertools.combinations(i_points, 3):
            i1, p1 = t1
            i2, p2 = t2
            i3, p3 = t3
            self.sig[i1, i2, i3] = self.__fast_trip_sig(p1, p2, p3) > 0
        self.length = len(self.points)
        self.is_clean = True

    def Sig(self):
        """Encodes CC-System info into a dict."""
        r = {}
        self.clean()
        for i1, i2, i3 in self.sig:
            r[i1, i2, i3] = self.sig[i1, i2, i3]
            r[i2, i3, i1] = r[i1, i2, i3]
            r[i3, i1, i2] = r[i1, i2, i3]
            r[i3, i2, i1] = not self.sig[i1, i2, i3]
            r[i1, i3, i2] = r[i3, i2, i1]
            r[i2, i1, i3] = r[i3, i2, i1]
        return r

    def add(self, p):
        self.points.append(p)
        self.dirty()

    def add_random(self, n):
        for i in range(n):
            self.add((random.random(), random.random()))

    def trip(self, t):
        self.clean()
        return self.sig[t]

    def __det(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return x1*y2 - x2*y1

    def __trip_sig(self, p1, p2, p3):
        return self.__det(p1, p2) - self.__det(p1, p3) + self.__det(p2, p3)

    def __fast_trip_sig(self, p1, p2, p3):
        """An optimization of __trip_sig."""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        return x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)

    def __str__(self):
        return str(self.points)

    def is_quad(self, quad):
        s = 0
        for t in itertools.combinations(quad, 3):
            if self.trip(t):
                s += 1
        return s % 2 == 0

    def is_poly(self, poly):
        for quad in itertools.combinations(poly, 4):
            if not self.is_quad(quad):
                return False
        return True

    def has_poly(self, n):
        self.clean()
        if not self.length >= n:
            return False
        for poly in itertools.combinations(range(self.length), n):
            if self.is_poly(poly):
                return True
        return False

    def vec(self):
        self.clean()
        if not self.vec_cache:
            r = []
            for t in itertools.combinations(range(self.length), 3):
                r.append(int(self.trip(t)))
            self.vec_cache = tuple(r)
        return self.vec_cache


    def proj(self, n):
        self.clean()
        if not self.proj_cache:
            r = []
            for point_subset in itertools.combinations(self.points, n):
                ss = Points()
                for p in point_subset:
                    ss.add(p)
                r.append(ss.vec())
            r.sort()
            r = tuple(r)
            self.proj_cache = r
        return self.proj_cache


def random_points(n):
    r = Points()
    r.add_random(n)
    return r

def polygon(n):
    """Return a pentagon on the interval [0, 1]x[0, 1]."""
    pts = Points()
    theta = math.pi*2/n
    for i in range(n):
        pts.add((math.cos(theta*i)/2 + .5, math.sin(theta*i)/2 + .5))
    pts.clean()
    return pts

# def label(s):
#     s = set(s)
#     r = {}
#     for i, x in enumerate(sorted(s)):
#         r[x] = i
#     return r
# 
# def mod2set(l):
#     r = set()
#     for x in l:
#         r ^= set([x])
#     return frozenset(r)
# 
# 
# def intersect_values(d1, d2):
#     s = set(d1.values()) & set(d2.values())
#     return s
# 
# def mod2(t):
#     s = set()
#     l = list(t)
#     for k in l:
#         if l.count(k) % 2:
#             s.add(k)
#     return s
#             
