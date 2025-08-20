#!/usr/bin/env python3
"""
FastAPI Backend for 8-Puzzle Solver
Optimized for Render deployment
"""

import sys
import os
import time
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add parent directory to path to import our algorithms
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import our existing modules
try:
    from Abstractions import Node, Problem, reconstruct_path
    from Heuristics import HEURISTICS, GOAL
    spec = importlib.util.spec_from_file_location(
        "n_8_problem", 
        parent_dir / "Problems" / "N-8-Problem.py"
    )
    n_8_problem = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(n_8_problem)
    EightPuzzle = n_8_problem.EightPuzzle
    
    spec = importlib.util.spec_from_file_location(
        "search_algorithms", 
        parent_dir / "Search-algoritms" / "BFS - DFS - Uniform Cost - Greedy - A - IDA.py"
    )
    search_algorithms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search_algorithms)
    
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

app = FastAPI(
    title="8-Puzzle Solver API",
    description="API for solving 8-puzzle using various search algorithms",
    version="2.0.0"
)

# Request/Response models
class SolveRequest(BaseModel):
    algorithm: str
    heuristic: str = "manhattan"
    initial: List[List[int]]
    mode: str = "steps"

class StepInfo(BaseModel):
    board: List[List[int]]
    move: str
    heuristic: Optional[float] = None
    depth: int = 0
    cost: float = 0

class SolveResponse(BaseModel):
    success: bool
    message: str = ""
    steps: Optional[List[StepInfo]] = None
    metrics: Optional[Dict[str, Any]] = None

# Algorithm mapping
ALGORITHMS = {
    "bfs": search_algorithms.bfs,
    "dfs": search_algorithms.dfs,
    "ucs": search_algorithms.ucs,
    "greedy": search_algorithms.greedy,
    "astar": search_algorithms.astar,
    "ida": search_algorithms.ida_star,
}

def matrix_to_tuple(matrix: List[List[int]]) -> tuple:
    """Convert 3x3 matrix to flat tuple for our algorithms"""
    return tuple(item for row in matrix for item in row)

def tuple_to_matrix(state_tuple: tuple) -> List[List[int]]:
    """Convert flat tuple back to 3x3 matrix"""
    return [
        [state_tuple[0], state_tuple[1], state_tuple[2]],
        [state_tuple[3], state_tuple[4], state_tuple[5]],
        [state_tuple[6], state_tuple[7], state_tuple[8]]
    ]

def get_move_description(from_state: tuple, to_state: tuple) -> str:
    """Generate human-readable move description"""
    if from_state == to_state:
        return "Initial state"
    
    from_empty = from_state.index(0)
    to_empty = to_state.index(0)
    moved_number = from_state[to_empty]
    
    directions = {
        -3: "Up",
        3: "Down", 
        -1: "Left",
        1: "Right"
    }
    
    direction = directions.get(to_empty - from_empty, "Unknown")
    return f"Move {moved_number} {direction}"

def reconstruct_solution_steps(problem: EightPuzzle, result: Dict, heuristic_func) -> List[StepInfo]:
    """Reconstruct step-by-step solution from search result"""
    steps = []
    
    if not result.get('success') or not result.get('actions'):
        initial_matrix = tuple_to_matrix(problem.initial)
        steps.append(StepInfo(
            board=initial_matrix,
            move="Initial state",
            heuristic=heuristic_func(problem.initial) if heuristic_func else None,
            depth=0,
            cost=0
        ))
        return steps
    
    current_state = problem.initial
    current_cost = 0
    
    initial_matrix = tuple_to_matrix(current_state)
    steps.append(StepInfo(
        board=initial_matrix,
        move="Initial state", 
        heuristic=heuristic_func(current_state) if heuristic_func else None,
        depth=0,
        cost=current_cost
    ))
    
    for i, action in enumerate(result['actions']):
        next_state = problem.result(current_state, action)
        current_cost += problem.step_cost(current_state, action, next_state)
        
        matrix = tuple_to_matrix(next_state)
        move_desc = get_move_description(current_state, next_state)
        
        steps.append(StepInfo(
            board=matrix,
            move=move_desc,
            heuristic=heuristic_func(next_state) if heuristic_func else None,
            depth=i + 1,
            cost=current_cost
        ))
        
        current_state = next_state
    
    return steps

@app.get("/")
async def root():
    return {"message": "8-Puzzle Solver API", "version": "2.0.0", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/algorithms")
async def get_algorithms():
    """Get available algorithms and heuristics"""
    return {
        "algorithms": list(ALGORITHMS.keys()),
        "heuristics": list(HEURISTICS.keys())
    }

@app.post("/api/solve", response_model=SolveResponse)
async def solve_puzzle(request: SolveRequest):
    """Solve the 8-puzzle with specified algorithm and heuristic"""
    
    if request.algorithm not in ALGORITHMS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unknown algorithm: {request.algorithm}. Available: {list(ALGORITHMS.keys())}"
        )
    
    if request.algorithm in ["greedy", "astar", "ida"] and request.heuristic not in HEURISTICS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown heuristic: {request.heuristic}. Available: {list(HEURISTICS.keys())}"
        )
    
    try:
        initial_tuple = matrix_to_tuple(request.initial)
        if len(initial_tuple) != 9 or set(initial_tuple) != set(range(9)):
            raise ValueError("Invalid state")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Initial state must be a 3x3 matrix with numbers 0-8 exactly once"
        )
    
    problem = EightPuzzle(initial_tuple)
    algorithm_func = ALGORITHMS[request.algorithm]
    
    heuristic_func = None
    if request.algorithm in ["greedy", "astar", "ida"]:
        heuristic_func = lambda state: HEURISTICS[request.heuristic](state, GOAL)
    
    start_time = time.time()
    
    try:
        if heuristic_func:
            result = algorithm_func(problem, heuristic_func)
        else:
            result = algorithm_func(problem)
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        
        if not result.get('success'):
            return SolveResponse(
                success=False,
                message=result.get('message', 'No solution found'),
                steps=None,
                metrics=None
            )
        
        steps = reconstruct_solution_steps(problem, result, heuristic_func)
        
        metrics = {
            "moves": result.get('depth', 0),
            "time": execution_time,
            "nodes_explored": result.get('nodes_explored', 0),
            "cost": result.get('cost', 0),
            "algorithm": request.algorithm,
            "heuristic": request.heuristic if heuristic_func else None
        }
        
        return SolveResponse(
            success=True,
            message="Solution found successfully",
            steps=steps,
            metrics=metrics
        )
        
    except Exception as e:
        return SolveResponse(
            success=False,
            message=f"Error during solving: {str(e)}",
            steps=None,
            metrics=None
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting 8-Puzzle API Server on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)

# Request/Response models
class SolveRequest(BaseModel):
    algorithm: str
    heuristic: str = "manhattan"
    initial: List[List[int]]
    mode: str = "steps"

class StepInfo(BaseModel):
    board: List[List[int]]
    move: str
    heuristic: Optional[float] = None
    depth: int = 0
    cost: float = 0

class SolveResponse(BaseModel):
    success: bool
    message: str = ""
    steps: Optional[List[StepInfo]] = None
    metrics: Optional[Dict[str, Any]] = None

# Algorithm mapping
ALGORITHMS = {
    "bfs": search_algorithms.bfs,
    "dfs": search_algorithms.dfs,
    "ucs": search_algorithms.ucs,
    "greedy": search_algorithms.greedy,
    "astar": search_algorithms.astar,
    "ida": search_algorithms.ida_star,
}

def matrix_to_tuple(matrix: List[List[int]]) -> tuple:
    """Convert 3x3 matrix to flat tuple for our algorithms"""
    return tuple(item for row in matrix for item in row)

def tuple_to_matrix(state_tuple: tuple) -> List[List[int]]:
    """Convert flat tuple back to 3x3 matrix"""
    return [
        [state_tuple[0], state_tuple[1], state_tuple[2]],
        [state_tuple[3], state_tuple[4], state_tuple[5]],
        [state_tuple[6], state_tuple[7], state_tuple[8]]
    ]

def get_move_description(from_state: tuple, to_state: tuple) -> str:
    """Generate human-readable move description"""
    if from_state == to_state:
        return "Initial state"
    
    # Find the empty position (0) in both states
    from_empty = from_state.index(0)
    to_empty = to_state.index(0)
    
    # Find what number moved into the empty position
    moved_number = from_state[to_empty]
    
    # Determine direction
    directions = {
        -3: "Up",
        3: "Down", 
        -1: "Left",
        1: "Right"
    }
    
    direction = directions.get(to_empty - from_empty, "Unknown")
    return f"Move {moved_number} {direction}"

def reconstruct_solution_steps(problem: EightPuzzle, result: Dict, heuristic_func) -> List[StepInfo]:
    """Reconstruct step-by-step solution from search result"""
    steps = []
    
    if not result.get('success') or not result.get('actions'):
        # No solution found, return just initial state
        initial_matrix = tuple_to_matrix(problem.initial)
        steps.append(StepInfo(
            board=initial_matrix,
            move="Initial state",
            heuristic=heuristic_func(problem.initial) if heuristic_func else None,
            depth=0,
            cost=0
        ))
        return steps
    
    # Reconstruct path from actions
    current_state = problem.initial
    current_cost = 0
    
    # Add initial state
    initial_matrix = tuple_to_matrix(current_state)
    steps.append(StepInfo(
        board=initial_matrix,
        move="Initial state", 
        heuristic=heuristic_func(current_state) if heuristic_func else None,
        depth=0,
        cost=current_cost
    ))
    
    # Apply each action
    for i, action in enumerate(result['actions']):
        next_state = problem.result(current_state, action)
        current_cost += problem.step_cost(current_state, action, next_state)
        
        matrix = tuple_to_matrix(next_state)
        move_desc = get_move_description(current_state, next_state)
        
        steps.append(StepInfo(
            board=matrix,
            move=move_desc,
            heuristic=heuristic_func(next_state) if heuristic_func else None,
            depth=i + 1,
            cost=current_cost
        ))
        
        current_state = next_state
    
    return steps

@app.get("/")
async def root():
    return {"message": "8-Puzzle Solver API", "version": "2.0.0"}

@app.get("/algorithms")
async def get_algorithms():
    """Get available algorithms and heuristics"""
    return {
        "algorithms": list(ALGORITHMS.keys()),
        "heuristics": list(HEURISTICS.keys())
    }

@app.post("/api/solve", response_model=SolveResponse)
async def solve_puzzle(request: SolveRequest):
    """Solve the 8-puzzle with specified algorithm and heuristic"""
    
    # Validate algorithm
    if request.algorithm not in ALGORITHMS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unknown algorithm: {request.algorithm}. Available: {list(ALGORITHMS.keys())}"
        )
    
    # Validate heuristic for informed algorithms
    if request.algorithm in ["greedy", "astar", "ida"] and request.heuristic not in HEURISTICS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown heuristic: {request.heuristic}. Available: {list(HEURISTICS.keys())}"
        )
    
    # Validate initial state
    try:
        initial_tuple = matrix_to_tuple(request.initial)
        if len(initial_tuple) != 9 or set(initial_tuple) != set(range(9)):
            raise ValueError("Invalid state")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Initial state must be a 3x3 matrix with numbers 0-8 exactly once"
        )
    
    # Create problem instance
    problem = EightPuzzle(initial_tuple)
    
    # Get algorithm function
    algorithm_func = ALGORITHMS[request.algorithm]
    
    # Prepare heuristic function for informed algorithms
    heuristic_func = None
    if request.algorithm in ["greedy", "astar", "ida"]:
        heuristic_func = lambda state: HEURISTICS[request.heuristic](state, GOAL)
    
    # Measure execution time
    start_time = time.time()
    
    try:
        # Call the algorithm
        if heuristic_func:
            result = algorithm_func(problem, heuristic_func)
        else:
            result = algorithm_func(problem)
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Check if solution was found
        if not result.get('success'):
            return SolveResponse(
                success=False,
                message=result.get('message', 'No solution found'),
                steps=None,
                metrics=None
            )
        
        # Generate steps
        steps = reconstruct_solution_steps(problem, result, heuristic_func)
        
        # Prepare metrics
        metrics = {
            "moves": result.get('depth', 0),
            "time": execution_time,
            "nodes_explored": result.get('nodes_explored', 0),
            "cost": result.get('cost', 0),
            "algorithm": request.algorithm,
            "heuristic": request.heuristic if heuristic_func else None
        }
        
        return SolveResponse(
            success=True,
            message="Solution found successfully",
            steps=steps,
            metrics=metrics
        )
        
    except Exception as e:
        return SolveResponse(
            success=False,
            message=f"Error during solving: {str(e)}",
            steps=None,
            metrics=None
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting 8-Puzzle Solver API...")
    print("Available at: http://localhost:8000")
    print("Docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
