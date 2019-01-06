import functools
import itertools
import operator
import re

from collections import defaultdict
from z3 import *

def make_grid(dimension):
    assert dimension > 0, "Need to have at least one cell"
    grid = []
    for row in range(dimension):
        cols = [BitVec(f"grid_{row}_{col}", 16) for col in range(dimension)]
        grid.append(cols)
    return grid

def get_mask(dimension):
    return BitVecVal(2**(dimension + 1) - 2, 16)

def add_row_constraints(solver, grid):
    d = len(grid)
    one = BitVecVal(1, 16)
    for r in range(d):
        result = (one << grid[r][0])
        for c in range(1, d):
            result |= (one << grid[r][c])
        solver.add(result == get_mask(d))

def add_column_constraints(solver, grid):
    d = len(grid)
    one = BitVecVal(1, 16)
    for c in range(d):
        result = (one << grid[0][c])
        for r in range(1, d):
            result |= (one << grid[r][c])
        solver.add(result == get_mask(d))

def print_board(model, grid):
    d = len(grid)
    for r in range(d):
        print(" ".join(str(model[grid[r][c]]) for c in range(d)))

def parse_board(board):
    lines = [l.strip() for l in board.split("\n") if l.strip()]
    if not all(len(l) == len(lines) for l in lines):
        raise RuntimeError("Invalid input, should be a square board.")

    coordinates = defaultdict(list)
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            coordinates[lines[y][x]].append((y,x)) 

    return len(lines), coordinates

def get_operator(op_token):
    return {
            '+': operator.add,
            '-': operator.sub,
            '/': operator.truediv,
            '*': operator.mul,
    }[op_token]

def parse_constraints(board,constraints):
    pattern = re.compile(r'[A-Za-z] = [+/*-]\d+')
    constraints = [l.strip() for l in constraints.split("\n") if l.strip()]
    for l in constraints:
        if not pattern.match(l):
            raise RuntimeError("Invalid constraint: {}.".format(l))

    constraint_list = []
    for l in constraints:
        c, o, d = l[0], l[4], int(l[5:])
        if not c in board:
            raise RuntimeError("Invalid constraint: {}.".format(l))
        constraint_list.append((c, get_operator(o), d))

    return constraint_list

def is_commutative(op):
    return op not in (operator.sub, operator.truediv)

def add_special_constraints(solver, board, grid, constraints):
    for Char, op, outcome in constraints:
        coords = board[Char]
        
        if is_commutative(op):
            perms = [coords]
        else:
            perms = itertools.permutations(coords)

        constraints = []
        for p in perms:
            y, x = p[0]
            constr = grid[y][x]
            for y, x in p[1:]:
                constr = op(constr, grid[y][x])
            constraints.append(constr == outcome)

        if is_commutative(op):
            solver.add(Or(*constraints))
        else:
            solver.add(constraints[0])

    return grid, solver

def make_solver(dimension, board, constraints):
    solver = Solver()

    grid = make_grid(dimension)
    add_column_constraints(solver, grid)
    add_row_constraints(solver, grid)

    return add_special_constraints(solver, board, grid, constraints)

def check_and_print(solution, grid):
    if not solution.check():
        print("Cannot find solution.")
    else:
        print_board(solution.model(), grid)

def read_input(filename):
    f = open(filename)
    board, constraints = f.read().split("\n\n")

    dimension, board = parse_board(board)
    constraints = parse_constraints(board, constraints)

    return dimension, board, constraints

def run(filename):
    dimension, board, constraints = read_input(filename)    
    grid, solution = make_solver(dimension, board, constraints)
    check_and_print(solution, grid)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Solve some calcudoku')
    parser.add_argument('input', metavar='INPUT', help='calcudoku input file format')
    args = parser.parse_args()
    run(args.input)
