README
------

A Calcudoku is a logical puzzle in which you, like a soduku, have to fill
distinct numbers in every row and column (1 through n), where n is the width
of the calcudoku. 

In addition there are a number of areas, roughly like below in which the numbershave to combine to a certain total, under one of the basic operations like
+, -, * or /. So for example, the two numbers in the top-right area can
have a hint (2-), which means that if you substract the smaller from the larger
one you should end up with 2.


        +-+-+---+
	|.|.|. .|
	| | +---+
	|.|.|. .|
	+-+ | |-|
	|.|.|.|.|
        | +-+-+ |
	|. .|. .|
	+-------+

Note that numbers in an area need not be distinct!

You provide the input as a square of letters (capitals or lowercase), where
the same letters designate the same area, plus the constraint for every area.
The constraint is usually written inside the area in a puzzle.

Board and constraints should be separated by an empty line. The board has to
be square.

Example Input
-------------

	ABCC
	ABDD
	EBDF
	EEFF

	A = -1
	B = +6
	C = -2
	D = +5
	E = +7
	F = +9

Example output
--------------

	python calcudoku.py example1.txt
		3 1 4 2
		4 2 3 1
		2 3 1 4
		1 4 2 3


And indeed you can verify that 4-3 = 1 (Area A), 1 + 2 + 3 = 6 (Area B), etc.
Note that Area D (3 + 1 + 1) has two 1s in it, which is fine, since they are
not on the same row or column.

Implementation
--------------

All the heavy lifting is done by the Z3 theorem prover: https://github.com/Z3Prover/z3/wiki 

This is just a thin wrapper to parse the input and make the model. You need to install this
in order for the solver to work.
