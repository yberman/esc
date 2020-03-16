#!/usr/bin/env python3
"""
pen_free.py

Generate lots of sets of points which do not contain a convex pentagon.
"""
import points as pts

known = set()
for i in range(100000000):
    points = pts.random_points(8)
    if points.has_poly(5):
        continue
    else:
        if points.vec() in known:
            continue
        print(points.points)
        known.add(points.vec())

