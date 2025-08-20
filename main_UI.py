names = [r[0] for r in rows]
times = [r[3] for r in rows]
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importaciones de módulos propios
import importlib.util
import sys
import os
from Heuristics import manhattan, misplaced

# Importar Puzzle
from Problems import N_8_Problem as N8
Puzzle = N8.Puzzle

# Importar algoritmos desde archivo con nombre complejo
algos_path = os.path.join(os.path.dirname(__file__), 'Search-algoritms', 'BFS - DFS - Uniform Cost - Greedy - A - IDA.py')
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

def run_algorithms():
	start = tuple(int(e.get()) for e in entries)
	p = Puzzle(start)
	algos = [
		("BFS", lambda pr: BFS(pr)),
		("DFS", lambda pr: DFS(pr)),
		("UCS", lambda pr: UCS(pr)),
		("Greedy(manhattan)", lambda pr: Greedy(pr, manhattan)),
		("A*(manhattan)", lambda pr: A_star(pr, manhattan)),
		("A*(misplaced)", lambda pr: A_star(pr, misplaced)),
		("IDA*(manhattan)", lambda pr: IDA_star(pr, manhattan)),
	]
	rows = []
	for name, fn in algos:
		try:
			import time
			t0 = time.time()
			result, expanded = fn(p)
			dt = time.time() - t0
			if result is None:
				depth = None; cost = None; steps = None
			else:
				steps = [a for a,_ in result][1:]
				depth = len(steps)
				cost = result[-1][1] if hasattr(result[-1], '__getitem__') and len(result[-1])>1 else None
			rows.append((name, expanded, depth, dt))
		except Exception as ex:
			rows.append((name, 'error', 'error', 'error'))
	show_results(rows)

def show_results(rows):
	for i in tree.get_children():
		tree.delete(i)
	for r in rows:
		tree.insert('', 'end', values=r)
	names = [r[0] for r in rows]
	times = [r[3] if isinstance(r[3], (int, float)) else 0 for r in rows]
	fig = plt.Figure(figsize=(6,3))
	ax = fig.add_subplot(111)
	ax.bar(range(len(times)), times)
	ax.set_xticks(range(len(times)))
	ax.set_xticklabels(names, rotation=45, ha='right')
	ax.set_ylabel('Tiempo (s)')
	ax.set_title('Comparación de tiempos por algoritmo')
	fig.tight_layout()
	canvas = FigureCanvasTkAgg(fig, master=frame_plot)
	canvas.draw()
	for widget in frame_plot.winfo_children():
		widget.destroy()
	canvas.get_tk_widget().pack(fill='both', expand=True)

# Interfaz Tkinter
root = tk.Tk()
root.title("Comparador de algoritmos de búsqueda - 8 Puzzle")

frame_input = ttk.Frame(root)
frame_input.pack(padx=10, pady=10)
ttk.Label(frame_input, text="Estado inicial (0=hueco):").grid(row=0, column=0, columnspan=9)
entries = []
for i in range(9):
	e = ttk.Entry(frame_input, width=2, justify='center')
	e.grid(row=1, column=i)
	e.insert(0, str([1,4,2,7,5,3,0,8,6][i]))
	entries.append(e)
ttk.Button(frame_input, text="Ejecutar algoritmos", command=run_algorithms).grid(row=2, column=0, columnspan=9, pady=5)

frame_table = ttk.Frame(root)
frame_table.pack(padx=10, pady=5, fill='x')
cols = ("Algoritmo", "Expandidos", "Profundidad", "Tiempo (s)")
tree = ttk.Treeview(frame_table, columns=cols, show='headings', height=7)
for c in cols:
	tree.heading(c, text=c)
	tree.column(c, width=120)
tree.pack(side='left', fill='x', expand=True)
scroll = ttk.Scrollbar(frame_table, orient='vertical', command=tree.yview)
tree.configure(yscroll=scroll.set)
scroll.pack(side='right', fill='y')

frame_plot = ttk.Frame(root)
frame_plot.pack(padx=10, pady=10, fill='both', expand=True)

root.mainloop()