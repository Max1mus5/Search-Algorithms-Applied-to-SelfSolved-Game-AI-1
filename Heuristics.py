GOAL = (1,2,3,4,5,6,7,8,0)
GOAL_POS = {v:i for i,v in enumerate(GOAL)}

# Clase dummy para tipado, solo para evitar errores de importación
class PuzzleState:
    def __init__(self, tiles): self.tiles = tuple(tiles)
    def key(self): return self.tiles
    def __repr__(self): return f"PuzzleState{self.tiles}"

def misplaced(s: PuzzleState) -> int:
    return sum(1 for i,v in enumerate(s.tiles) if v != 0 and v != GOAL[i])

def manhattan(s: PuzzleState) -> int:
    dist = 0
    for i,v in enumerate(s.tiles):
        if v == 0: continue
        gi = GOAL_POS[v]
        x1,y1 = divmod(i,3); x2,y2 = divmod(gi,3)
        dist += abs(x1-x2) + abs(y1-y2)
    return dist