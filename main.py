
import time
import sys
import os
import importlib.util

# Agregar paths para imports
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'Problems'))
sys.path.append(os.path.join(current_dir, 'Search-algoritms'))

# Importar módulos usando importlib para evitar problemas con nombres de archivo
try:
    # Importar N-8-Problem
    n8_path = os.path.join(current_dir, 'Problems', 'N-8-Problem.py')
    spec = importlib.util.spec_from_file_location("n8_mod", n8_path)
    n8_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(n8_mod)
    EightPuzzle = n8_mod.EightPuzzle
    
    from Heuristics import HEURISTICS, GOAL
    
    # Importar algoritmos desde archivo con nombre complejo
    algos_path = os.path.join(current_dir, 'Search-algoritms', 'BFS - DFS - Uniform Cost - Greedy - A - IDA.py')
    spec = importlib.util.spec_from_file_location("algos_mod", algos_path)
    algos_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(algos_mod)

    bfs = algos_mod.bfs
    dfs = algos_mod.dfs
    ucs = algos_mod.ucs
    greedy = algos_mod.greedy
    astar = algos_mod.astar
    ida_star = algos_mod.ida_star
    
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)

PRESETS = {
    "facil":  (1,2,3,4,5,6,7,0,8),
    "medio":  (1,2,3,4,5,6,0,7,8),
    "dificil":(7,2,4,5,0,6,8,3,1),
}

def print_board(state):
    """Imprime el tablero en formato 3x3"""
    print("┌─────────┐")
    for i in range(0,9,3):
        row = state[i:i+3]
        formatted_row = " ".join("·" if x==0 else str(x) for x in row)
        print(f"│ {formatted_row} │")
    print("└─────────┘")

def validate_state(state):
    """Valida que el estado sea válido para el 8-puzzle"""
    if len(state) != 9:
        return False, "El estado debe tener exactamente 9 números"
    
    if sorted(state) != list(range(9)):
        return False, "El estado debe contener los números 0-8 sin repetir"
    
    return True, ""

def is_solvable(state):
    """Verifica si el estado es resoluble usando la paridad de inversiones"""
    # Contar inversiones (excluyendo el 0)
    tiles = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i+1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    
    # Para el 8-puzzle, es resoluble si el número de inversiones es par
    return inversions % 2 == 0

def run_cli():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              8-PUZZLE BUSCADORES (FASE 1)                ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    # Selección de algoritmo
    print("\n🔍 Algoritmos disponibles:")
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. UCS (Uniform Cost Search)")
    print("4. Greedy (Best-First Search)")
    print("5. A* (A-Star)")
    print("6. IDA* (Iterative Deepening A*)")
    
    while True:
        alg_choice = input("\nSelecciona algoritmo (1-6): ").strip()
        alg_map = {"1": "bfs", "2": "dfs", "3": "ucs", "4": "greedy", "5": "astar", "6": "ida"}
        
        if alg_choice in alg_map:
            alg = alg_map[alg_choice]
            break
        else:
            print("❌ Opción inválida. Por favor selecciona un número del 1 al 6.")
    
    # Selección de heurística para algoritmos informados
    hname = None
    if alg in ("greedy", "astar", "ida"):
        print("\n🧠 Heurísticas disponibles:")
        print("1. Manhattan Distance")
        print("2. Misplaced Tiles")
        
        while True:
            h_choice = input("Selecciona heurística (1-2): ").strip()
            h_map = {"1": "manhattan", "2": "misplaced"}
            
            if h_choice in h_map:
                hname = h_map[h_choice]
                break
            else:
                print("❌ Heurística inválida. Por favor selecciona 1 o 2.")
    
    # Selección de estado inicial
    print("\n🎯 Estado inicial:")
    print("1. Fácil:", PRESETS["facil"])
    print("2. Medio:", PRESETS["medio"])
    print("3. Difícil:", PRESETS["dificil"])
    print("4. Manual")
    
    while True:
        choice = input("Selecciona (1-4): ").strip()
        
        if choice == "1":
            initial = PRESETS["facil"]
            break
        elif choice == "2":
            initial = PRESETS["medio"]
            break
        elif choice == "3":
            initial = PRESETS["dificil"]
            break
        elif choice == "4":
            while True:
                try:
                    raw = input("Ingresa 9 números (0-8) separados por espacio: ")
                    parts = [int(x) for x in raw.strip().split()]
                    
                    valid, msg = validate_state(parts)
                    if not valid:
                        print(f"❌ {msg}")
                        continue
                    
                    initial = tuple(parts)
                    
                    if not is_solvable(initial):
                        print("⚠️  Advertencia: Este estado puede no tener solución (número impar de inversiones)")
                        confirm = input("¿Continuar de todos modos? (s/N): ").strip().lower()
                        if confirm != 's':
                            continue
                    
                    break
                except ValueError:
                    print("❌ Entrada inválida. Asegúrate de ingresar 9 números separados por espacios.")
            break
        else:
            print("❌ Opción inválida. Por favor selecciona un número del 1 al 4.")
    
    print(f"\n📋 Estado inicial:")
    print_board(initial)
    
    print(f"📋 Estado objetivo:")
    print_board(GOAL)
    
    # Crear problema y ejecutar algoritmo
    problem = EightPuzzle(initial)
    
    print(f"\n⚡ Ejecutando {alg.upper()}{'(' + hname + ')' if hname else ''}...")
    print("   Por favor espera...")
    
    try:
        if alg == "bfs":
            res = bfs(problem)
        elif alg == "dfs":
            res = dfs(problem, depth_limit=50)
        elif alg == "ucs":
            res = ucs(problem)
        elif alg == "greedy":
            h_func = lambda s: HEURISTICS[hname](s, GOAL)
            res = greedy(problem, h_func)
        elif alg == "astar":
            h_func = lambda s: HEURISTICS[hname](s, GOAL)
            res = astar(problem, h_func)
        elif alg == "ida":
            h_func = lambda s: HEURISTICS[hname](s, GOAL)
            res = ida_star(problem, h_func)
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        return
    
    # Mostrar resultados
    print("\n" + "="*60)
    print(f"📊 RESULTADOS")
    print("="*60)
    print(f"Algoritmo: {alg.upper()}")
    if hname:
        print(f"Heurística: {hname}")
    
    if res['success']:
        print(f"✅ Solución encontrada!")
        print(f"📏 Profundidad: {res['depth']}")
        print(f"💰 Costo: {res['cost']}")
        print(f"🔍 Nodos expandidos: {res['expanded']}")
        print(f"⏱️  Tiempo: {res['time']:.6f} segundos")
        if res['actions']:
            print(f"🗺️  Pasos (acciones): {' → '.join(res['actions'])}")
        
        # Opción de mostrar paso a paso
        while True:
            show = input("\n¿Mostrar tablero paso a paso? (s/N): ").strip().lower()
            if show in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n🎬 Secuencia de estados:")
                print("="*30)
                for i, state in enumerate(res["path"]):
                    if i > 0:
                        print(f"\n➡️  Acción: {res['actions'][i-1]}")
                    print(f"\n📍 Paso {i}:")
                    print_board(state)
                    if i < len(res["path"]) - 1:
                        input("Presiona Enter para continuar...")
                print("\n🎉 ¡Solución completada!")
                break
            elif show in ['n', 'no', '']:
                break
            else:
                print("❌ Por favor responde 's' para sí o 'n' para no.")
                
    else:
        print("❌ No se encontró solución")
        print(f"🔍 Nodos expandidos: {res['expanded']}")
        print(f"⏱️  Tiempo: {res['time']:.6f} segundos")
        
        if alg == "dfs":
            print("💡 Nota: DFS tiene límite de profundidad de 50. Intenta con otro algoritmo.")
        elif alg == "ida":
            print("💡 Nota: IDA* alcanzó el límite máximo. El problema puede requerir más iteraciones.")

def run_batch_test():
    """Ejecuta una prueba rápida de todos los algoritmos con el estado fácil"""
    print("🧪 Ejecutando prueba rápida de todos los algoritmos...")
    problem = EightPuzzle(PRESETS["facil"])
    
    algorithms = [
        ("BFS", lambda: bfs(problem)),
        ("DFS", lambda: dfs(problem, depth_limit=10)),
        ("UCS", lambda: ucs(problem)),
        ("Greedy(manhattan)", lambda: greedy(problem, lambda s: HEURISTICS["manhattan"](s, GOAL))),
        ("A*(manhattan)", lambda: astar(problem, lambda s: HEURISTICS["manhattan"](s, GOAL))),
        ("A*(misplaced)", lambda: astar(problem, lambda s: HEURISTICS["misplaced"](s, GOAL))),
    ]
    
    print(f"{'Algoritmo':<20} {'Éxito':<6} {'Prof.':<5} {'Costo':<6} {'Expandidos':<10} {'Tiempo(s)':<10}")
    print("-" * 65)
    
    for name, algo_func in algorithms:
        try:
            result = algo_func()
            success = "✅" if result['success'] else "❌"
            depth = result['depth'] if result['depth'] is not None else "N/A"
            cost = result['cost'] if result['cost'] is not None else "N/A"
            expanded = result['expanded']
            time_taken = f"{result['time']:.4f}"
            
            print(f"{name:<20} {success:<6} {depth:<5} {cost:<6} {expanded:<10} {time_taken:<10}")
        except Exception as e:
            print(f"{name:<20} ❌     N/A   N/A    N/A        Error")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--mobile":
            print("🚧 Modo móvil no implementado en FASE 1")
            print("💡 Usa main_UI.py para la interfaz gráfica básica")
        elif sys.argv[1] == "--test":
            run_batch_test()
        else:
            print("Opciones disponibles:")
            print("  --mobile  : Interfaz móvil (no implementado)")
            print("  --test    : Prueba rápida de algoritmos")
    else:
        run_cli()