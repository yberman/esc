#!/bin/bash
# For 4, 5, and 6-gons confirm the conjecture
for ngon in $( seq 4 6 ); do
	echo ngon=$ngon
	for points in $( seq $ngon $(( (1 << ( $ngon -	2) ) + 1))); do
		./esc.py --ngon=$ngon --points=$points | \
			./add_dimacs_header.py > temp.cnf
		echo points=$points
		minisat temp.cnf solution > /dev/null
		minisat_return=$?
		echo $minisat_return
		if [[ $minisat_return == 10 ]]; then
			echo SAT
		elif [[ $minisat_return == 20 ]]; then
			echo UNSAT
		else
			exit 1
		fi
		echo
	done
	sleep 1
	echo
done
