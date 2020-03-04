# Erdos-Szekeres Conjecture

Programs to confirm the Erdos-Szekeres Conjecture for the known cases.

Generates a DIMACS CNF format file, which can be tested and should produce
no solutions.

For 17 points, and ngon=6 (the largest known case), it completes in ... hours.

## usage

Note that `esc.py` doesn't put in a proper header for the DIMACS format, this
can be fixed with `add_header.py` but it is not strictly needed for minisat.

```bash
# install minisat
# maybe "sudo apt install minisat"

# run the program
for ngon in $( seq 4 6 ); do
  for points in $( seq $ngon $(( (1 << ( $ngon -  2) ) + 1))); do
    python3 esc.py --ngon=$ngon --points=$points | python3 add_header.py > temp.cnf
    echo points=$points ngon=$ngon
    minisat temp.cnf | grep SAT
  done
done
```
