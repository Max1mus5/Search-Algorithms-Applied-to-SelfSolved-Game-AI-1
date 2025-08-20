from typing import Tuple, Callable, Dict

State = Tuple[int, ...]
GOAL = (1,2,3,4,5,6,7,8,0)
GOAL_POS = {v:i for i,v in enumerate(GOAL)}

def misplaced_tiles(state: State, goal: State = GOAL) -> int:
    """Número de fichas mal ubicadas (excluye el hueco 0)"""
    return sum(1 for i,v in enumerate(state) if v != 0 and v != goal[i])

def manhattan_distance(state: State, goal: State = GOAL) -> int:
    """Suma de distancias Manhattan por ficha (excluye el hueco 0)"""
    dist = 0
    goal_pos = {v:i for i,v in enumerate(goal)}
    for i,v in enumerate(state):
        if v == 0: continue
        gi = goal_pos[v]
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(gi, 3)
        dist += abs(x1-x2) + abs(y1-y2)
    return dist

# Aliases para compatibilidad
def misplaced(state: State) -> int:
    return misplaced_tiles(state, GOAL)

def manhattan(state: State) -> int:
    return manhattan_distance(state, GOAL)

# Clase dummy para tipado, solo para evitar errores de importación
class PuzzleState:
    def __init__(self, tiles): self.tiles = tuple(tiles)
    def key(self): return self.tiles
    def __repr__(self): return f"PuzzleState{self.tiles}"

# Mapa por nombre para el menú
HEURISTICS: Dict[str, Callable[[State, State], int]] = {
    "misplaced": misplaced_tiles,
    "manhattan": manhattan_distance,
}