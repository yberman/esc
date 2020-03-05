#!/usr/bin/env python3
"""
add_header.py

Read in a DIMACS file which doesn't have a header 
and add one. The header is of the form:
"p cnf VARCOUNT CLAUSECOUNT"

TODO(yberman) command line options for stdin/out
"""

import sys
import tempfile


t = tempfile.TemporaryFile(mode="w+")
variables = set()
clause_count = 0

for line in sys.stdin:
    line = line.strip()
    if line.startswith("p"):
        raise Exception("file has header")
    if line.startswith("c") or len(line) == 0:
        continue
    for w in line.split():
        x = abs(int(w))
        if x == 0:
            clause_count += 1
            continue
        variables.add(x)
    print(line, file=t)


print("p cnf %d %d" % (len(variables), clause_count))
t.seek(0)
for line in t.readlines():
    line = line.strip()
    print(line, file=sys.stdout)
