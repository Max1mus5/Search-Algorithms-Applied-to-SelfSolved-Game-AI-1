from typing import List, Tuple, Iterable
import sys
import os

# Añadir el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Abstractions import Problem

Action = str
State = Tuple[int, ...]  # largo 9

GOAL = (1,2,3,4,5,6,7,8,0)

class EightPuzzle(Problem):
    def __init__(self, initial: State, goal: State=GOAL):
        self.initial = initial
        self.goal = goal
        
    def initial_state(self) -> State:
        return self.initial
        
    def is_goal(self, state: State) -> bool:
        return state == self.goal
        
    def actions(self, state: State) -> Iterable[Action]:
        """Retorna las acciones válidas desde un estado"""
        i = state.index(0)  # posición del hueco
        x, y = divmod(i, 3)  # convertir a coordenadas x,y
        
        actions = []
        if x > 0: actions.append("up")      # puede mover hacia arriba
        if x < 2: actions.append("down")    # puede mover hacia abajo  
        if y > 0: actions.append("left")    # puede mover hacia izquierda
        if y < 2: actions.append("right")   # puede mover hacia derecha
        
        return actions
    
    def result(self, state: State, action: Action) -> State:
        """Aplica una acción y retorna el nuevo estado"""
        i = state.index(0)  # posición del hueco
        x, y = divmod(i, 3)
        
        # Calcular nueva posición del hueco
        if action == "up":
            new_x, new_y = x - 1, y
        elif action == "down":
            new_x, new_y = x + 1, y
        elif action == "left":
            new_x, new_y = x, y - 1
        elif action == "right":
            new_x, new_y = x, y + 1
        else:
            raise ValueError(f"Acción inválida: {action}")
            
        j = new_x * 3 + new_y  # nueva posición lineal
        
        # Intercambiar hueco con la ficha
        tiles = list(state)
        tiles[i], tiles[j] = tiles[j], tiles[i]
        
        return tuple(tiles)
    
    def step_cost(self, state: State, action: Action, next_state: State) -> int:
        return 1
        
    def successors(self, state: State) -> Iterable[Tuple[Action, State, int]]:
        """Retorna (action, next_state, step_cost) para cada acción válida"""
        for action in self.actions(state):
            next_state = self.result(state, action)
            cost = self.step_cost(state, action, next_state)
            yield (action, next_state, cost)

# Alias para compatibilidad con código existente
class PuzzleState:
    def __init__(self, tiles): 
        self.tiles = tuple(tiles)
    def key(self): 
        return self.tiles
    def __repr__(self): 
        return f"PuzzleState{self.tiles}"

class Puzzle(Problem):
    """Clase de compatibilidad con código existente"""
    def __init__(self, start):
        if isinstance(start, (list, tuple)):
            self.start_state = start
        else:
            self.start_state = start.tiles if hasattr(start, 'tiles') else start
        self.puzzle = EightPuzzle(self.start_state)
        
    def initial_state(self):
        return self.start_state
        
    def is_goal(self, state):
        if hasattr(state, 'tiles'):
            return state.tiles == GOAL
        return state == GOAL
        
    def actions(self, state):
        if hasattr(state, 'tiles'):
            state = state.tiles
        return self.puzzle.actions(state)
        
    def result(self, state, action):
        if hasattr(state, 'tiles'):
            state = state.tiles
        return self.puzzle.result(state, action)
        
    def successors(self, state):
        if hasattr(state, 'tiles'):
            state = state.tiles
        return self.puzzle.successors(state)

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    # Estados de prueba
    easy = (1,2,3,4,5,6,7,0,8)
    medium = (1,2,3,4,5,6,0,7,8) 
    hard = (7,2,4,5,0,6,8,3,1)
    
    puzzle = EightPuzzle(easy)
    print(f"Estado inicial: {puzzle.initial_state()}")
    print(f"¿Es meta?: {puzzle.is_goal(puzzle.initial_state())}")
    print(f"Acciones válidas: {list(puzzle.actions(puzzle.initial_state()))}")
    
    # Probar una acción
    if puzzle.actions(puzzle.initial_state()):
        action = list(puzzle.actions(puzzle.initial_state()))[0]
        new_state = puzzle.result(puzzle.initial_state(), action)
        print(f"Después de '{action}': {new_state}")
        
    print("Pruebas del 8-puzzle completadas.")