from typing import Callable, Dict, Optional, Any
import time
import sys
import os

# Añadir el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Abstractions import Problem, Node, reconstruct_path, reconstruct_actions
from Strucure import Stack, Queue, MinHeap

SearchResult = Dict[str, Any]

def bfs(problem: Problem) -> SearchResult:
    """Búsqueda en anchura (Breadth-First Search)"""
    start_time = time.perf_counter()
    frontier = Queue()
    start_node = Node(problem.initial_state())
    frontier.push(start_node)
    explored = set()
    expanded = 0
    
    while not frontier.is_empty():
        node = frontier.pop()
        
        if problem.is_goal(node.state):
            end_time = time.perf_counter()
            path = reconstruct_path(node)
            actions = reconstruct_actions(node)
            return {
                'success': True,
                'path': path,
                'actions': actions,
                'cost': node.g,
                'depth': node.depth,
                'expanded': expanded,
                'time': end_time - start_time
            }
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        expanded += 1
        
        for child in node.expand(problem):
            if child.state not in explored:
                frontier.push(child)
    
    end_time = time.perf_counter()
    return {
        'success': False,
        'path': None,
        'actions': None,
        'cost': None,
        'depth': None,
        'expanded': expanded,
        'time': end_time - start_time
    }

def dfs(problem: Problem, depth_limit: Optional[int] = None) -> SearchResult:
    """Búsqueda en profundidad (Depth-First Search)"""
    start_time = time.perf_counter()
    frontier = Stack()
    start_node = Node(problem.initial_state())
    frontier.push(start_node)
    explored = set()
    expanded = 0
    
    while not frontier.is_empty():
        node = frontier.pop()
        
        if problem.is_goal(node.state):
            end_time = time.perf_counter()
            path = reconstruct_path(node)
            actions = reconstruct_actions(node)
            return {
                'success': True,
                'path': path,
                'actions': actions,
                'cost': node.g,
                'depth': node.depth,
                'expanded': expanded,
                'time': end_time - start_time
            }
        
        if node.state in explored:
            continue
            
        if depth_limit is not None and node.depth >= depth_limit:
            continue
            
        explored.add(node.state)
        expanded += 1
        
        for child in node.expand(problem):
            if child.state not in explored:
                frontier.push(child)
    
    end_time = time.perf_counter()
    return {
        'success': False,
        'path': None,
        'actions': None,
        'cost': None,
        'depth': None,
        'expanded': expanded,
        'time': end_time - start_time
    }

def ucs(problem: Problem) -> SearchResult:
    """Búsqueda de costo uniforme (Uniform Cost Search)"""
    start_time = time.perf_counter()
    frontier = MinHeap()
    start_node = Node(problem.initial_state())
    frontier.push(start_node, 0.0)
    best_g = {start_node.state: 0.0}
    expanded = 0
    
    while not frontier.is_empty():
        _, node = frontier.pop()
        
        if problem.is_goal(node.state):
            end_time = time.perf_counter()
            path = reconstruct_path(node)
            actions = reconstruct_actions(node)
            return {
                'success': True,
                'path': path,
                'actions': actions,
                'cost': node.g,
                'depth': node.depth,
                'expanded': expanded,
                'time': end_time - start_time
            }
        
        if node.state in best_g and node.g > best_g[node.state]:
            continue
            
        expanded += 1
        
        for child in node.expand(problem):
            if child.state not in best_g or child.g < best_g[child.state]:
                best_g[child.state] = child.g
                frontier.push(child, child.g)
    
    end_time = time.perf_counter()
    return {
        'success': False,
        'path': None,
        'actions': None,
        'cost': None,
        'depth': None,
        'expanded': expanded,
        'time': end_time - start_time
    }

def greedy(problem: Problem, h: Callable) -> SearchResult:
    """Búsqueda voraz (Greedy Best-First Search)"""
    start_time = time.perf_counter()
    frontier = MinHeap()
    start_node = Node(problem.initial_state())
    h_value = h(start_node.state)
    frontier.push(start_node, h_value)
    explored = set()
    expanded = 0
    
    while not frontier.is_empty():
        _, node = frontier.pop()
        
        if problem.is_goal(node.state):
            end_time = time.perf_counter()
            path = reconstruct_path(node)
            actions = reconstruct_actions(node)
            return {
                'success': True,
                'path': path,
                'actions': actions,
                'cost': node.g,
                'depth': node.depth,
                'expanded': expanded,
                'time': end_time - start_time
            }
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        expanded += 1
        
        for child in node.expand(problem):
            if child.state not in explored:
                h_value = h(child.state)
                frontier.push(child, h_value)
    
    end_time = time.perf_counter()
    return {
        'success': False,
        'path': None,
        'actions': None,
        'cost': None,
        'depth': None,
        'expanded': expanded,
        'time': end_time - start_time
    }

def astar(problem: Problem, h: Callable) -> SearchResult:
    """Búsqueda A* (A-Star)"""
    start_time = time.perf_counter()
    frontier = MinHeap()
    start_node = Node(problem.initial_state())
    f_value = start_node.g + h(start_node.state)
    frontier.push(start_node, f_value)
    best_g = {start_node.state: 0.0}
    expanded = 0
    
    while not frontier.is_empty():
        _, node = frontier.pop()
        
        if problem.is_goal(node.state):
            end_time = time.perf_counter()
            path = reconstruct_path(node)
            actions = reconstruct_actions(node)
            return {
                'success': True,
                'path': path,
                'actions': actions,
                'cost': node.g,
                'depth': node.depth,
                'expanded': expanded,
                'time': end_time - start_time
            }
        
        if node.state in best_g and node.g > best_g[node.state]:
            continue
            
        expanded += 1
        
        for child in node.expand(problem):
            if child.state not in best_g or child.g < best_g[child.state]:
                best_g[child.state] = child.g
                f_value = child.g + h(child.state)
                frontier.push(child, f_value)
    
    end_time = time.perf_counter()
    return {
        'success': False,
        'path': None,
        'actions': None,
        'cost': None,
        'depth': None,
        'expanded': expanded,
        'time': end_time - start_time
    }

def ida_star(problem: Problem, h: Callable, max_bound: int = 10000) -> SearchResult:
    """Búsqueda IDA* (Iterative Deepening A-Star)"""
    start_time = time.perf_counter()
    start_node = Node(problem.initial_state())
    bound = h(start_node.state)
    expanded_total = 0
    
    def dfs_limited(node, g, bound):
        nonlocal expanded_total
        f = g + h(node.state)
        if f > bound:
            return f, None
        if problem.is_goal(node.state):
            return f, node
        
        min_bound = float('inf')
        expanded_total += 1
        
        for child in node.expand(problem):
            child_g = g + (child.g - node.g)
            t, result = dfs_limited(child, child_g, bound)
            if result is not None:
                return t, result
            if t < min_bound:
                min_bound = t
        
        return min_bound, None
    
    while bound <= max_bound:
        t, solution_node = dfs_limited(start_node, 0, bound)
        if solution_node is not None:
            end_time = time.perf_counter()
            path = reconstruct_path(solution_node)
            actions = reconstruct_actions(solution_node)
            return {
                'success': True,
                'path': path,
                'actions': actions,
                'cost': solution_node.g,
                'depth': solution_node.depth,
                'expanded': expanded_total,
                'time': end_time - start_time
            }
        if t == float('inf'):
            break
        bound = t
    
    end_time = time.perf_counter()
    return {
        'success': False,
        'path': None,
        'actions': None,
        'cost': None,
        'depth': None,
        'expanded': expanded_total,
        'time': end_time - start_time
    }

# Aliases para compatibilidad con código existente
BFS = bfs
DFS = dfs
UCS = ucs
Greedy = greedy
A_star = astar
IDA_star = ida_star
