import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import importlib.util

# Agregar paths para imports
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'Problems'))
sys.path.append(os.path.join(current_dir, 'Search-algoritms'))

try:
    # Importar N-8-Problem usando importlib
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

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver (FASE 1)")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.alg_var = tk.StringVar(value="astar")
        self.h_var = tk.StringVar(value="manhattan")
        self.result_var = tk.StringVar(value="Listo para resolver...")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="🧩 8-Puzzle Solver", 
                              font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="FASE 1 - Algoritmos de Búsqueda", 
                                 font=("Arial", 10))
        subtitle_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Selección de algoritmo
        algo_frame = tk.LabelFrame(main_frame, text="Algoritmo", padx=10, pady=10)
        algo_frame.pack(fill="x", pady=5)
        
        algorithms = [
            ("BFS", "bfs"),
            ("DFS", "dfs"), 
            ("UCS", "ucs"),
            ("Greedy", "greedy"),
            ("A*", "astar"),
            ("IDA*", "ida")
        ]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.alg_var, 
                               value=value, command=self.on_algorithm_change)
            rb.pack(side="left", padx=5)
        
        # Selección de heurística
        self.heuristic_frame = tk.LabelFrame(main_frame, text="Heurística", padx=10, pady=10)
        self.heuristic_frame.pack(fill="x", pady=5)
        
        heuristics = [("Manhattan", "manhattan"), ("Misplaced Tiles", "misplaced")]
        for text, value in heuristics:
            rb = tk.Radiobutton(self.heuristic_frame, text=text, variable=self.h_var, value=value)
            rb.pack(side="left", padx=5)
        
        # Estado inicial
        state_frame = tk.LabelFrame(main_frame, text="Estado Inicial", padx=10, pady=10)
        state_frame.pack(fill="x", pady=5)
        
        tk.Label(state_frame, text="Ingresa 9 números (0-8) separados por espacio:").pack()
        
        self.entry = tk.Entry(state_frame, width=40, font=("Courier", 12))
        self.entry.insert(0, "1 2 3 4 5 6 7 0 8")
        self.entry.pack(pady=5)
        
        # Estados predefinidos
        presets_frame = tk.Frame(state_frame)
        presets_frame.pack(pady=5)
        
        presets = [
            ("Fácil", "1 2 3 4 5 6 7 0 8"),
            ("Medio", "1 2 3 4 5 6 0 7 8"),
            ("Difícil", "7 2 4 5 0 6 8 3 1")
        ]
        
        for name, state in presets:
            btn = tk.Button(presets_frame, text=name, 
                           command=lambda s=state: self.set_state(s))
            btn.pack(side="left", padx=5)
        
        # Botón resolver
        solve_btn = tk.Button(main_frame, text="🔍 Resolver", command=self.solve,
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                             pady=10)
        solve_btn.pack(pady=20)
        
        # Resultados
        result_frame = tk.LabelFrame(main_frame, text="Resultados", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, pady=5)
        
        self.result_text = tk.Text(result_frame, height=10, wrap=tk.WORD, 
                                  font=("Courier", 10))
        scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Actualizar interfaz inicial
        self.on_algorithm_change()
        
    def set_state(self, state_str):
        """Establece un estado predefinido"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, state_str)
        
    def on_algorithm_change(self):
        """Actualiza la interfaz cuando cambia el algoritmo"""
        alg = self.alg_var.get()
        if alg in ("greedy", "astar", "ida"):
            self.heuristic_frame.pack(fill="x", pady=5, after=self.heuristic_frame.master.children[list(self.heuristic_frame.master.children.keys())[0]])
        else:
            self.heuristic_frame.pack_forget()
    
    def validate_input(self, input_str):
        """Valida la entrada del usuario"""
        try:
            parts = [int(x) for x in input_str.strip().split()]
            if len(parts) != 9:
                return False, "Debe ingresar exactamente 9 números"
            if sorted(parts) != list(range(9)):
                return False, "Debe usar los números 0-8 sin repetir"
            return True, tuple(parts)
        except ValueError:
            return False, "Formato inválido. Use números separados por espacios"
    
    def solve(self):
        """Ejecuta el algoritmo seleccionado"""
        try:
            # Validar entrada
            input_str = self.entry.get().strip()
            valid, result = self.validate_input(input_str)
            
            if not valid:
                messagebox.showerror("Error", result)
                return
                
            initial_state = result
            
            # Crear problema
            problem = EightPuzzle(initial_state)
            
            # Obtener algoritmo y heurística
            alg = self.alg_var.get()
            hname = self.h_var.get()
            
            # Actualizar interfaz
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Ejecutando {alg.upper()}...\n")
            self.result_text.update()
            
            # Ejecutar algoritmo
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
            else:
                messagebox.showerror("Error", "Algoritmo no reconocido")
                return
            
            # Mostrar resultados
            self.display_results(res, alg, hname)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución:\n{str(e)}")
    
    def display_results(self, result, algorithm, heuristic):
        """Muestra los resultados en la interfaz"""
        self.result_text.delete(1.0, tk.END)
        
        # Encabezado
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, "📊 RESULTADOS\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        
        # Información del algoritmo
        self.result_text.insert(tk.END, f"Algoritmo: {algorithm.upper()}\n")
        if heuristic and algorithm in ("greedy", "astar", "ida"):
            self.result_text.insert(tk.END, f"Heurística: {heuristic}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Resultados
        if result['success']:
            self.result_text.insert(tk.END, "✅ Solución encontrada!\n\n")
            self.result_text.insert(tk.END, f"📏 Profundidad: {result['depth']}\n")
            self.result_text.insert(tk.END, f"💰 Costo: {result['cost']}\n")
            self.result_text.insert(tk.END, f"🔍 Nodos expandidos: {result['expanded']}\n")
            self.result_text.insert(tk.END, f"⏱️  Tiempo: {result['time']:.6f} segundos\n\n")
            
            if result['actions']:
                self.result_text.insert(tk.END, "🗺️  Secuencia de acciones:\n")
                actions_text = " → ".join(result['actions'])
                self.result_text.insert(tk.END, f"   {actions_text}\n\n")
            
            # Mostrar algunos estados clave
            if result['path'] and len(result['path']) > 1:
                self.result_text.insert(tk.END, "📋 Estados clave:\n\n")
                self.result_text.insert(tk.END, "Estado inicial:\n")
                self.display_board(result['path'][0])
                self.result_text.insert(tk.END, "\nEstado final:\n")
                self.display_board(result['path'][-1])
        else:
            self.result_text.insert(tk.END, "❌ No se encontró solución\n\n")
            self.result_text.insert(tk.END, f"🔍 Nodos expandidos: {result['expanded']}\n")
            self.result_text.insert(tk.END, f"⏱️  Tiempo: {result['time']:.6f} segundos\n\n")
            
            if algorithm == "dfs":
                self.result_text.insert(tk.END, "💡 Nota: DFS tiene límite de profundidad.\n")
            elif algorithm == "ida":
                self.result_text.insert(tk.END, "💡 Nota: IDA* alcanzó el límite máximo.\n")
    
    def display_board(self, state):
        """Muestra un tablero en formato texto"""
        self.result_text.insert(tk.END, "┌─────────┐\n")
        for i in range(0, 9, 3):
            row = state[i:i+3]
            formatted_row = " ".join("·" if x == 0 else str(x) for x in row)
            self.result_text.insert(tk.END, f"│ {formatted_row} │\n")
        self.result_text.insert(tk.END, "└─────────┘\n")

def main():
    """Función principal"""
    root = tk.Tk()
    app = PuzzleGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
