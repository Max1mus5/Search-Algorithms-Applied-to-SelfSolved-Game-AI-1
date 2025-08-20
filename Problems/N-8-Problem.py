import time

def run_and_measure(problem, algorithms):
    rows = []
    for name, fn in algorithms:
        t0 = time.time()
        result, expanded = fn(problem)
        dt = time.time() - t0
        if result is None:
            depth = None; cost = None; steps = None
        else:
            steps = [a for a,_ in result][1:]  # acciones excluyendo el None inicial
            depth = len(steps)
            cost = result[-1][1]  # estado final (no usamos g aquí por simplicidad)
        rows.append((name, expanded, depth, dt))
    return rows

# Instancia de prueba

# Representación: tupla de 9 ints; 0 = hueco
from Abstractions import State, Problem
import importlib.util
import sys
import os
from Heuristics import manhattan, misplaced

# Importar algoritmos desde archivo con nombre complejo
algos_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Search-algoritms', 'BFS - DFS - Uniform Cost - Greedy - A - IDA.py')
spec = importlib.util.spec_from_file_location("algos_mod", algos_path)
algos_mod = importlib.util.module_from_spec(spec)
sys.modules["algos_mod"] = algos_mod
spec.loader.exec_module(algos_mod)
BFS = algos_mod.BFS
DFS = algos_mod.DFS
UCS = algos_mod.UCS
Greedy = algos_mod.Greedy
A_star = algos_mod.A_star
IDA_star = algos_mod.IDA_star

GOAL = (1,2,3,4,5,6,7,8,0)
GOAL_POS = {v:i for i,v in enumerate(GOAL)}

class PuzzleState(State):
    __slots__ = ("tiles",)
    def __init__(self, tiles): self.tiles = tuple(tiles)
    def key(self): return self.tiles
    def __repr__(self): return f"PuzzleState{self.tiles}"

class Puzzle(Problem):
    def __init__(self, start):
        self.start = PuzzleState(start)
    def initial_state(self) -> State: return self.start
    def is_goal(self, s: PuzzleState) -> bool: return s.tiles == GOAL
    def actions(self, s: PuzzleState):
        i = s.tiles.index(0); x,y = divmod(i,3)
        for dx,dy,a in ((1,0,"DOWN"),(-1,0,"UP"),(0,1,"RIGHT"),(0,-1,"LEFT")):
            nx,ny = x+dx,y+dy
            if 0 <= nx < 3 and 0 <= ny < 3: yield a
    def result(self, s: PuzzleState, a):
        delta = {"DOWN":(1,0),"UP":(-1,0),"RIGHT":(0,1),"LEFT":(0,-1)}[a]
        i = s.tiles.index(0); x,y = divmod(i,3)
        nx,ny = x+delta[0], y+delta[1]; j = nx*3+ny
        tiles = list(s.tiles); tiles[i], tiles[j] = tiles[j], tiles[i]
        return PuzzleState(tiles)
START = (1,2,3,4,5,6,0,7,8)  # puedes cambiarla por otras
p = Puzzle(START)

algos = [
    ("BFS", lambda pr: BFS(pr)),
    ("DFS", lambda pr: DFS(pr)),
    ("UCS", lambda pr: UCS(pr)),
    ("Greedy(manhattan)", lambda pr: Greedy(pr, manhattan)),
    ("A*(manhattan)", lambda pr: A_star(pr, manhattan)),
    ("A*(misplaced)", lambda pr: A_star(pr, misplaced)),
    ("IDA*(manhattan)", lambda pr: IDA_star(pr, manhattan)),
]

rows = run_and_measure(p, algos)
for r in rows:
    print(f"{r[0]:18s} | expandidos={r[1]:6} | profundidad={r[2]} | tiempo={r[3]:.3f}s")