# Erdos-Szekeres Conjecture

Program to confirm the Erdos-Szekeres Conjecture for the known cases.

Generates a DIMACS CNF format file, which can be tested and should produce
no solutions. It does not add a header to the DIMACS file, but I've added
a script that can append it.

Currently it does not halt for 17 points in a reasonable ammount of time,
and I am trying to improve that.

Usage:
```bash
python3 esc.py --ngon 5 --points 9 > temp.cnf
```

See also `run.sh`.
