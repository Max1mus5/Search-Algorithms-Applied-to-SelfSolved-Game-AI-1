
from typing import Any, Iterable, Optional, List, Tuple

class State:
    def key(self) -> Any: raise NotImplementedError
    def __hash__(self): return hash(self.key())
    def __eq__(self, o): return isinstance(o, State) and self.key()==o.key()

class Problem:
    def initial_state(self) -> Any: raise NotImplementedError
    def is_goal(self, state: Any) -> bool: raise NotImplementedError
    def actions(self, state: Any) -> Iterable[Any]: raise NotImplementedError
    def result(self, state: Any, action: Any) -> Any: raise NotImplementedError
    def step_cost(self, state: Any, action: Any, next_state: Any) -> float: return 1.0
    
    # Método para compatibilidad con FASE 1
    def successors(self, state: Any):
        """Retorna (action, next_state, step_cost) para cada acción válida"""
        for action in self.actions(state):
            next_state = self.result(state, action)
            cost = self.step_cost(state, action, next_state)
            yield (action, next_state, cost)
    
    def goal_test(self, state: Any) -> bool:
        return self.is_goal(state)

class Node:
    __slots__ = ("state", "parent", "action", "g", "depth", "f")
    def __init__(self, state: Any, parent: Optional['Node']=None, action: Optional[Any]=None, step_cost: float=0.0, f: float=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = (parent.g + step_cost) if parent else 0.0
        self.depth = (parent.depth + 1) if parent else 0
        self.f = f  # para A*/Greedy
        
    def expand(self, problem: Problem):
        for action, next_state, cost in problem.successors(self.state):
            yield Node(next_state, self, action, cost)

def reconstruct_path(goal_node: Node) -> List[Any]:
    """Devuelve lista de estados desde inicial a meta"""
    path = []
    current = goal_node
    while current:
        path.append(current.state)
        current = current.parent
    return list(reversed(path))

def reconstruct_actions(goal_node: Node) -> List[Any]:
    """Devuelve lista de acciones desde inicial a meta"""
    actions = []
    current = goal_node
    while current and current.action is not None:
        actions.append(current.action)
        current = current.parent
    return list(reversed(actions))
